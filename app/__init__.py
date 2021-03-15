from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


# create and configure the application
app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# link database and admin
db = SQLAlchemy(app)
admin = Admin(app)

# set up the api 
from app.api import Registration, Attendance
api = Api(app)
api.add_resource(Attendance, '/api/attendance')
api.add_resource(Registration, '/api/registration')

# collect all code
from app import models
from app import views
from app import api

# create the admin views
admin.add_view(ModelView(models.Student, db.session))
admin.add_view(ModelView(models.Doctor, db.session))
admin.add_view(ModelView(models.Course, db.session))
admin.add_view(ModelView(models.UniversityFaculty, db.session))
admin.add_view(ModelView(models.Attendance, db.session))
admin.add_view(ModelView(models.Log, db.session))
