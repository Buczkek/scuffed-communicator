import sys
import time

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QListView, QPlainTextEdit, QFileDialog, \
    QCheckBox, QLabel, QLineEdit, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt, QEvent

import requests as r
import socketio


class Client:
    def __init__(self, mainWindow, url='http://127.0.0.1:8080/', debug=False):
        self.socket = socketio.client.Client(reconnection_attempts=5, reconnection_delay=10)
        self.cookies = {'session': ''}
        self.loginResponse = None
        self.nickname = ''
        self.debug = debug
        self.url = url
        self.id = 0
        self.mainWindow = mainWindow

        @self.socket.on('message')
        def handle_message(data):
            if debug:
                print(data)
            self.mainWindow.newMessage(data['content'], 1)

        @self.socket.on('connect')
        def handle_connect():
            if debug:
                print("Connected")

        @self.socket.on('disconnect')
        def handle_disconnect():
            if debug:
                print("Disconnected")

        @self.socket.on('connect_error')
        def handle_connection_error(err):
            if debug:
                print(f"Connection ERROR | {err}")

        @self.socket.on('success')
        def handle_success(data):
            if debug:
                print(f"Success! Event: {data.get('event', None)}")

        @self.socket.on('failure')
        def handle_failure(data):
            if debug:
                print(f"Failure! Event: {data.get('event', None)}")

        @self.socket.on('messages')
        def handle_messages(data):
            if debug:
                print(data)
            self.mainWindow.addMessages(data)

        @self.socket.on('connection')
        def handle_connection(data):
            self.mainWindow.addConnection(data['connection'])

    def login(self, nickname='', password=''):
        if self.debug:
            print("Logging in...")
        response = r.post(self.url + '/login/', data={'nickname': nickname, 'password': password})
        self.loginResponse = response
        if response.text:
            print(response.text)
            self.nickname = nickname
            self.id = int(response.text)
            self.cookies = response.cookies
            print('siema')
            return self.id
        return self.id

    def signup(self, nickname='', password=''):
        if self.debug:
            print("Signing up...")
        response = r.post(self.url + '/signup/', data={'nickname': nickname, 'password': password})
        return response.text == 'success'

    def connect(self):
        if self.debug:
            print("Connecting...")
        assert self.cookies['session']
        self.socket.connect(self.url, headers={'Cookie': f'session={self.cookies["session"]}'})
        return True

    def send_message(self, content, recipient, group=False):
        if self.debug:
            print("Sending message")
        self.socket.emit('message', {'content': content, 'recipient': recipient, 'group': group})

    def disconnect(self):
        if self.debug:
            print("Disconnecting...")
        self.socket.disconnect()
        self.cookies = {'session': ''}
        self.loginResponse = None
        self.nickname = ''
        self.id = 0

    def get_connections(self):
        if self.debug:
            print("Getting connections")
        response = r.get(self.url + '/get_connections/', cookies=self.cookies)
        return response.json()['connections']

    def get_connection_requests(self):
        if self.debug:
            print("Getting connection requests")
        response = r.get(self.url + '/get_connection_requests/', cookies=self.cookies)
        return response.json()['connectionRequests']

    def get_messages(self, conversationId, amount, before):
        if self.debug:
            print("Getting messages")
        if before:
            self.socket.emit('get_messages', {'conversationId': conversationId, 'amount': amount, 'fresh': False, 'before': before})
        else:
            self.socket.emit('get_messages', {'conversationId': conversationId, 'amount': amount, 'fresh': True})

    def request_connection(self, nickname: str):
        if self.debug:
            print("Requesting connection")
        self.socket.emit('request_connection', {'nickname': nickname})

    def accept_request(self, userid):
        self.socket.emit('accept_connection', {'userId': userid})


# client.connect('http://127.0.0.1:8080/', headers={'Cookie': f'session={session}'})
# a = r.post('http://127.0.0.1:8080/login', data={'email': 'admin', 'password':'admin'})


class LoginDialog(QtWidgets.QDialog):
    def __init__(self, mainWindow):
        super(LoginDialog, self).__init__()
        uic.loadUi('loginDialog.ui', self)
        self.show()
        # QPushButton.conn
        self.loginButton.clicked.connect(self.login)
        self.signupButton.clicked.connect(self.signup)
        self.domain = self.domainTextField.toPlainText()
        self.mainWindow = mainWindow
        self.client = Client(self.mainWindow, url=self.domain, debug=True)  # TODO change
        self.loginTextField.setPlainText('testy')
        self.passwordLineEdit.setText('testy')
        self.loginTextField.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.loginTextField and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Tab):
                self.passwordLineEdit.setFocus()
                return True
        return super().eventFilter(obj, event)

    def login(self) -> None:
        self.statusLabel.setText('Logging in...')
        self.domain = self.domainTextField.toPlainText()
        login = self.loginTextField.toPlainText()
        password = self.passwordLineEdit.text()
        result = self.client.login(login, password)
        if not result:
            self.statusLabel.setText('Failed to authenticate')
            return
        self.mainWindow.id = result
        result = self.client.connect()
        if not result:
            self.statusLabel.setText('Failed to connect socket server')
            return
        self.statusLabel.setText('Connected')
        self.mainWindow.client = self.client
        self.mainWindow.logged()
        self.mainWindow.activateWindow()
        self.accept()

    def signup(self) -> None:
        self.statusLabel.setText('Signing up...')
        self.domain = self.domainTextField.toPlainText()
        login = self.loginTextField.toPlainText()
        password = self.passwordLineEdit.text()
        result = self.client.signup(login, password)
        if not result:
            self.statusLabel.setText('Failed to sign up')
            return
        self.statusLabel.setText('Signed up!')


class AddDialog(QDialog):
    def __init__(self, client):
        super(AddDialog, self).__init__()
        uic.loadUi('addConnectionDialog.ui', self)
        self.show()
        self.client = client
        self.sendButton.clicked.connect(self.send)
        self.nicknameTextField.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.nicknameTextField and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.send()
                return True
        return super().eventFilter(obj, event)

    def send(self):
        nickname = self.nicknameTextField.toPlainText()
        self.client.request_connection(nickname)
        self.accept()


class RequestsDialog(QDialog):
    def __init__(self, client, connection_requests):
        super(RequestsDialog, self).__init__()
        uic.loadUi('requestsDialog.ui', self)
        self.show()
        self.client = client
        self.connection_requests = connection_requests

        self.acceptButton.clicked.connect(self.requestsAccept)

        self.buildList()

    def requestsAccept(self):
        print(self.requestsList.selectedItems())
        if self.requestsList.selectedItems():
            for selected in self.requestsList.selectedItems():
                self.client.accept_request(selected.userid)
        self.accept()

    def newRequest(self, connection_request):
        self.connection_requests.append(connection_request)
        item = QListWidgetItem(connection_request['nickname'])
        item.userid = connection_request['id']
        self.requestsList.insertItem(0, item)

    def buildList(self):
        for connection_request in self.connection_requests:
            item = QListWidgetItem(connection_request['nickname'], self.requestsList)
            item.userid = connection_request['id']


class UiClass(QtWidgets.QMainWindow):
    def __init__(self):
        super(UiClass, self).__init__()
        uic.loadUi('client.ui', self)
        self.show()
        self.myNickname.setText('Not logged')
        self.chatNickname.setText('None')
        self.messageTextField.setPlainText('')
        self.loginDialog = LoginDialog(self)
        self.client = None
        self.addDialog = None
        self.requestsDialog = None
        self.isLogged = False
        self.id = 0
        self.messages = {}
        self.noneChat = {'nickname': 'None', 'id': 0, 'conversationId': 0}
        self.activeChat = self.noneChat
        self.connections = []
        self.messageTextField.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.messageTextField and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.sendMessage()
                return True
        return super().eventFilter(obj, event)

    def logged(self):
        self.myNickname.setText(self.client.nickname)
        self.addConnectionButton.clicked.connect(self.requestConnection)
        self.logoutButton.clicked.connect(self.logout)
        self.connectionRequestsButton.clicked.connect(self.requests)
        self.removeConnectionButton.clicked.connect(self.removeConnection)
        self.connection_requests = self.client.get_connection_requests()
        self.connectionsList.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.messageSendButton.clicked.connect(self.sendMessage)
        self.isLogged = True
        self.connections = self.getConnections()
        self.buildConnections(self.connections)
        # QListView

    def requestConnection(self):
        if self.addDialog:
            self.addDialog.show()
            self.addDialog.activateWindow()
        else:
            self.addDialog = AddDialog(self.client)

    def removeConnection(self):
        print(self.client.get_connections())

    def logout(self, close=False):
        if not self.isLogged:
            return
        if self.client:
            self.client.disconnect()
        self.addConnectionButton.clicked.connect(self.noAction)
        self.connectionRequestsButton.clicked.connect(self.noAction)
        self.removeConnectionButton.clicked.connect(self.noAction)
        self.messageSendButton.clicked.connect(self.noAction)
        self.myNickname.setText('Not Logged')
        self.chatNickname.setText('None')
        self.isLogged = False
        self.connectionsList.clear()
        if self.addDialog:
            self.addDialog.close()
        if self.requestsDialog:
            self.requestsDialog.close()
        if not close:
            self.loginDialog.show()
            self.loginDialog.activateWindow()

    def closeEvent(self, event):
        self.logout(True)
        self.loginDialog.close()
        return super(UiClass, self).closeEvent(event)

    def requests(self):
        self.connection_requests = self.client.get_connection_requests()
        if self.requestsDialog:
            self.requestsDialog.show()
            self.requestsDialog.activateWindow()
        else:
            self.requestsDialog = RequestsDialog(self.client, self.connection_requests)

    def getConnections(self):
        return self.client.get_connections()

    def buildConnections(self, connections):
        for connection in connections:
            item = QListWidgetItem(connection['nickname'], self.connectionsList)
            item.connection = connection

    def addConnection(self, connection):
        self.connections.append(connection)
        self.buildConnections([connection])

    def getMessages(self, conversationId, amount=15, before=None):
        self.client.get_messages(conversationId, amount, before)

    def loadMore(self):
        if self.chatList.item(2):
            self.getMessages(self.activeChat['conversationId'], 15, self.chatList.item(2).message['id'])

    def addMessages(self, messages):
        if messages['conversationId'] == self.activeChat['conversationId'] and messages['messages']:
            messages['messages'].reverse()
            if not self.messages.get('conversationId', None):
                self.messages['conversationId'] = messages['messages']
            else:
                for message in messages['messages']:
                    self.messages['conversationId'].append(message)

            self.buildMessages(messages['messages'])
        else:
            self.chatList.item(0).setText("NO MORE TO LOAD")

    def newMessage(self, content, alignment, date=time.time()):
        content = self.overflowMessageCheck(content)
        item = QListWidgetItem(content)
        item.setTextAlignment(alignment)
        item2 = QListWidgetItem(time.strftime("%H:%M:%S %d/%m/%Y", time.localtime(date)))
        item2.setTextAlignment(alignment)
        item3 = QListWidgetItem('')
        # self.chatList.addItem(item3)
        self.chatList.addItem(item2)
        self.chatList.addItem(item)
        self.chatList.scrollToItem(item, True)
        return item

    def sendMessage(self):
        content = self.messageTextField.toPlainText()
        if content == '':
            self.loadMore()
            return
        content = content.strip()
        if not content:
            return
        self.client.send_message(content, recipient=self.activeChat['id'])
        self.messageTextField.setPlainText('')
        item = self.newMessage(content, 2)
        self.chatList.scrollToItem(item, True)

    def itemDoubleClicked(self, item):
        self.changeChat(item.connection)

    def changeChat(self, connection):
        conversationId = connection.get('conversationId', 0)
        self.chatList.clear()
        if not conversationId:
            self.activeChat = self.noneChat
            self.chatNickname.setText('None')
            return
        else:
            item = QListWidgetItem('LOAD MORE')
            item.setTextAlignment(4)
            self.chatList.insertItem(0, item)
            self.activeChat = connection
            self.chatNickname.setText(connection['nickname'])
            messages = self.messages.get(conversationId, [])
            if messages:
                self.buildMessages(messages)
            else:
                self.getMessages(conversationId)

    def overflowMessageCheck(self, content):
        content = content.split(' ')
        newContent = []
        for word in content:
            if len(word) > 65:
                word = word[:65] + ' ' + word[65:]
                word = self.overflowMessageCheck(word)
            newContent.append(word)
        newContent = ' '.join(newContent)
        return newContent

    def buildMessages(self, messages):
        messages.reverse()
        for message in messages:
            content = self.overflowMessageCheck(message['content'])
            item = QListWidgetItem(content)
            item.message = message
            item2 = QListWidgetItem(time.strftime("%H:%M:%S %d/%m/%Y", time.localtime(message['date'])))
            item2.message = message
            item3 = QListWidgetItem('')
            if message['authorId'] != self.id:
                item.setTextAlignment(1)
                item2.setTextAlignment(1)
            else:
                item.setTextAlignment(2)
                item2.setTextAlignment(2)
            self.chatList.insertItem(1, item)
            self.chatList.insertItem(1, item2)
            # self.chatList.insertItem(1, item3)

    def noAction(self):
        pass


app = QtWidgets.QApplication(sys.argv)
win = UiClass()
app.exec_()
