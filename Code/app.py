from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'

from models import *
from views import *
   
if __name__ == '__main__':
    app.run()
    