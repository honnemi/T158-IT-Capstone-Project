from datetime import date

from flask import Blueprint, render_template
from flask_login import login_required, current_user

home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET", "POST"])
@login_required
def show_home():
    user_trips = current_user.trips
    return render_template("home.html", user_trips=user_trips, current_date=date.today())
