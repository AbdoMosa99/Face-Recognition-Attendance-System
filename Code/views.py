from flask import render_template, redirect, session, request
from app import app
import models
from face_recog import *

@app.route('/', methods=['GET', 'POST'])
def index():
    if (request.method == 'POST'):
        if request.files:
            main()
            img = request.files["UploadImg"]
            img = convertImg(img)
            res = analyze(img)
            if res:
                return "Success!"
            else:
                return "Failed to identify"
        else:
            return "No files uploaded"
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
        
    else:
        return render_template("register.html")

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template("admin.html")
