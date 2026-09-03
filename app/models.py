from sqlalchemy.orm import declared_attr
from werkzeug.security import check_password_hash
from . import db
from flask_login import UserMixin


user_trip = db.Table(
    'user_trip',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('trip_id', db.Integer, db.ForeignKey('trips.id'), primary_key=True)
)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    password_changed = db.Column(db.Boolean, default=True, nullable=False)

    trips = db.relationship(
        'Trip',
        secondary=user_trip,
        back_populates='users'
    )

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Consultant(db.Model):
    __tablename__ = "consultants"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    trips = db.relationship(
        'Trip',
        back_populates='consultant'
    )

    flights = db.relationship(
        'Flight',
        back_populates='consultant'
    )

    accommodations = db.relationship(
        'Accommodation',
        back_populates='consultant'
    )

    others = db.relationship(
        'Other',
        back_populates='consultant'
    )

    tours = db.relationship(
        'Tour',
        back_populates='consultant'
    )

    cruises = db.relationship(
        'Cruise',
        back_populates='consultant'
    )

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    whiteboard = db.Column(db.Text, nullable=True)

    consultant_id = db.Column(
        db.Integer,
        db.ForeignKey('consultants.id'),
        nullable=False
    )

    consultant = db.relationship(
        'Consultant',
        back_populates='trips'
    )

    users = db.relationship(
        'User',
        secondary=user_trip,
        back_populates='trips'
    )


class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=True)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    notes = db.Column(db.String(8000), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(500), nullable=True)
    created_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    trip_id = db.Column(
        db.Integer,
        db.ForeignKey('trips.id'),
        nullable=False
    )

    created_by_user = db.relationship(
        "User",
        foreign_keys=[created_by]
    )


class Booking(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(500), nullable=True)

    @declared_attr
    def trip_id(cls):
        return db.Column(
            db.Integer,
            db.ForeignKey('trips.id'),
            nullable=False
        )

    @declared_attr
    def consultant_id(cls):
        return db.Column(
            db.Integer,
            db.ForeignKey('consultants.id'),
            nullable=False
        )


class Flight(Booking):
    __tablename__ = "flights"

    departure_airport = db.Column(db.String(100), nullable=False)
    departure_address = db.Column(db.String(500), nullable=True)

    arrival_airport = db.Column(db.String(100), nullable=False)
    arrival_address = db.Column(db.String(500), nullable=True)

    flight_number = db.Column(db.String(20), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)

    consultant = db.relationship(
        'Consultant',
        back_populates='flights'
    )


class Accommodation(Booking):
    __tablename__ = "accommodations"

    check_in = db.Column(db.DateTime, nullable=False)
    check_out = db.Column(db.DateTime, nullable=False)
    room_capacity = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    contact_email = db.Column(db.String(100), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)

    consultant = db.relationship(
        'Consultant',
        back_populates='accommodations'
    )


class Other(Booking):
    __tablename__ = "others"

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    consultant = db.relationship(
        'Consultant',
        back_populates='others'
    )


class Tour(Booking):
    __tablename__ = "tours"

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    consultant = db.relationship(
        'Consultant',
        back_populates='tours'
    )


class Cruise(Booking):
    __tablename__ = "cruises"

    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    boarding_location = db.Column(db.String(100), nullable=False)
    boarding_address = db.Column(db.String(500), nullable=True)

    drop_off_location = db.Column(db.String(100), nullable=False)
    drop_off_address = db.Column(db.String(500), nullable=True)

    cruise_line = db.Column(db.String(100), nullable=True)

    consultant = db.relationship(
        'Consultant',
        back_populates='cruises'
    )


class Budget(db.Model):
    __tablename__ = "budgets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    trip_id = db.Column(
        db.Integer,
        db.ForeignKey('trips.id'),
        nullable=False
    )