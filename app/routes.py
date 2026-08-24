from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home.html")

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

@main.route("/inspo")
def show_inspo():
    return render_template("inspo.html")

@main.route("/login")
def show_login():
    return render_template("login.html")

@main.route("/forgot-password")
def show_forgot_password():
    return render_template("forgot-password.html")

@main.route("/reset-password")
def show_reset_password():
    return render_template("reset-password.html")