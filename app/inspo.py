from flask import Blueprint, render_template, abort, request, jsonify
from flask_login import login_required, current_user
from app.models import Trip
from app import db
from datetime import datetime
import json

inspo_bp = Blueprint("inspo", __name__)

@inspo_bp.route("/inspo/<int:trip_id>", methods=["GET", "POST"])
@login_required
def show_inspo(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    view_only = trip.end_date < datetime.now().date()
    return render_template("inspo.html", trip=trip, view_only=view_only)

@inspo_bp.route("/inspo/save/<int:trip_id>", methods=["POST"])
@login_required
def save_whiteboard(trip_id):
    trip = Trip.query.get_or_404(trip_id)

    data = request.get_json()
    trip.whiteboard = data.get("whiteboard")

    db.session.commit()

    return jsonify({"success": True})