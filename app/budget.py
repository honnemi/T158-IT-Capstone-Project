from datetime import datetime

from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from app.models import (
    Trip,
    Budget,
    Flight,
    Accommodation,
    Other,
    Tour,
    Cruise
)


budget_bp = Blueprint("budget", __name__)


@budget_bp.route("/budget/<int:trip_id>", methods=["GET"])
@login_required
def show_budget(trip_id):

    # ========================================
    # GET TRIP
    # ========================================

    trip = Trip.query.get_or_404(trip_id)

    # Make sure the logged-in user belongs
    # to the selected trip
    if current_user not in trip.users:
        abort(403)


    # ========================================
    # GET BUDGET
    # ========================================

    budget = (
        Budget.query
        .filter_by(trip_id=trip_id)
        .first()
    )


    # ========================================
    # GET ALL BOOKINGS
    # ========================================

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

    tours = (
        Tour.query
        .filter_by(trip_id=trip_id)
        .order_by(Tour.start_time.asc())
        .all()
    )

    cruises = (
        Cruise.query
        .filter_by(trip_id=trip_id)
        .order_by(Cruise.start_date.asc())
        .all()
    )

    others = (
        Other.query
        .filter_by(trip_id=trip_id)
        .order_by(Other.start_time.asc())
        .all()
    )


    # ========================================
    # CALCULATE TOTALS
    # ========================================

    flight_total = sum(
        flight.cost
        for flight in flights
    )

    accommodation_total = sum(
        accommodation.cost
        for accommodation in accommodations
    )

    tour_total = sum(
        tour.cost
        for tour in tours
    )

    cruise_total = sum(
        cruise.cost
        for cruise in cruises
    )

    other_total = sum(
        other.cost
        for other in others
    )


    # ========================================
    # TOTAL SPENT
    # ========================================

    total_spent = (
        flight_total
        + accommodation_total
        + tour_total
        + cruise_total
        + other_total
    )


    # ========================================
    # TOTAL BUDGET
    # ========================================

    if budget:
        total_budget = budget.total_amount
    else:
        total_budget = 0


    # ========================================
    # REMAINING BUDGET
    # ========================================

    remaining_budget = (
        total_budget
        - total_spent
    )


    # ========================================
    # BUILD BUDGET ITEM LIST
    # ========================================

    budget_items = []


    # Flights
    for flight in flights:

        budget_items.append({
            "name": flight.name,
            "cost": flight.cost,
            "location": flight.location,
            "type": "Flight",
            "updated_at": flight.updated_at,
            "updated_by": (
                flight.updated_by_user.name
                if flight.updated_by_user
                else None
            )
        })


    # Accommodation
    for accommodation in accommodations:

        budget_items.append({
            "name": accommodation.name,
            "cost": accommodation.cost,
            "location": accommodation.location,
            "type": "Accommodation",
            "updated_at": accommodation.updated_at,
            "updated_by": (
                accommodation.updated_by_user.name
                if accommodation.updated_by_user
                else None
            )
        })


    # Tours
    for tour in tours:

        budget_items.append({
            "name": tour.name,
            "cost": tour.cost,
            "location": tour.location,
            "type": "Tour",
            "updated_at": tour.updated_at,
            "updated_by": (
                tour.updated_by_user.name
                if tour.updated_by_user
                else None
            )
        })


    # Cruises
    for cruise in cruises:

        budget_items.append({
            "name": cruise.name,
            "cost": cruise.cost,
            "location": cruise.location,
            "type": "Cruise",
            "updated_at": cruise.updated_at,
            "updated_by": (
                cruise.updated_by_user.name
                if cruise.updated_by_user
                else None
            )
        })


    # Other bookings
    for other in others:

        budget_items.append({
            "name": other.name,
            "cost": other.cost,
            "location": other.location,
            "type": "Other",
            "updated_at": other.updated_at,
            "updated_by": (
                other.updated_by_user.name
                if other.updated_by_user
                else None
            )
        })


    # ========================================
    # MOST RECENTLY UPDATED FIRST
    # ========================================

    budget_items.sort(
        key=lambda item: (
            item["updated_at"]
            if item["updated_at"]
            else datetime.min
        ),
        reverse=True
    )


    # ========================================
    # LOAD PAGE
    # ========================================

    return render_template(
        "budget.html",
        trip=trip,
        budget=budget,
        total_budget=total_budget,
        total_spent=total_spent,
        remaining_budget=remaining_budget,
        flight_total=flight_total,
        accommodation_total=accommodation_total,
        tour_total=tour_total,
        cruise_total=cruise_total,
        other_total=other_total,
        budget_items=budget_items
    )