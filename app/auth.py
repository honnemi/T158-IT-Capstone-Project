from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash
from app.models import User, db
from app.forms import LoginForm, ResetPasswordForm

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def show_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password.", "error")
            return render_template("login.html", form=form)

        if user.password_changed == False:
            return redirect(url_for("auth.reset_password", user_id=user.id))

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

    
@auth_bp.route("/reset-password/<int:user_id>", methods=["GET", "POST"])
def reset_password(user_id):
    form = ResetPasswordForm()

    user = db.session.get(User, user_id)

    if form.validate_on_submit():
        if user.check_password(form.new_password.data):
            flash("You must not re-use your existing password.", "error")
            return render_template("reset-password.html", form=form)


        user.password = generate_password_hash(form.new_password.data)

        user.password_changed = True

        db.session.commit()

        login_user(user)

        flash("Password updated successfully!", "success")
        return redirect(url_for("auth.show_login"))

    return render_template("reset-password.html", form=form)