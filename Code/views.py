from flask import render_template, redirect, url_for, session, request, g, flash, Response
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
            course_code = request.form['courseCode']
            lec_n = request.form['lectureNUM']
            file = request.files["UploadImg"]
            
            
            img = file2RGB(file)
            res = analyze(img)
            if res:
                x = models.addAttendance(lec_n, course_code, res.id)
                if not x:
                    return redirect('/error')
                
                flash(f'Hey {res.name}! You have successfuly been submited.')
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
        id = request.form['studentid']
        fullname = request.form['fullname'] 
        gender = request.form['gender']
        email = request.form['email'] 
        university = request.form['university']
        faculty = request.form['faculty']
        courses = request.form['courses']
        file = request.files['uploadImg']
        
        img = file2RGB(file)
        enc = getEncoding(img)
        courses = courses.split(',')
        
        s = models.addStudent(id, fullname, gender, email, university, faculty, courses, str(enc.tolist()))
        if not s:
            return redirect('/error')
        return f"Student {fullname} Added Successfully"
        
    return render_template("register.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camfeed')
def camfeed():
    return render_template("camfeed.html")



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
    if g.user:
        return redirect('/data')
    return render_template("admin.html")


@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        pass
    if g.user:
        return render_template("data.html")
    return redirect('/admin')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/data/students')
def displayStudents():
    if g.user:
        table = models.getStudents()
        return render_template("data.html", table=table)
    return redirect('/admin')

@app.route('/data/faculties')
def displayFaculties():
    if g.user:
        table = models.getFaculties()
        return render_template("data.html", table=table)
    return redirect('/admin')

@app.route('/data/doctors')
def displayDoctors():
    if g.user:
        table = models.getDoctors()
        return render_template("data.html", table=table)
    return redirect('/admin')

@app.route('/data/courses')
def displayCourses():
    if g.user:
        table = models.getCourses()
        return render_template("data.html", table=table)
    return redirect('/admin')

@app.route('/data/attendance')
def displayAttendance():
    if g.user:
        table = models.getAttendance()
        return render_template("data.html", table=table)
    return redirect('/admin')

@app.route('/data/logs')
def displayLogs():
    if g.user:
        table = models.getLogs()
        return render_template("data.html", table=table)
    return redirect('/admin')
