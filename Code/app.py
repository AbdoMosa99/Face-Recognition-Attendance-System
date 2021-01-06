from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'

db = SQLAlchemy(app)
api = Api(app)

from models import *
from views import *
from api import *

if __name__ == '__main__':
    app.run(DEBUG=True)
    