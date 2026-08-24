from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash
from app.models import User, db
from app.forms import LoginForm

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def show_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password.", "error")
            return render_template("login.html", form=form)

        login_user(user)
        return redirect(url_for("home.show_home"))

    return render_template("login.html", form=form)

def create_demo_user():

    email = "alex@example.com"

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        print("Demo user already exists.")
        return

    demo_user = User(
        email=email,
        name="Alex Morgan",
        password=generate_password_hash("Test123!"),
        password_changed=False
    )

    db.session.add(demo_user)
    db.session.commit()

    print("Demo user created!")
    
@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.show_login"))