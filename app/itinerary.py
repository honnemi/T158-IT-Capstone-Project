from flask import Blueprint, render_template, abort, request
from flask_login import login_required, current_user
from app.models import Trip, Activity, Flight, Accommodation, Other
from datetime import timedelta

itinerary_bp = Blueprint(
    "itinerary",
    __name__,
    url_prefix="/itinerary"
)


@itinerary_bp.route("/overview/<int:trip_id>")
@login_required
def show_itinerary_overview(trip_id):

    trip = Trip.query.get_or_404(trip_id)

    if current_user not in trip.users:
        abort(403)

    week = request.args.get("week", 1, type=int)

    trip_start = trip.start_date

    trip_duration = (trip.end_date - trip_start).days + 1
    max_week = (trip_duration + 6) // 7

    # Find the Sunday at the start of the first calendar week
    first_sunday = trip_start - timedelta(
        days=(trip_start.weekday() + 1) % 7
    )

    # Calculate this week's Sunday
    week_start = first_sunday + timedelta(days=(week - 1) * 7)

    # Calculate Saturday
    week_end = week_start + timedelta(days=6)

    # Don't allow weeks completely after the trip
    if week_start > trip.end_date:
        week = 1
        week_start = first_sunday
        week_end = week_start + timedelta(days=6)

    activities = Activity.query.filter_by(
        trip_id=trip.id
    ).all()

    flights = Flight.query.filter_by(
        trip_id=trip.id
    ).all()

    accommodations = Accommodation.query.filter_by(
        trip_id=trip.id
    ).all()

    others = Other.query.filter_by(
        trip_id=trip.id
    ).all()

    calendar_items = []

    # Activities
    for activity in activities:

        calendar_items.append({
            "name": activity.name,
            "date": activity.date,
            "start_time": activity.start_time,
            "end_time": activity.end_time,
            "type": "activity"
        })

    # Flights
    for flight in flights:

        calendar_items.append({
            "name": flight.name,
            "date": flight.departure_time.date(),
            "start_time": flight.departure_time.time(),
            "end_time": flight.arrival_time.time(),
            "type": "flight"
        })

    # Accommodation
    for accommodation in accommodations:

        calendar_items.append({
            "name": accommodation.name + " - Check-in",
            "date": accommodation.check_in.date(),
            "start_time": accommodation.check_in.time(),
            "end_time": (
                accommodation.check_in + timedelta(minutes=30)
            ).time(),
            "type": "accommodation"
        })

        calendar_items.append({
            "name": accommodation.name + " - Check-out",
            "date": accommodation.check_out.date(),
            "start_time": accommodation.check_out.time(),
            "end_time": (
                accommodation.check_out + timedelta(minutes=30)
            ).time(),
            "type": "accommodation"
        })

    # Other bookings
    for other in others:

        calendar_items.append({
            "name": other.name,
            "date": other.start_time.date(),
            "start_time": other.start_time.time(),
            "end_time": other.end_time.time(),
            "type": "other"
        })

    # Create Sunday -> Saturday dates
    week_dates = []

    current_date = week_start

    for _ in range(7):
        week_dates.append(current_date)
        current_date += timedelta(days=1)

    # Only keep items belonging to this week
    calendar_items = [
        item
        for item in calendar_items
        if week_start <= item["date"] <= week_end
    ]

    # Calculate position and height
    for item in calendar_items:

        start_minutes = (
            item["start_time"].hour * 60
            + item["start_time"].minute
        )

        end_minutes = (
            item["end_time"].hour * 60
            + item["end_time"].minute
        )

        # Position from midnight
        item["top_percent"] = (
            start_minutes / 1440
        ) * 100

        # Height based on duration
        duration = end_minutes - start_minutes

        # Handle something that crosses midnight
        if duration <= 0:
            duration += 1440

        item["height_percent"] = (
            duration / 1440
        ) * 100

    return render_template(
        "itinerary-overview.html",
        trip=trip,
        calendar_items=calendar_items,
        week_dates=week_dates,
        week=week,
        max_week=max_week,
        week_start=week_start,
        week_end=week_end
    )


@itinerary_bp.route("/detailed/<int:trip_id>", methods=["GET", "POST"])
@login_required
def show_itinerary_detailed(trip_id):

    trip = Trip.query.get_or_404(trip_id)
    
    if current_user not in trip.users:
        abort(403)

    activities = Activity.query.filter_by(
        trip_id=trip.id
    ).all()

    return render_template(
        "itinerary-detailed.html",
        trip=trip,
        activities=activities
    )