from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models import Consultant


contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contact", methods=["GET"])
@login_required
def show_contact():

    # Get all trips belonging to the current user
    user_trips = current_user.trips

    # base.html uses trip.id for the main navigation.
    # Use the user's first trip if they have one.
    trip = user_trips[0] if user_trips else None

    # ----------------------------------------
    # MY AGENTS
    # ----------------------------------------

    my_agents = []
    my_agent_ids = set()

    # Find consultants assigned to the
    # current user's trips
    for user_trip in user_trips:

        if (
            user_trip.consultant
            and user_trip.consultant.id not in my_agent_ids
        ):
            my_agents.append(user_trip.consultant)
            my_agent_ids.add(user_trip.consultant.id)

    # ----------------------------------------
    # OTHER AGENTS
    # ----------------------------------------

    if my_agent_ids:

        other_agents = (
            Consultant.query
            .filter(~Consultant.id.in_(my_agent_ids))
            .order_by(Consultant.name.asc())
            .all()
        )

    else:

        # If the user has no assigned agents,
        # show all consultants as other agents
        other_agents = (
            Consultant.query
            .order_by(Consultant.name.asc())
            .all()
        )

    # ----------------------------------------
    # LOAD CONTACT PAGE
    # ----------------------------------------

    return render_template(
        "contact.html",
        trip=trip,
        my_agents=my_agents,
        other_agents=other_agents
    )