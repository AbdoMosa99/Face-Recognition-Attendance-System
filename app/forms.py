from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp
from flask_wtf.file import FileField, FileRequired, FileAllowed


class AttendanceForm(FlaskForm):
    course_code = StringField(label = "Course Code",
                              validators = [DataRequired(), Length(max=10)],
                              render_kw = {"placeholder": "CS101", "maxlength": "10",
                                          "pattern": "^[A-Z]{2}\d{3}$"})
    
    lecture_number = IntegerField(label = "Lecture Number",
                                  validators = [DataRequired(), NumberRange(min=1, max=30)],
                                  render_kw = {"placeholder": "2", "maxlength": "2",
                                               "pattern": "^\d+$"})
    
    uploaded_file = FileField(label = "Face Image",
                              validators=[FileRequired(), 
                                          FileAllowed(['jpg', 'png'], 'Images only!')],
                             render_kw = {"accept": "image/png, image/jpeg"})
    

    
class RegistrationForm(FlaskForm):
    full_name = StringField(label = "Full Name",
                            validators = [DataRequired(), Length(max=100)],
                            render_kw = {"placeholder": "Mike Smith",
                                        "pattern": "^(\w+)(\s\w+)*$"})
    
    student_id = IntegerField(label = "Student ID",
                              validators = [DataRequired(), NumberRange(min=1)],
                              render_kw = {"placeholder": "151072", "pattern": "^\d+$"})
    
    gender = SelectField(label = "Gender",
                        validators = [DataRequired()],
                        choices = [("M", "Male"), ("F", "Female")])
    
    email = StringField(label = "Email",
                       validators = [DataRequired(), 
                                     Regexp(regex = "^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")],
                       render_kw = {"placeholder": "mikeSmith@example.com"})
    
    university_name = SelectField(label = "University", validators = [DataRequired()])
    
    faculty_name = SelectField(label = "Faculty", validators = [DataRequired()])
    
    courses_codes = StringField(label = "Courses",
                       validators = [DataRequired(), Regexp(regex = "^(\w+)(,\w+)*$")],
                       render_kw = {"placeholder": "SE301,CS381,CS352",
                                   "pattern": "^(\w+)(,\w+)*$"})
    
    uploaded_file = FileField(label = "Face Image",
                              validators = [FileRequired(), 
                                            FileAllowed(['jpg', 'png'], 'Images only!')],
                             render_kw = {"accept": "image/png, image/jpeg"})
    
    
class LoginForm(FlaskForm):
    username = StringField(label= "Username",
                           validators=[DataRequired(), Length(max=255)],
                          render_kw = {"pattern": "^(?=.{4,255}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"})
    
    password = PasswordField(label=('Password'),
                             validators=[DataRequired(), Length(min=8, max=255)])
    