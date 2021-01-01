from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
app.config['DEBUG'] = True

db = SQLAlchemy(app)

from models import *
from views import *
   
if __name__ == '__main__':
    app.run()
    