from flask import render_template, redirect, url_for, session, g, request, flash
import requests

from app import app, models, bcrypt
from app.forms import AttendanceForm


# Home Route
@app.route("/", methods=["GET", "POST"])
def index():
    form = AttendanceForm()
    
    # For Post Request: Submitting an attendance
    if (request.method == "POST"):
        if form.validate_on_submit():
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
    # For Post Request: Submitting the registration form
    if (request.method == "POST"):
        # using the registration API 
        response = requests.post("http://127.0.0.1:5000/api/registration",
                                 request.form, files=request.files) 
        
        flash(response.json()["message"])
        return redirect('/')
    
    # For Get Request: Opening registration form
    universities = models.University.query.all()
    faculties = models.Faculty.query.all()
    return render_template("register.html",
                           universities = universities, 
                           faculties = faculties)


# Admin Login
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    # For Post Request: Submitting the login form
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # get that admin from db if exists
        user = models.Admin.query.filter(models.Admin.username == username).first()

        # check credentials
        if user and ph.verify(user.hashpass, password):
            session["username"] = username # keep logged in
            return redirect(url_for("admin_panel"))
        else:
            flash("Wrong username or password!")
            return redirect(url_for("admin_login"))
    
    # For Get Request: Opening login form
    return render_template("admin_login.html")


# Admin Logout
@app.route('/admin_logout')
def admin_logout(): 
    session.pop('username', None)
    return redirect(url_for('admin_login'))


# ** Supposed to modify flask_admin etc.
@app.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        pass
    if g.user:
        return render_template("data.html")
    return redirect('/admin')
