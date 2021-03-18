from flask import render_template, redirect, url_for, session, g, request, flash
import requests

from app import app, models, bcrypt
from app.forms import AttendanceForm, RegistrationForm


# Home Route
@app.route("/", methods=["GET", "POST"])
def index():
    form = AttendanceForm()
    
    # For Post Request: Submitting an attendance
    if request.method == "POST" and form.validate():
        # using the attendance API 
        response = requests.post("http://127.0.0.1:5000/api/attendance",
                                 request.form, files=request.files)

        flash(response.json()["message"])  
        return redirect(url_for("/", form=form))
    
    # For Get Request: Opening home page
    return render_template("index.html", form=form)


# Registration Route
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    
    # For Post Request: Submitting the registration form
    if request.method == "POST" and form.validate():
        # using the registration API 
        response = requests.post("http://127.0.0.1:5000/api/registration",
                                 request.form, files=request.files) 
        
        flash(response.json()["message"])
        return redirect('/')
    
    # For Get Request: Opening registration form
    universities = models.University.query.all()
    universities_list = [(u.id, u.name) for u in universities]
    form.university_id.choices = universities_list
    
    faculties = models.Faculty.query.all()
    faculties_list = [(f.id, f.name) for f in faculties]
    form.faculty_id.choices = faculties_list
    
    return render_template("register.html", form=form)

