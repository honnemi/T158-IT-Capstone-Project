from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Trip, Activity, Flight, Accommodation, Other
from datetime import datetime, timedelta
from app import db

itinerary_bp = Blueprint(
    "itinerary",
    __name__,
    url_prefix="/itinerary"
)

def position_overlapping_items(calendar_items):
    items_by_date = {}

    for item in calendar_items:
        items_by_date.setdefault(item["date"], []).append(item)

    for date_items in items_by_date.values():

        for item in date_items:

            start = (
                item["start_time"].hour * 60
                + item["start_time"].minute
            )

            end = (
                item["end_time"].hour * 60
                + item["end_time"].minute
            )

            if end <= start:
                end += 1440

            item["_start_minutes"] = start
            item["_end_minutes"] = end

            duration = end - start

            item["top_percent"] = (
                start / 1440
            ) * 100

            item["height_percent"] = (
                duration / 1440
            ) * 100

        date_items.sort(
            key=lambda item: item["_start_minutes"]
        )

        groups = []

        for item in date_items:

            added_to_group = False

            for group in groups:

                overlaps = any(
                    item["_start_minutes"] < other["_end_minutes"]
                    and item["_end_minutes"] > other["_start_minutes"]
                    for other in group
                )

                if overlaps:
                    group.append(item)
                    added_to_group = True
                    break

            if not added_to_group:
                groups.append([item])

        for group in groups:

            columns = []

            for item in group:

                placed = False

                for column_index, column in enumerate(columns):

                    if item["_start_minutes"] >= column[-1]["_end_minutes"]:
                        column.append(item)
                        item["_column"] = column_index
                        placed = True
                        break

                if not placed:
                    columns.append([item])
                    item["_column"] = len(columns) - 1

            total_columns = len(columns)

            for item in group:

                item["width_percent"] = 100 / total_columns

                item["left_percent"] = (
                    item["_column"]
                    * item["width_percent"]
                )

    for item in calendar_items:
        item.pop("_start_minutes", None)
        item.pop("_end_minutes", None)

    return calendar_items

@itinerary_bp.route("/overview/<int:trip_id>", methods=["GET"])
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

    # Calculate positions of each activity on the calendar
    calendar_items = position_overlapping_items(calendar_items)

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

    # Get day/date from URL
    date_string = request.args.get("date")
    current_day = request.args.get("day", type=int)

    # If user selected a date from the date picker
    if date_string:

        try:
            selected_date = datetime.strptime(
                date_string,
                "%Y-%m-%d"
            ).date()

            current_day = (
                selected_date - trip.start_date
            ).days + 1

        except ValueError:
            current_day = 1

    # Default to Day 1
    elif current_day is None:
        current_day = 1

    # Trip duration
    trip_duration = (
        trip.end_date - trip.start_date
    ).days + 1

    # Keep day inside trip
    current_day = max(
        1,
        min(current_day, trip_duration)
    )

    # Calculate date from day number
    selected_date = trip.start_date + timedelta(
        days=current_day - 1
    )

    # Get itinerary items from DB
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

        # Ignore unscheduled activities
        if activity.date is None:
            continue

        calendar_items.append({
            "id": activity.id,
            "name": activity.name,
            "date": activity.date,
            "start_time": activity.start_time,
            "end_time": activity.end_time,
            "location": activity.location,
            "address": activity.address,
            "notes": activity.notes,
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
                accommodation.check_in
                + timedelta(minutes=30)
            ).time(),
            "type": "accommodation"
        })

        calendar_items.append({
            "name": accommodation.name + " - Check-out",
            "date": accommodation.check_out.date(),
            "start_time": accommodation.check_out.time(),
            "end_time": (
                accommodation.check_out
                + timedelta(minutes=30)
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

    # Only show activities for the selected day
    calendar_items = [
        item
        for item in calendar_items
        if item["date"] == selected_date
    ]

    # Calculate positions of each activity on the calendar
    calendar_items = position_overlapping_items(calendar_items)

    return render_template(
        "itinerary-detailed.html",
        trip=trip,
        calendar_items=calendar_items,
        current_day=current_day,
        max_day=trip_duration,
        selected_date=selected_date
    )

@itinerary_bp.route("/delete/<int:activity_id>", methods=["POST"])
@login_required
def delete_activity(activity_id):

    activity = Activity.query.get_or_404(activity_id)

    # Get the trip using the activity's trip_id
    trip = Trip.query.get_or_404(activity.trip_id)

    # Make sure the current user belongs to this trip
    if current_user not in trip.users:
        abort(403)

    db.session.delete(activity)
    db.session.commit()

    # Keep the user on the day they were viewing
    day = request.form.get("day", type=int)

    return redirect(url_for(
        "itinerary.show_itinerary_detailed",
        trip_id=trip.id,
        day=day or 1
    ))

@itinerary_bp.route("/edit/<int:activity_id>", methods=["POST"])
@login_required
def edit_activity(activity_id):

    activity = Activity.query.get_or_404(activity_id)

    trip = Trip.query.get_or_404(activity.trip_id)

    if current_user not in trip.users:
        abort(403)

    activity.name = request.form.get("name")
    activity.location = request.form.get("location")
    activity.notes = request.form.get("notes")

    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")

    if start_time:
        activity.start_time = datetime.strptime(
            start_time,
            "%H:%M"
        ).time()

    if end_time:
        activity.end_time = datetime.strptime(
            end_time,
            "%H:%M"
        ).time()

    db.session.commit()

    day = request.form.get("day", type=int)

    return redirect(url_for(
        "itinerary.show_itinerary_detailed",
        trip_id=trip.id,
        day=day or 1
    ))