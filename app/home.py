from flask import Blueprint, render_template
from flask_login import login_required

home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET", "POST"])
@login_required
def show_home():
    return render_template("home.html")
