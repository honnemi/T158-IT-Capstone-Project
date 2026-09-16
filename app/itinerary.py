from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Trip, Activity, Flight, Accommodation, Cruise, Tour, Other
from datetime import datetime, timedelta
from app import db
from zoneinfo import ZoneInfo


itinerary_bp = Blueprint(
    "itinerary",
    __name__,
    url_prefix="/itinerary"
)


def get_timezone_name(date_value, time_value, timezone_id):
    timezone = ZoneInfo(timezone_id)

    if isinstance(time_value, datetime):
        aware_datetime = time_value.replace(tzinfo=timezone)
    else:
        aware_datetime = datetime.combine(
            date_value,
            time_value,
            tzinfo=timezone
        )

    return aware_datetime.strftime("%Z")


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

    first_sunday = trip_start - timedelta(
        days=(trip_start.weekday() + 1) % 7
    )

    week_start = first_sunday + timedelta(
        days=(week - 1) * 7
    )

    week_end = week_start + timedelta(days=6)

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

    cruises = Cruise.query.filter_by(
        trip_id=trip.id
    ).all()

    tours = Tour.query.filter_by(
        trip_id=trip.id
    ).all()

    others = Other.query.filter_by(
        trip_id=trip.id
    ).all()

    calendar_items = []

    for activity in activities:

        if activity.date is None:
            continue

        timezone = ZoneInfo(activity.timezone_id)

        start_dt = datetime.combine(
            activity.date,
            activity.start_time,
            tzinfo=timezone
        )

        end_dt = datetime.combine(
            activity.date,
            activity.end_time,
            tzinfo=timezone
        )

        calendar_items.append({
            "id": activity.id,
            "name": activity.name,
            "date": activity.date,
            "start_time": activity.start_time,
            "end_time": activity.end_time,
            "timezone": get_timezone_name(
                activity.date,
                activity.start_time,
                activity.timezone_id
            ),
            "location": activity.location,
            "address": activity.address,
            "notes": activity.notes,
            "created_by": activity.created_by_user.name,
            "type": "activity",
            "updated_at": activity.updated_at,
            "updated_by": (
                activity.updated_by_user.name
                if activity.updated_by_user
                else None
            )
        })

    for flight in flights:

        departure_timezone = ZoneInfo(
            flight.departure_timezone_id
        )

        arrival_timezone = ZoneInfo(
            flight.timezone_id
        )

        departure_dt = flight.departure_time.replace(
            tzinfo=departure_timezone
        )

        arrival_dt = flight.arrival_time.replace(
            tzinfo=arrival_timezone
        )

        calendar_items.append({
            "name": flight.name,
            "date": flight.departure_time.date(),
            "start_time": departure_dt,
            "end_time": arrival_dt,
            "timezone": departure_dt.strftime("%Z"),
            "start_timezone": departure_dt.strftime("%Z"),
            "end_timezone": arrival_dt.strftime("%Z"),
            "location": flight.departure_airport,
            "address": flight.departure_address,
            "type": "flight",
            "created_by": flight.consultant.name,
            "updated_at": flight.updated_at,
            "updated_by": (
                flight.updated_by_user.name
                if flight.updated_by_user
                else None
            )
        })

    for accommodation in accommodations:

        timezone = ZoneInfo(
            accommodation.timezone_id
        )

        check_in_dt = accommodation.check_in.replace(
            tzinfo=timezone
        )

        check_out_dt = accommodation.check_out.replace(
            tzinfo=timezone
        )

        calendar_items.append({
            "name": f"{accommodation.name} - Check-in",
            "date": accommodation.check_in.date(),
            "start_time": check_in_dt,
            "end_time": check_in_dt + timedelta(minutes=30),
            "timezone": check_in_dt.strftime("%Z"),
            "location": accommodation.location,
            "address": accommodation.address,
            "type": "accommodation",
            "created_by": accommodation.consultant.name,
            "updated_at": accommodation.updated_at,
            "updated_by": (
                accommodation.updated_by_user.name
                if accommodation.updated_by_user
                else None
            )
        })

        calendar_items.append({
            "name": f"{accommodation.name} - Check-out",
            "date": accommodation.check_out.date(),
            "start_time": check_out_dt,
            "end_time": check_out_dt + timedelta(minutes=30),
            "timezone": check_out_dt.strftime("%Z"),
            "location": accommodation.location,
            "address": accommodation.address,
            "type": "accommodation",
            "created_by": accommodation.consultant.name,
            "updated_at": accommodation.updated_at,
            "updated_by": (
                accommodation.updated_by_user.name
                if accommodation.updated_by_user
                else None
            )
        })

    for cruise in cruises:

        timezone = ZoneInfo(
            cruise.timezone_id
        )

        start_dt = cruise.start_date.replace(
            tzinfo=timezone
        )

        end_dt = cruise.end_date.replace(
            tzinfo=timezone
        )

        calendar_items.append({
            "name": f"{cruise.name} - Boarding",
            "date": cruise.start_date.date(),
            "start_time": start_dt,
            "end_time": start_dt + timedelta(minutes=30),
            "timezone": start_dt.strftime("%Z"),
            "location": cruise.boarding_location,
            "address": cruise.boarding_address,
            "type": "cruise",
            "created_by": cruise.consultant.name,
            "updated_at": cruise.updated_at,
            "updated_by": (
                cruise.updated_by_user.name
                if cruise.updated_by_user
                else None
            )
        })

        calendar_items.append({
            "name": f"{cruise.name} - Drop-off",
            "date": cruise.end_date.date(),
            "start_time": end_dt,
            "end_time": end_dt + timedelta(minutes=30),
            "timezone": end_dt.strftime("%Z"),
            "type": "cruise",
            "location": cruise.drop_off_location,
            "address": cruise.drop_off_address,
            "created_by": cruise.consultant.name,
            "updated_at": cruise.updated_at,
            "updated_by": (
                cruise.updated_by_user.name
                if cruise.updated_by_user
                else None
            )
        })

    for tour in tours:

        timezone = ZoneInfo(
            tour.timezone_id
        )

        start_dt = tour.start_time.replace(
            tzinfo=timezone
        )

        end_dt = tour.end_time.replace(
            tzinfo=timezone
        )

        calendar_items.append({
            "name": tour.name,
            "date": tour.start_time.date(),
            "start_time": start_dt,
            "end_time": end_dt,
            "timezone": start_dt.strftime("%Z"),
            "location": tour.location,
            "address": tour.address,
            "type": "tour",
            "created_by": tour.consultant.name,
            "updated_at": tour.updated_at,
            "updated_by": (
                tour.updated_by_user.name
                if tour.updated_by_user
                else None
            )
        })

    for other in others:

        timezone = ZoneInfo(
            other.timezone_id
        )

        start_dt = other.start_time.replace(
            tzinfo=timezone
        )

        end_dt = other.end_time.replace(
            tzinfo=timezone
        )

        calendar_items.append({
            "name": other.name,
            "date": other.start_time.date(),
            "start_time": start_dt,
            "end_time": end_dt,
            "timezone": start_dt.strftime("%Z"),
            "location": getattr(other, "location", None),
            "address": getattr(other, "address", None),
            "type": "other",
            "created_by": other.consultant.name,
            "updated_at": other.updated_at,
            "updated_by": (
                other.updated_by_user.name
                if other.updated_by_user
                else None
            )
        })

    week_dates = []

    current_date = week_start

    for _ in range(7):
        week_dates.append(current_date)
        current_date += timedelta(days=1)

    calendar_items = [
        item
        for item in calendar_items
        if week_start <= item["date"] <= week_end
    ]

    calendar_items = position_overlapping_items(
        calendar_items
    )

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

    date_string = request.args.get("date")
    current_day = request.args.get("day", type=int)

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

    elif current_day is None:
        current_day = 1

    trip_duration = (
        trip.end_date - trip.start_date
    ).days + 1

    current_day = max(
        1,
        min(current_day, trip_duration)
    )

    selected_date = trip.start_date + timedelta(
        days=current_day - 1
    )

    activities = Activity.query.filter_by(
        trip_id=trip.id
    ).all()

    flights = Flight.query.filter_by(
        trip_id=trip.id
    ).all()

    accommodations = Accommodation.query.filter_by(
        trip_id=trip.id
    ).all()

    tours = Tour.query.filter_by(
        trip_id=trip.id
    ).all()

    cruises = Cruise.query.filter_by(
        trip_id=trip.id
    ).all()

    others = Other.query.filter_by(
        trip_id=trip.id
    ).all()

    calendar_items = []

    for activity in activities:

        if activity.date is None:
            continue

        timezone = ZoneInfo(
            activity.timezone_id
        )

        start_dt = datetime.combine(
            activity.date,
            activity.start_time,
            tzinfo=timezone
        )

        end_dt = datetime.combine(
            activity.date,
            activity.end_time,
            tzinfo=timezone
        )

        calendar_items.append({
            "id": activity.id,
            "name": activity.name,
            "date": activity.date,
            "start_time": activity.start_time,
            "end_time": activity.end_time,
            "timezone": get_timezone_name(
                activity.date,
                activity.start_time,
                activity.timezone_id
            ),
            "location": activity.location,
            "address": activity.address,
            "notes": activity.notes,
            "created_by": activity.created_by_user.name,
            "type": "activity",
            "updated_at": activity.updated_at,
            "updated_by": (
                activity.updated_by_user.name
                if activity.updated_by_user
                else None
            )
        })

    for flight in flights:

        departure_timezone = ZoneInfo(
            flight.departure_timezone_id
        )

        arrival_timezone = ZoneInfo(
            flight.timezone_id
        )

        departure_dt = flight.departure_time.replace(
            tzinfo=departure_timezone
        )

        arrival_dt = flight.arrival_time.replace(
            tzinfo=arrival_timezone
        )

        calendar_items.append({
            "name": flight.name,
            "date": flight.departure_time.date(),
            "start_time": departure_dt,
            "end_time": arrival_dt,
            "timezone": departure_dt.strftime("%Z"),
            "start_timezone": departure_dt.strftime("%Z"),
            "end_timezone": arrival_dt.strftime("%Z"),
            "location": flight.departure_airport,
            "address": flight.departure_address,
            "type": "flight",
            "created_by": flight.consultant.name,
            "updated_at": flight.updated_at,
            "updated_by": (
                flight.updated_by_user.name
                if flight.updated_by_user
                else None
            )
        })

    for accommodation in accommodations:

        timezone = ZoneInfo(
            accommodation.timezone_id
        )

        check_in_dt = accommodation.check_in.replace(
            tzinfo=timezone
        )

        check_out_dt = accommodation.check_out.replace(
            tzinfo=timezone
        )

        calendar_items.append({
            "name": f"{accommodation.name} - Check-in",
            "date": accommodation.check_in.date(),
            "start_time": check_in_dt,
            "end_time": check_in_dt + timedelta(minutes=30),
            "timezone": check_in_dt.strftime("%Z"),
            "location": accommodation.location,
            "address": accommodation.address,
            "type": "accommodation",
            "created_by": accommodation.consultant.name,
            "updated_at": accommodation.updated_at,
            "updated_by": (
                accommodation.updated_by_user.name
                if accommodation.updated_by_user
                else None
            )
        })

        calendar_items.append({
            "name": f"{accommodation.name} - Check-out",
            "date": accommodation.check_out.date(),
            "start_time": check_out_dt,
            "end_time": check_out_dt + timedelta(minutes=30),
            "timezone": check_out_dt.strftime("%Z"),
            "location": accommodation.location,
            "address": accommodation.address,
            "type": "accommodation",
            "created_by": accommodation.consultant.name,
            "updated_at": accommodation.updated_at,
            "updated_by": (
                accommodation.updated_by_user.name
                if accommodation.updated_by_user
                else None
            )
        })

    for cruise in cruises:

        timezone = ZoneInfo(
            cruise.timezone_id
        )

        start_dt = cruise.start_date.replace(
            tzinfo=timezone
        )

        end_dt = cruise.end_date.replace(
            tzinfo=timezone
        )

        calendar_items.append({
            "name": f"{cruise.name} - Boarding",
            "date": cruise.start_date.date(),
            "start_time": start_dt,
            "end_time": start_dt + timedelta(minutes=30),
            "timezone": start_dt.strftime("%Z"),
            "location": cruise.boarding_location,
            "address": cruise.boarding_address,
            "type": "cruise",
            "created_by": cruise.consultant.name,
            "updated_at": cruise.updated_at,
            "updated_by": (
                cruise.updated_by_user.name
                if cruise.updated_by_user
                else None
            )
        })

        calendar_items.append({
            "name": f"{cruise.name} - Drop-off",
            "date": cruise.end_date.date(),
            "start_time": end_dt,
            "end_time": end_dt + timedelta(minutes=30),
            "timezone": end_dt.strftime("%Z"),
            "type": "cruise",
            "location": cruise.drop_off_location,
            "address": cruise.drop_off_address,
            "created_by": cruise.consultant.name,
            "updated_at": cruise.updated_at,
            "updated_by": (
                cruise.updated_by_user.name
                if cruise.updated_by_user
                else None
            )
        })

    for tour in tours:

        timezone = ZoneInfo(
            tour.timezone_id
        )

        start_dt = tour.start_time.replace(
            tzinfo=timezone
        )

        end_dt = tour.end_time.replace(
            tzinfo=timezone
        )

        calendar_items.append({
            "name": tour.name,
            "date": tour.start_time.date(),
            "start_time": start_dt,
            "end_time": end_dt,
            "timezone": start_dt.strftime("%Z"),
            "location": tour.location,
            "address": tour.address,
            "type": "tour",
            "created_by": tour.consultant.name,
            "updated_at": tour.updated_at,
            "updated_by": (
                tour.updated_by_user.name
                if tour.updated_by_user
                else None
            )
        })

    for other in others:

        timezone = ZoneInfo(
            other.timezone_id
        )

        start_dt = other.start_time.replace(
            tzinfo=timezone
        )

        end_dt = other.end_time.replace(
            tzinfo=timezone
        )

        calendar_items.append({
            "name": other.name,
            "date": other.start_time.date(),
            "start_time": start_dt,
            "end_time": end_dt,
            "timezone": start_dt.strftime("%Z"),
            "location": getattr(other, "location", None),
            "address": getattr(other, "address", None),
            "type": "other",
            "created_by": other.consultant.name,
            "updated_at": other.updated_at,
            "updated_by": (
                other.updated_by_user.name
                if other.updated_by_user
                else None
            )
        })

    calendar_items = [
        item
        for item in calendar_items
        if item["date"] == selected_date
    ]

    unassigned_activities = [
        activity
        for activity in activities
        if activity.date is None
    ]

    calendar_items = position_overlapping_items(
        calendar_items
    )

    return render_template(
        "itinerary-detailed.html",
        trip=trip,
        calendar_items=calendar_items,
        current_day=current_day,
        max_day=trip_duration,
        selected_date=selected_date,
        unassigned_activities=unassigned_activities
    )


@itinerary_bp.route("/delete/<int:activity_id>", methods=["POST"])
@login_required
def delete_activity(activity_id):

    activity = Activity.query.get_or_404(activity_id)

    trip = Trip.query.get_or_404(activity.trip_id)

    if current_user not in trip.users:
        abort(403)

    db.session.delete(activity)
    db.session.commit()

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
    activity.address = request.form.get("address")
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

    activity.updated_by = current_user.id

    db.session.commit()

    day = request.form.get("day", type=int)

    return redirect(url_for(
        "itinerary.show_itinerary_detailed",
        trip_id=trip.id,
        day=day or 1
    ))


@itinerary_bp.route("/move/<int:activity_id>", methods=["POST"])
@login_required
def move_activity(activity_id):

    activity = Activity.query.get_or_404(activity_id)

    trip = Trip.query.get_or_404(activity.trip_id)

    if current_user not in trip.users:
        abort(403)

    date_string = request.form.get("date")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")

    if not date_string:

        activity.date = None
        activity.start_time = None
        activity.end_time = None

    else:

        activity.date = datetime.strptime(
            date_string,
            "%Y-%m-%d"
        ).date()

        activity.start_time = datetime.strptime(
            start_time,
            "%H:%M"
        ).time()

        activity.end_time = datetime.strptime(
            end_time,
            "%H:%M"
        ).time()

    db.session.commit()

    return {"success": True}


@itinerary_bp.route("/add/<int:trip_id>", methods=["POST"])
@login_required
def add_activity(trip_id):

    trip = Trip.query.get_or_404(trip_id)

    if current_user not in trip.users:
        abort(403)

    name = request.form.get("name")
    location = request.form.get("location")
    address = request.form.get("address")
    notes = request.form.get("notes")

    if not name:
        return redirect(url_for(
            "itinerary.show_itinerary_detailed",
            trip_id=trip.id,
            day=request.form.get("day", type=int) or 1
        ))

    activity = Activity(
        name=name,
        location=location,
        address=address,
        notes=notes,
        trip_id=trip.id,
        date=None,
        start_time=None,
        end_time=None,
        created_by=current_user.name,
        timezone_id=trip.timezone_id
    )

    db.session.add(activity)
    db.session.commit()

    day = request.form.get("day", type=int)

    return redirect(url_for(
        "itinerary.show_itinerary_detailed",
        trip_id=trip.id,
        day=day or 1
    ))