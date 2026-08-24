from flask import Blueprint, render_template

itinerary_bp = Blueprint("itinerary", __name__)

@itinerary_bp.route("/itinerary")
def show_itinerary_overview():
    return render_template("itinerary-overview.html")

@itinerary_bp.route("/itinerary/detailed")
def show_itinerary_detailed():
    return render_template("itinerary-detailed.html")
