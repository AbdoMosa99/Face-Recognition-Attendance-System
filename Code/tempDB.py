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
    
                
        
        
        