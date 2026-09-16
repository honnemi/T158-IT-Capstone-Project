from flask import Blueprint, render_template
from flask_login import login_required, current_user


account_bp = Blueprint("account", __name__)


@account_bp.route("/account", methods=["GET"])
@login_required
def show_account():
    user_trips = current_user.trips
    trip = user_trips[0] if user_trips else None

    return render_template(
        "account.html",
        trip=trip
    )