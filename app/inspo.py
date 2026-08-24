from flask import Blueprint, render_template
from flask_login import login_required

inspo_bp = Blueprint("inspo", __name__)

@inspo_bp.route("/inspo")
@login_required
def show_inspo():
    return render_template("inspo.html")