from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.show_login'
    
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
       print("LOAD USER CALLED:", user_id)
       return db.session.scalar(db.select(User).where(User.id==user_id))

    from . import home, auth, itinerary, bookings, inspo, budget
    app.register_blueprint(home.home_bp)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(itinerary.itinerary_bp)
    app.register_blueprint(bookings.bookings_bp)
    app.register_blueprint(inspo.inspo_bp)
    app.register_blueprint(budget.budget_bp)

    return app