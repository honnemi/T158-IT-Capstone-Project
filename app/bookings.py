from flask import Blueprint, render_template
from flask_login import login_required

bookings_bp = Blueprint("bookings", __name__)

@bookings_bp.route("/flights", methods=["GET", "POST"])
@login_required
def show_flights():
    return render_template("flights.html")

@bookings_bp.route("/accommodations", methods=["GET", "POST"])
@login_required
def show_accommodations():
    return render_template("accommodations.html")

@bookings_bp.route("/other", methods=["GET", "POST"])
@login_required
def show_other():
    return render_template("other.html")

