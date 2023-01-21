import yaml
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from yaml import *

app = Flask(__name__)


def load_file(name: str):
    with open(name + '.yaml') as f:
        file = yaml.load(f, Loader=yaml.FullLoader)
        print(file)
        return file['q']



@app.route("/<string:name>", methods=['GET', 'POST'])
def index(name):
    data = [
        {'q': 'Jaki to framework', 'o': ['Django', 'Flask', 'Inny'], 'a': 'Flask'},
        {'q': 'Pytanie', 'a': 'Odpowiedz'},
    ]
    if request.method == 'POST':
        ans = request.form
        err = False
        for qnr, a in ans.items():
            if a != data[int(qnr)].get('a'):
                err = True
        if err:
            return redirect(url_for("result", msg='err'))
        else:
            return redirect(url_for("result", msg='ok'))
    elif request.method == 'GET':
        data = load_file(name)
        return render_template("index.html", questions=data)


@app.route("/ok")
def ansOk():
    return "OK!"


@app.route("/err")
def ansErr():
    return "Error!"


@app.route('/result/')
def result():
    return request.args.get('msg')


if __name__ == "__main__":
    app.run(debug='True')
