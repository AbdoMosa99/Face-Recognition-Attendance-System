from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB/DB.db'

from Code import models
from Code import views
   
if __name__ == '__main__':
    app.run()
    