from flask import render_template
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template("admin.html")
