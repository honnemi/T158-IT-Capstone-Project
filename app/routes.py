from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("base.html")

@main.route("/itinerary")
def show_itinerary_overview():
    return render_template("itinerary-overview.html")