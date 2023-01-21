from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, send, emit, disconnect, rooms

import time

app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app)

CONNECTED = {}


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authorId = db.Column(db.Integer)
    conversationId = db.Column(db.Integer)
    isGroup = db.Column(db.Boolean)
    content = db.Column(db.String(1024))
    date = db.Column(db.Float)


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1id = db.Column(db.Integer)
    user2id = db.Column(db.Integer)


class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1id = db.Column(db.Integer)
    user2id = db.Column(db.Integer)
    conversationId = db.Column(db.Integer)


class ConnectionRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1id = db.Column(db.Integer)
    user2id = db.Column(db.Integer)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.request_loader
def load_request(my_request):
    auth = my_request.authorization

    if auth is not None:
        username, password = auth['username'], auth['password']
        user = User.get_by_username(username)
        if user is not None and user.password == password:
            return user
    return None


@socketio.on('connect')
def test_connect():
    print(f"Connected {session} | {request.server}")
    if not session:
        disconnect()
    print(f"{request.sid}")
    print(f"{rooms(request.sid)}")
    CONNECTED[current_user.id] = request.sid
    print(CONNECTED)
    emit('my_message', {'data': 'Connected'})
    emit('my_message', {'data': 'To sidem'}, to=request.sid)


@socketio.on('message')
def handle_message(data):
    print(f'Received message from id: "{current_user.id}" | socketid: {CONNECTED.get(current_user.id, None)}')
    print(CONNECTED)
    print(data)
    recipientId = data['recipient']
    isGroup = data.get('group', False)
    date = time.time()
    content = data['content']
    authorId = current_user.id
    conversation = Conversation.query.filter_by(user1id=recipientId, user2id=authorId).first()
    if not conversation:
        conversation = Conversation.query.filter_by(user1id=authorId, user2id=recipientId).first()
    conversationId = conversation.id
    message = Message(authorId=authorId, isGroup=isGroup, date=date, content=content, conversationId=conversationId)
    db.session.add(message)
    db.session.commit()
    recipientSocketID = CONNECTED.get(recipientId, None)
    if recipientSocketID:
        emit('message',
             {'content': content, 'authorId': authorId, 'conversationId': conversationId, 'group': False, 'date': date},
             to=recipientSocketID)
    print(data)


@socketio.on('get_messages')
def handle_get_messages(data):
    fresh = data.get('fresh', False)
    conversationId = data.get('conversationId')
    if fresh:
        messages = Message.query.filter_by(conversationId=conversationId).order_by(Message.date.desc()).limit(15)
    else:
        before = data.get('before')
        messages = Message.query.filter_by(conversationId=conversationId).filter(Message.id < before).order_by(
            Message.date.desc()).limit(15)

    result = []
    for message in messages:
        result.append({
            'id': message.id,
            'date': message.date,
            'conversationId': message.conversationId,
            'content': message.content,
            'authorId': message.authorId,
            'group': message.isGroup
        })
    print(result)
    emit('messages', {'messages': result, 'conversationId': conversationId})


@socketio.on('accept_connection')
def handle_accept_connection(data):
    print(f"Received connection accept request")
    print(data)
    try:
        print('elo')
        connectingUserId = data['userId']
        acceptingUserId = current_user.id
        connectionRequest = ConnectionRequest.query.filter_by(user1id=connectingUserId).filter_by(
            user2id=acceptingUserId).first()
        assert connectionRequest
        conversation = Conversation.query.filter_by(user1id=connectingUserId, user2id=acceptingUserId).first()
        if not conversation:
            conversation = Conversation.query.filter_by(user1id=acceptingUserId, user2id=connectingUserId).first()
        if not conversation:
            conversation = Conversation(user1id=connectingUserId, user2id=acceptingUserId)
            db.session.add(conversation)
        connection = Connection(user1id=connectingUserId, user2id=acceptingUserId, conversationId=conversation.id)
        ConnectionRequest.query.filter_by(user1id=connectingUserId).filter_by(user2id=acceptingUserId).delete()
        db.session.add(connection)
        db.session.commit()
        emit('success', {'event': 'accept_connection'})
        emit('connection', {'connection': {
            'nickname': User.query.filter_by(id=connectingUserId).first().nickname,
            'id': connectingUserId,
            'conversationId': conversation.id,
        }})
        connectingUserSocketID = CONNECTED.get(connectingUserId, None)
        if connectingUserSocketID:
            emit('connection',
                 {'connection': {
                     'nickname': User.query.filter_by(id=acceptingUserId).first().nickname,
                     'id': acceptingUserId,
                     'conversationId': conversation.id,
                 }},
                 to=connectingUserSocketID)
            # print('sent')

    except:
        emit('failure', {'event': 'accept_connection'})
        print(f"Received corrupted data")


@socketio.on('request_connection')
def handle_request_connection(data):
    print(f"Received connection request")
    print(data)
    try:
        connectingUserId = current_user.id
        nickname = data['nickname']
        user = User.query.filter_by(nickname=nickname).first()
        assert user
        toConnectUserId = user.id
        connectionRequest = ConnectionRequest.query.filter_by(user1id=connectingUserId).filter_by(
            user2id=toConnectUserId).first()
        if connectionRequest:
            emit('failure', {'event': 'request_connection'})
            print('Request already pending')
            return
        connectionRequest = ConnectionRequest.query.filter_by(user2id=connectingUserId).filter_by(
            user1id=toConnectUserId).first()
        if connectionRequest:
            emit('failure', {'event': 'request_connection'})
            print('Request already pending')
            return
        connectionRequest = ConnectionRequest(user1id=connectingUserId, user2id=toConnectUserId)
        db.session.add(connectionRequest)
        db.session.commit()
        emit('success', {'event': 'request_connection'})
        if CONNECTED.get(toConnectUserId, None):
            emit('connection_request', {'nickname': current_user.nickname, 'id': current_user.id})
    except:
        emit('failure', {'event': 'request_connection'})
        print(f"Received corrupted data")


@socketio.on('disconnect')
def handle_disconnect():
    emit('disconnect')
    if session:
        CONNECTED.pop(current_user.id)
    print(f'socketio disconnected')


@app.route('/get_connections/')
@login_required
def handle_get_connections():
    userid = current_user.id
    result = Connection.query.filter_by(user1id=userid)
    connections = []
    for row in result:
        con = row.user2id
        conversation = Conversation.query.filter_by(user1id=userid, user2id=con).first()
        if not conversation:
            conversation = Conversation.query.filter_by(user1id=con, user2id=userid).first()
        conversationId = conversation.id
        connections.append({
            'nickname': User.query.filter_by(id=con).first().nickname,
            'id': con,
            'conversationId': conversationId,
        })

    result = Connection.query.filter_by(user2id=userid)
    for row in result:
        con = row.user1id
        conversation = Conversation.query.filter_by(user1id=userid, user2id=con).first()
        if not conversation:
            conversation = Conversation.query.filter_by(user1id=con, user2id=userid).first()
        conversationId = conversation.id
        connections.append({
            'nickname': User.query.filter_by(id=con).first().nickname,
            'id': con,
            'conversationId': conversationId,
        })
    return {'connections': connections}


@app.route('/get_connection_requests/')
@login_required
def get_connection_requests():
    id = current_user.id
    result = ConnectionRequest.query.filter_by(user2id=id)
    connectionRequests = []
    for row in result:
        con = row.user1id
        connectionRequests.append({
            'nickname': User.query.filter_by(id=con).first().nickname,
            'id': con,
        })

    return {'connectionRequests': connectionRequests}


@app.route('/test/')
@login_required
def test():
    print(session)
    return {'name': current_user.nickname, 'id': current_user.id}


@app.route('/login/', methods=['POST'])
def loginPost():
    nickname = request.form.get('nickname')
    password = request.form.get('password')
    user = User.query.filter_by(nickname=nickname).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return f'{user.id}'
    return '0'


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return 'success'


@app.route('/signup/', methods=['POST'])
def signupPost():
    nickname = request.form.get('nickname')
    password = request.form.get('password')
    if nickname.count(' ') or nickname.count('\n') or nickname.count('\t'):
        return 'failure'
    user = User.query.filter(User.nickname == nickname).first()
    if not user and len(password) > 4:
        user = User(nickname=nickname, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return 'success'
    return 'failure'


if __name__ == "__main__":
    app.config['SECRET_KEY'] = 'vkc"jUK9B5IqYn7=DE5X"{l0>SGp!X'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager.login_view = 'login'
    login_manager.init_app(app)

    db.create_all(app=app)

    app.run(port=8080)
