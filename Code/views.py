from flask import render_template, redirect, url_for, session, request, g, flash
from argon2 import PasswordHasher
from app import app
import models
from face_recog import *


@app.before_request
def before_request():
    g.user = None
    users = models.Admin.query.all()
    if 'username' in session:
        for user in users:
            if user.username == session['username']:
                g.user = user

@app.route('/', methods=['GET', 'POST'])
def index():
    if (request.method == 'POST'):
        if request.files:
            img = request.files["UploadImg"]
            img = file2RGB(img)
            res = analyze(img)
            if res:
                flash(f'Hey {res}! You have successfuly been submited.')
                return redirect('/')
            else:
                flash(f'Sorry! We couldn\'t identify you.')
                return redirect('/')
        else:
            flash(f'No images were uploaded!')
            return redirect('/')
    else:
        return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if (request.method == 'POST'):
        fullname = request.form['fullname'] 
        # gender = request.form['gender'] # can't because it's not an input
        email = request.form['email'] 
        # university = request.form['university'] 
        # faculty = request.form['faculty']
        courses = request.form['courses']
        file = request.files["uploadImg"]
        img = file2RGB(file)
        enc = getEncoding(img)
        
        models.addStudent(fullname, "M", email, "Suez", "FCI", courses, str(face_enc.tolist()))
        flash(fullname)
        return f"Student {fullname} Added Successfully"
        
    return render_template("register.html")

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        session.pop('username', None)
        
        username = request.form['username']
        password = request.form['password']
        
        ph = PasswordHasher()        
        users = models.Admin.query.all()
        
        for user in users:
            if user.username == username:
                try:
                    if ph.verify(user.hashpass, password):
                        session['username'] = username
                        return redirect('/data')
                except:
                    return "Wrong password!"
            return "Wrong Username!"
                
    return render_template("admin.html")


@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        pass
    if g.user:
        return render_template("data.html")
    return redirect('/admin')








