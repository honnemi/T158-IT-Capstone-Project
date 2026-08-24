from flask import Blueprint, render_template

bookings_bp = Blueprint("bookings", __name__)

@bookings_bp.route("/flights")
def show_flights():
    return render_template("flights.html")

@bookings_bp.route("/accommodations")
def show_accommodations():
    return render_template("accommodations.html")

@bookings_bp.route("/other")
def show_other():
    return render_template("other.html")

