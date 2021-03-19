from flask_admin import AdminIndexView, expose
from flask import session, redirect, url_for, render_template, request, flash
from app import models, bcrypt
from app.forms import LoginForm
from app.services import add_log


class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        authenticated = 'username' in session
        if not authenticated:
            return redirect(url_for('.login_view'))
        
        return super(MyAdminIndexView, self).index()

    
    @expose('/login', methods=('GET', 'POST'))
    def login_view(self):
        form = LoginForm()
        
        # For Post Request: Submitting the login form
        if request.method == "POST" and form.validate():
            try:
                username = request.form["username"]
                password = request.form["password"]

                # get that admin from db if exists
                user = models.Admin.query.filter(models.Admin.username == username).one()

                # check credentials
                authenticated = bcrypt.check_password_hash(user.password_hash, password)
                if not authenticated:
                    raise Exception(f"Wrong Password From <{username}>")
                    
                session["username"] = username # keep logged in
                add_log(f"{username} has successfully logged in.")
                return redirect(url_for(".index"))
            except Exception as e:
                add_log(f"There has been a failed attempt of login with the exception {e}.")
                flash("Wrong username or password!")
                return redirect(url_for('.login_view'))

        # For Get Request: Opening login form
        return render_template("admin/login.html", form=form)


    @expose('/logout/')
    def logout_view(self):
        add_log(f"{session['username']} has successfully logged out.")
        session.pop('username', None)
        return redirect(url_for('index'))

