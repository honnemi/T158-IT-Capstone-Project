from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from app.models import Trip

bookings_bp = Blueprint("bookings", __name__)


@bookings_bp.route("/flights/<int:trip_id>", methods=["GET", "POST"])
@login_required
def show_flights(trip_id):

    trip = Trip.query.get_or_404(trip_id)

    if current_user not in trip.users:
        abort(403)

    return render_template(
        "flights.html",
        trip=trip
    )


@bookings_bp.route("/accommodations/<int:trip_id>", methods=["GET", "POST"])
@login_required
def show_accommodations(trip_id):

    trip = Trip.query.get_or_404(trip_id)
    
    if current_user not in trip.users:
        abort(403)

    return render_template(
        "accommodations.html",
        trip=trip
    )


@bookings_bp.route("/other/<int:trip_id>", methods=["GET", "POST"])
@login_required
def show_other(trip_id):

    trip = Trip.query.get_or_404(trip_id)
    
    if current_user not in trip.users:
        abort(403)

    return render_template(
        "other.html",
        trip=trip
    )