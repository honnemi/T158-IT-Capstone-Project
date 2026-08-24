from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from app.models import Trip

budget_bp = Blueprint("budget", __name__)

@budget_bp.route("/budget/<int:trip_id>", methods=["GET", "POST"])
@login_required
def show_budget(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    if current_user not in trip.users:
        abort(403)
    return render_template("budget.html", trip=trip)

