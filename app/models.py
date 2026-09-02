from sqlalchemy.orm import declared_attr
from werkzeug.security import check_password_hash
from . import db
from flask_login import UserMixin

user_trip = db.Table('user_trip',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('trip_id', db.Integer, db.ForeignKey('trips.id'), primary_key=True)
)

flight_consultant = db.Table('flight_consultant',
    db.Column('flight_id', db.Integer, db.ForeignKey('flights.id'), primary_key=True),
    db.Column('consultant_id', db.Integer, db.ForeignKey('consultants.id'), primary_key=True)
)

accommodation_consultant = db.Table('accommodation_consultant',
    db.Column('accommodation_id', db.Integer, db.ForeignKey('accommodations.id'), primary_key=True),
    db.Column('consultant_id', db.Integer, db.ForeignKey('consultants.id'), primary_key=True)
)

other_consultant = db.Table('other_consultant',
    db.Column('other_id', db.Integer, db.ForeignKey('others.id'), primary_key=True),
    db.Column('consultant_id', db.Integer, db.ForeignKey('consultants.id'), primary_key=True)
)

tour_consultant = db.Table('tour_consultant',
    db.Column('tour_id', db.Integer, db.ForeignKey('tours.id'), primary_key=True),
    db.Column('consultant_id', db.Integer, db.ForeignKey('consultants.id'), primary_key=True)
)

cruise_consultant = db.Table('cruise_consultant',
    db.Column('cruise_id', db.Integer, db.ForeignKey('cruises.id'), primary_key=True),
    db.Column('consultant_id', db.Integer, db.ForeignKey('consultants.id'), primary_key=True)
)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    password_changed = db.Column(db.Boolean, default=True, nullable=False)

    trips = db.relationship('Trip', secondary=user_trip, back_populates='users')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    
class Consultant(db.Model):
    __tablename__ = "consultants"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    trips = db.relationship('Trip', back_populates='consultant')
    flights = db.relationship('Flight', secondary=flight_consultant, back_populates='consultants')
    accommodations = db.relationship('Accommodation', secondary=accommodation_consultant, back_populates='consultants')
    others = db.relationship('Other', secondary=other_consultant, back_populates='consultants')
    tours = db.relationship('Tours', secondary=tour_consultant, back_populates='consultants')
    cruises = db.relationship('Cruises', secondary=cruise_consultant, back_populates='consultants')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


class Trip(db.Model):
    __tablename__ = "trips"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    whiteboard = db.Column(db.Text, nullable=True)
    
    consultant_id = db.Column(db.Integer, db.ForeignKey('consultants.id'), nullable=False)
    
    consultant = db.relationship('Consultant', back_populates='trips')
    users = db.relationship('User', secondary=user_trip, back_populates='trips')
    

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
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)

    created_by_user = db.relationship("User", foreign_keys=[created_by])


class Booking(db.Model):
    __abstract__ = True 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(500), nullable=True)
    
    @declared_attr
    def trip_id(cls):
        return db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)


class Flight(Booking):
    __tablename__ = "flights"
    departure_airport = db.Column(db.String(100), nullable=False)
    arrival_airport = db.Column(db.String(100), nullable=False)
    flight_number = db.Column(db.String(20), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False) 
    arrival_time = db.Column(db.DateTime, nullable=False)
    
    consultants = db.relationship('Consultant', secondary=flight_consultant, back_populates='flights')

    
class Accommodation(Booking):
    __tablename__ = "accommodations"
    check_in = db.Column(db.DateTime, nullable=False)
    check_out = db.Column(db.DateTime, nullable=False)
    room_capacity = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    contact_email = db.Column(db.String(100), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    
    consultants = db.relationship('Consultant', secondary=accommodation_consultant, back_populates='accommodations')

    
class Other(Booking):
    __tablename__ = "others"
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    
    consultants = db.relationship('Consultant', secondary=other_consultant, back_populates='others')

    
class Tours(Booking):
    __tablename__ = "tours"
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    
    consultants = db.relationship('Consultant', secondary=tour_consultant, back_populates='tours')

    
class Cruises(Booking):
    __tablename__ = "cruises"
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)
    boardingLocation = db.Column(db.String(100), nullable=False)
    dropOffLocation = db.Column(db.String(100), nullable=False)
    cruiseLine = db.Column(db.String(100), nullable=True)
    
    consultants = db.relationship('Consultant', secondary=cruise_consultant, back_populates='cruises')

    
class Budget(db.Model):
    __tablename__ = "budgets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
