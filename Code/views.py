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
            main()
            img = request.files["UploadImg"]
            img = convertImg(img)
            res = analyze(img)
            if res:
                flash(f'Hey {res}! You have successfuly been submited.')
                return redirect('/')
            else:
                flash(f'Sorry! We couldn\'t identify you.')
                return redirect('/')
        else:
            flash(f'No imges were uploaded!')
            return redirect('/')
    else:
        return render_template("index.html")

uid = 1
@app.route('/register', methods=['GET', 'POST'])
def register():
    global uid
    if (request.method == 'POST'):
        fullname = request.form['fullname'] 
        # gender = request.form['gender'] # can't because it's not an input
        email = request.form['email'] 
        # university = request.form['university'] 
        # faculty = request.form['faculty']
        courses = request.form['courses']
        img = request.files["uploadImg"]
        img = convertImg(img)
        enc = getEncodings(img)
        
        e = models.FaceEncoding(id=uid, encoding=str(enc))
        s = models.Student(id=uid, name=fullname, gender="M", email=email, face_enc_id=uid, fac_uni_id=uid)
        models.db.session.add(e)
        models.db.session.add(s)
        models.db.session.commit()
        print(models.FaceEncoding.query.all())
        print(models.Student.query.all())
        uid += 1
        return "Success"
        
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








