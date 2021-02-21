# Tasks

### Web Front End
* Create an HTML page that have 
  * 3 links in nav bar (home, register, admin)
  * in home, we need the functionality to upload a picture and analyse it
  * in home, there are 3 elements (upload button, url text field, open camera button)
  * Home page should be something like [this](https://imgbb.com/)
  * register page should have a form containig (Full Name, DoctorID, and more)
  * admin page should ask you to login and then provide you with data grid of the database

* Use any framework like (Vue, Bootstrap, etc) to complete the website fast
* Use JavaScript to validate inputs

### Back End
* Python Face Recognition (dir: Code) done
  * find a library for face detection and code how it should be used
  * find a library for face recognition 
  * test it against sample pictures
* Database DB.sql (dir: DB)
  * faculty table (id, name, university)
  * students table (name, id, doctorId, facultyId, etc)
  * doctors table (name, id, etc)
  * courses table (id, name, semester, doctorId, etc)
  * Attendance (id, time, studentId, courseId, etc)
  * logs
  * add DBCredentials.txt
* API
  * make an API that handles requests to the main features
  * provide logs
* Make the actual backend using flask 

### Documentation
* ReadMe1st.txt
  * the steps of deploying and running the project
* ProjectDocument.docx
  * preface
  * introduction
  * glossary
  * user requirment definition
  * system architecture
  * system requirments specification
  * system models
  * system evolution
  * appendices
  * index
* Demo.mp4
  * how is the running of your code commented by your voice
* Presentation.pptx
  * Agenda
  * Introduction
  * Problem Definition
  * Problem Description
  * Used Components.
  * Cost.
  * Used Programming Language, IDEs, and any other used tools.
  * Core Source Code.
  * Execution Result.
  * A video showing how to operate and run the project.
  * Future Vision of the project.
  * References (URLs, Books, …etc.).


### Current Tasks
* Database
* login and registration
* form.html + message.html
* full admin pannel + search 
* Front End modifications
* backend validation
* frontend validation with js
* testing all along

* manytomany relationships should refer to the original objects themselves?
* add Comments 

### Notes 
* to activate the env from the code directory 'env\Scripts\activate'
* to run the server 'flask run'
* run flask in debug mode 'set FLASK_ENV=development'
* debugging numpy problem 'pip install numpy==1.19.3'
* install all packages needed 'pip install -r requirements.txt'


# create database
from models import db
db.create_all()

# hash a password
from argon2 import PasswordHasher
ph = PasswordHasher()
hash = ph.hash("Mosa1234")

# add an admin
from models import Admin
from models import db
admin = Admin(username="Mosa99", hashpass=hash)
db.session.add(admin)
db.session.commit()

# Query the Admin and check success
Admin.query.all()

# check pass
ph.verify(hash, "Mosa1234")
    
  
  