from collections import defaultdict

from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from app.models import Trip, Flight, Accommodation, Other, Tour, Cruise


bookings_bp = Blueprint("bookings", __name__)


def _get_trip_for_current_user(trip_id):
    """Load a trip and ensure the signed-in user belongs to it."""
    trip = Trip.query.get_or_404(trip_id)

    if current_user not in trip.users:
        abort(403)

    return trip


def _get_booking_data(trip_id):
    """Load every booking type used by the booking pages."""
    flights = (
        Flight.query
        .filter_by(trip_id=trip_id)
        .order_by(Flight.departure_time.asc())
        .all()
    )

    accommodations = (
        Accommodation.query
        .filter_by(trip_id=trip_id)
        .order_by(Accommodation.check_in.asc())
        .all()
    )

    cruises = (
        Cruise.query
        .filter_by(trip_id=trip_id)
        .order_by(Cruise.start_date.asc())
        .all()
    )

    tours = (
        Tour.query
        .filter_by(trip_id=trip_id)
        .order_by(Tour.start_time.asc())
        .all()
    )

    others = (
        Other.query
        .filter_by(trip_id=trip_id)
        .order_by(Other.start_time.asc())
        .all()
    )

    return {
        "flights": flights,
        "accommodations": accommodations,
        "cruises": cruises,
        "tours": tours,
        "others": others,
    }


def _build_booking_timeline(booking_data):
    """Build the left-hand timeline from database booking records."""
    events = []

    for flight in booking_data["flights"]:
        events.append({
            "date": flight.departure_time.date(),
            "sort_time": flight.departure_time,
            "title": f"{flight.departure_airport} → {flight.arrival_airport} Departure",
            "time": flight.departure_time.strftime("%H:%M"),
            "colour": "red",
        })
        events.append({
            "date": flight.arrival_time.date(),
            "sort_time": flight.arrival_time,
            "title": f"{flight.departure_airport} → {flight.arrival_airport} Arrival",
            "time": flight.arrival_time.strftime("%H:%M"),
            "colour": "red",
        })

    for accommodation in booking_data["accommodations"]:
        events.append({
            "date": accommodation.check_in.date(),
            "sort_time": accommodation.check_in,
            "title": f"{accommodation.name} Check-in",
            "time": accommodation.check_in.strftime("%H:%M"),
            "colour": "orange",
        })
        events.append({
            "date": accommodation.check_out.date(),
            "sort_time": accommodation.check_out,
            "title": f"{accommodation.name} Check-out",
            "time": accommodation.check_out.strftime("%H:%M"),
            "colour": "orange",
        })

    for cruise in booking_data["cruises"]:
        events.append({
            "date": cruise.start_date.date(),
            "sort_time": cruise.start_date,
            "title": cruise.name,
            "time": cruise.start_date.strftime("%H:%M"),
            "colour": "purple",
        })

    for tour in booking_data["tours"]:
        events.append({
            "date": tour.start_time.date(),
            "sort_time": tour.start_time,
            "title": tour.name,
            "time": f"{tour.start_time.strftime('%H:%M')}-{tour.end_time.strftime('%H:%M')}",
            "colour": "blue",
        })

    for other in booking_data["others"]:
        events.append({
            "date": other.start_time.date(),
            "sort_time": other.start_time,
            "title": other.name,
            "time": f"{other.start_time.strftime('%H:%M')}-{other.end_time.strftime('%H:%M')}",
            "colour": "green",
        })

    events.sort(key=lambda event: event["sort_time"])

    grouped_timeline = defaultdict(list)
    for event in events:
        grouped_timeline[event["date"]].append(event)

    return grouped_timeline


def _render_booking_page(template_name, trip_id):
    """Render a booking page with all data needed for tabs and timeline."""
    trip = _get_trip_for_current_user(trip_id)
    booking_data = _get_booking_data(trip_id)
    grouped_timeline = _build_booking_timeline(booking_data)

    return render_template(
        template_name,
        trip=trip,
        grouped_timeline=grouped_timeline,
        **booking_data,
    )


@bookings_bp.route("/flights/<int:trip_id>", methods=["GET", "POST"])
@login_required
def show_flights(trip_id):
    return _render_booking_page("flights.html", trip_id)


@bookings_bp.route("/accommodations/<int:trip_id>", methods=["GET", "POST"])
@login_required
def show_accommodations(trip_id):
    return _render_booking_page("accommodations.html", trip_id)


@bookings_bp.route("/cruises/<int:trip_id>", methods=["GET", "POST"])
@login_required
def show_cruises(trip_id):
    return _render_booking_page("cruises.html", trip_id)


@bookings_bp.route("/tours/<int:trip_id>", methods=["GET", "POST"])
@login_required
def show_tours(trip_id):
    return _render_booking_page("tours.html", trip_id)


@bookings_bp.route("/other/<int:trip_id>", methods=["GET", "POST"])
@login_required
def show_other(trip_id):
    return _render_booking_page("other.html", trip_id)
