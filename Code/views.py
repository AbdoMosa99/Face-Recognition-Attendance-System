from flask import render_template, redirect, session, request
from app import app
from models import *

@app.route('/', methods=['GET', 'POST'])
def index():
    if (request.method == 'POST'):
        if request.files:
            image = request.files["UploadImg"]
            print(image)
            return redirect(request.url)
        else:
            print("no files uploaded")
    else:
        return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if (request.method == 'POST'):
        pass
    else:
        return render_template("register.html")

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template("admin.html")
