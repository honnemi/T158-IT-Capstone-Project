from flask import Blueprint, render_template

budget_bp = Blueprint("budget", __name__)

@budget_bp.route("/budget")
def show_budget():
    return render_template("budget.html")

