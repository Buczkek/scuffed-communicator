from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, make_response


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventary.db'
db = SQLAlchemy(app)
api = Api(app)
parser = reqparse.RequestParser()

if __name__ == '__main__':
    app.run(debug=True)
