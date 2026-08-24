from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash
from app.models import User, db
from app.forms import LoginForm

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def show_login():

    form = LoginForm()

    if request.method == "POST":

        if not form.validate():
            print("Errors:", form.errors)
            return render_template("login.html", form=form)

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        print("User found:", user)

        if user is None:
            flash("Invalid email or password.", "error")
            return render_template("login.html", form=form)

        print("Stored password hash:", user.password)

        password_correct = user.check_password(
            form.password.data
        )

        print("Password correct:", password_correct)

        if not password_correct:
            flash("Invalid email or password.", "error")
            return render_template("login.html", form=form)

        login_user(user)

        return redirect(url_for("home.show_home"))

    return render_template("login.html", form=form)

def create_demo_user():

    email = "test@example.com"

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        print("Demo user already exists.")
        return

    demo_user = User(
        email=email,
        name="Test User",
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