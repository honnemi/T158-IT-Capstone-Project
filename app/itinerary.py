from flask import Blueprint, render_template
from flask_login import login_required

itinerary_bp = Blueprint("itinerary", __name__)

@itinerary_bp.route("/itinerary", methods=["GET", "POST"])
@login_required
def show_itinerary_overview():
    return render_template("itinerary-overview.html")

@itinerary_bp.route("/itinerary/detailed", methods=["GET", "POST"])
@login_required
def show_itinerary_detailed():
    return render_template("itinerary-detailed.html")
