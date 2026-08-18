from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("base.html")

@main.route("/itinerary")
def show_itinerary_overview():
    return render_template("itinerary-overview.html")

@main.route("/itinerary/detailed")
def show_itinerary_detailed():
    return render_template("itinerary-detailed.html")

@main.route("/budget")
def show_budget():
    return render_template("budget.html")

@main.route("/flights")
def show_flights():
    return render_template("flights.html")

@main.route("/accommodations")
def show_accommodations():
    return render_template("accommodations.html")

@main.route("/other")
def show_other():
    return render_template("other.html")

@main.route("/login")
def show_login():
    return render_template("login.html")
