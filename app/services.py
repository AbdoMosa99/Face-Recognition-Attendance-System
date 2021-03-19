def reset_db():
    # remove old one
    import os
    file_path = "DB.db"
    if os.path.exists(file_path):
        os.remove(file_path)
    print("old db removed.")
    
    # create a new one
    from app import db
    db.create_all()
    print("new db created.")
    
    # initialize database with some records
    from app import models
    f1 = models.Faculty(name="FCI")
    f2 = models.Faculty(name="Engineering")
    u1 = models.University(name="Suez")
    u2 = models.University(name="Suez Canal")
    db.session.add(f1)
    db.session.add(f2)
    db.session.add(u1)
    db.session.add(u2)
    fu1 = models.UniversityFaculty(university=u1, faculty=f1)
    db.session.add(fu1)
    
    db.session.commit()
    print("added default records to db.")
    
    
def add_admin(username, password):
    # hash the password using bcrypt
    from app import bcrypt
    password_hash = bcrypt.generate_password_hash(password)
    password_hash = password_hash.decode("utf-8")
    
    # add to database
    from app import models, db
    admin = models.Admin(username=username, password_hash=password_hash)
    db.session.add(admin)
    db.session.commit()

    
def add_log(log_message):
    from app import db
    from app.models import Log
    log = Log(activity = log_message)
    db.session.add(log)
    db.session.commit()
    