from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename


class AttendanceForm(FlaskForm):
    course_code = StringField(label = "Course Code",
                              validators = [DataRequired(), Length(max=10)],
                              render_kw = {"placeholder": "CS101"})
    
    lecture_number = IntegerField(label = "Lecture Number",
                                  validators = [DataRequired(), NumberRange(min=1, max=30)],
                                  render_kw = {"placeholder": "2"})
    
    uploaded_file = FileField(label = "Face Image",
                              validators=[FileRequired(), 
                                          FileAllowed(['jpg', 'png'], 'Images only!')])
    

    
class RegistrationForm(FlaskForm):
    full_name = StringField(label = "Full Name",
                            validators = [DataRequired(), Length(max=100)],
                            render_kw = {"placeholder": "Mike Smith"})
    
    student_id = IntegerField(label = "Student ID",
                              validators = [DataRequired(), NumberRange(min=1)],
                              render_kw = {"placeholder": "151072"})
    
    gender = SelectField(label = "Gender",
                        validators = [DataRequired()],
                        choices = [("M", "Mail"), ("F", "Female")])
    
    email = StringField(label = "Email",
                       validators = [DataRequired(), 
                                     Regexp(regex = "^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")],
                       render_kw = {"placeholder": "mikeSmith@example.com"})
    
    university_id = SelectField(label = "University",
                        validators = [DataRequired()])
    
    faculty_id = SelectField(label = "Faculty",
                               validators = [DataRequired()])
    
    courses_codes = StringField(label = "Courses",
                       validators = [DataRequired(), 
                                     Regexp(regex = "^(\w+)(,\w+)*$")],
                       render_kw = {"placeholder": "SE301,CS381,CS352"})
    
    uploaded_file = FileField(label = "Face Image",
                              validators = [FileRequired(), 
                                            FileAllowed(['jpg', 'png'], 'Images only!')])
    
class LoginForm(FlaskForm):
    username = StringField(label= "Username",
                           validators=[DataRequired(), Length(max=255)])
    
    password = PasswordField(label=('Password'),
                             validators=[DataRequired(), Length(min=8, max=255)])
    