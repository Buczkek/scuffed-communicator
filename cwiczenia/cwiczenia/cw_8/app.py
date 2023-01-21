from crypt import methods
from operator import or_
from flask import Flask, render_template, request, redirect, url_for
from flask_login import UserMixin, login_user, LoginManager, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import yaml

app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

def load_file(name: int):
    with open(str(name) + '.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print(data)
        return data

def save_file(name, ans):
    with open(str(name) + 'odp.yaml', 'w') as f:
        yaml.dump(ans.to_dict(), f)





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup/')
def signup():
    return render_template('signup.html')

@app.route('/signup/', methods=['POST'])
def signupPost():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter(or_(User.email==email, User.name==name)).first()
    if not user and len(password) > 4:
        user = User(email=email, name=name, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return redirect(url_for('signup'))

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/login/', methods=['POST'])
def loginPost():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for('test'))
    return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/test/')
@login_required
def test():
    return f'{current_user.name} + {current_user.email} + {current_user.password}'

@app.route('/edit')
@login_required
def edit():
    return render_template('edit.html', email=current_user.email, name=current_user.name)

@app.route('/edit', methods=['POST'])
def editPost():
    email = request.form.get('email')
    if email != current_user.email:
        current_user.email = email
        db.session.commit()
        
    name = request.form.get('name')
    if name != current_user.name:
        current_user.name = name
        db.session.commit()
    password = request.form.get('password')
    if not check_password_hash(current_user.password, password):
        current_user.password = generate_password_hash(password)
        db.session.commit()
        
    print(email, name, password)
    return redirect(url_for('test'))



@app.route("/<int:name>", methods=['GET', 'POST'])
@login_required
def index(name):
    if request.method == 'POST':
        ans = request.form
        save_file(name, ans)
        return ans

    elif request.method == 'GET':
        data = load_file(name)
        return render_template("index.html", questions=data)


@app.route("/ok")
@login_required
def ansOk():
    return "OK!"


@app.route("/err")
@login_required
def ansErr():
    return "Error!"


@app.route('/result/')
@login_required
def result():
    return request.args.get('msg')


if __name__ == "__main__":
    app.config['SECRET_KEY'] = 'PoBmvPxpuMi4TAwixVB4d6A8FwcsZp96'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    
    login_manager.login_view = 'login'
    login_manager.init_app(app)
    
    db.init_app(app)
    db.create_all(app=app)
    
    app.run(port=5000)