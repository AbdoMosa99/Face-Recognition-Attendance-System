from flask_admin import AdminIndexView, expose
from flask import session, redirect, url_for, render_template, request, flash
from app import models, bcrypt

class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        authenticated = 'username' in session
        if not authenticated:
            return redirect(url_for('.login_view'))
        
        return super(MyAdminIndexView, self).index()

    
    @expose('/login', methods=('GET', 'POST'))
    def login_view(self):
        # For Post Request: Submitting the login form
        if request.method == "POST":
            try:
                username = request.form["username"]
                password = request.form["password"]

                # get that admin from db if exists
                user = models.Admin.query.filter(models.Admin.username == username).one()

                # check credentials
                authenticated = bcrypt.check_password_hash(user.password_hash, password)
                if not authenticated:
                    raise Exception("Wrong Password")
                    
                session["username"] = username # keep logged in
                return redirect(url_for(".index"))
            except:
                flash("Wrong username or password!")
                return redirect(url_for('.login_view'))

        # For Get Request: Opening login form
        return render_template("admin/login.html")


    @expose('/logout/')
    def logout_view(self):
        session.pop('username', None)
        return redirect(url_for('index'))

