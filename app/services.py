def reset_db():
    import os
    file_path = "DB.db"
    if os.path.exists(file_path):
        os.remove(file_path)
    print("old db removed.")
    
    from app import db
    db.create_all()
    print("new db created.")
    
    from app import models
    f1 = models.Faculty(name="FCI")
    f2 = models.Faculty(name="Engineering")
    u1 = models.University(name="Suez")
    u2 = models.University(name="Suez Canal")
    db.session.add(f1)
    db.session.add(f2)
    db.session.add(u1)
    db.session.add(u2)
    
    fu1 = models.UniversityFaculties(university=u1, faculty=f1)
    db.session.add(fu1)
    
    db.session.commit()
    print("added default records to db.")