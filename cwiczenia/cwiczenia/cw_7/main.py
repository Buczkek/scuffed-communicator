import yaml
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from yaml import *

app = Flask(__name__)


def load_file(name: str):
    with open(name + '.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print(data)
        return data


def save_file(name, ans):
    with open(name + 'odp.yaml', 'w') as f:
        yaml.dump(ans.to_dict(), f)


@app.route("/<string:name>", methods=['GET', 'POST'])
def index(name):
    if request.method == 'POST':
        ans = request.form
        save_file(name, ans)
        return ans

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
