from flask_sqlalchemy import SQLAlchemy
from Code import app

db = SQLAlchemy(app)

class Admin(db.Model):
    username = db.Column(db.String(45), nullable=False, primary_key=True)
    hashpass = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return 'admin %r created' % username
    
class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    
    def __repr__(self):
        return 'University %r created' % name
