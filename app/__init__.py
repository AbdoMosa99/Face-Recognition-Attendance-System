from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
from app.api import Registration, Attendance
api = Api(app)
admin = Admin(app)
api.add_resource(Attendance, '/api/attendance')
api.add_resource(Registration, '/api/registration')

from app import models
from app import views
from app import api

admin.add_view(ModelView(models.Student, db.session))
admin.add_view(ModelView(models.Doctor, db.session))
admin.add_view(ModelView(models.Course, db.session))
admin.add_view(ModelView(models.UniversityFaculty, db.session))
admin.add_view(ModelView(models.Attendance, db.session))
admin.add_view(ModelView(models.Log, db.session))
