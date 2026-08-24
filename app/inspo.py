from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from app.models import Trip

inspo_bp = Blueprint("inspo", __name__)

@inspo_bp.route("/inspo/<int:trip_id>", methods=["GET", "POST"])
@login_required
def show_inspo(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    if current_user not in trip.users:
        abort(403)
    return render_template("inspo.html", trip=trip)