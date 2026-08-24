from flask import Blueprint, render_template

inspo_bp = Blueprint("inspo", __name__)

@inspo_bp.route("/inspo")
def show_inspo():
    return render_template("inspo.html")