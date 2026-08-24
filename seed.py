from datetime import date, datetime, time
from werkzeug.security import generate_password_hash

# Adjust imports to match your project's structure
from app import create_app, db

app = create_app()

from app.models import (
    User, Trip, Activity, Flight, 
    Accommodation, Other, Budget
)

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        print("Seeding database...")

        # 1. Create Users
        alex = User(
            name="Alex Morgan",
            email="alex@example.com",
            password=generate_password_hash("Test123!"),
            password_changed=True
        )
        sam = User(
            name="Sam Taylor",
            email="sam@example.com",
            password=generate_password_hash("Test123!"),
            password_changed=True
        )
        db.session.add_all([alex, sam])
        db.session.commit()

        # 2. Create Trip
        tokyo_trip = Trip(
            name="Tokyo Weekend Getaway",
            start_date=date(2026, 10, 10),
            end_date=date(2026, 10, 13),
            consultant_name="Sarah Jenkins (GlobeTrotter Travel)"
        )
        
        # Associate users with the trip
        tokyo_trip.users.extend([alex, sam])
        db.session.add(tokyo_trip)
        db.session.commit()

        # 3. Create Budget
        trip_budget = Budget(
            name="Tokyo Travel Fund",
            total_amount=3500.00,
            trip_id=tokyo_trip.id
        )
        db.session.add(trip_budget)

        # 4. Create Bookings (Flights, Accommodation, Other)
        flight_outbound = Flight(
            name="Outbound Flight - LAX to NRT",
            cost=850.00,
            trip_id=tokyo_trip.id,
            departure_airport="LAX",
            arrival_airport="NRT",
            flight_number="NH175",
            departure_time=datetime(2026, 10, 10, 11, 30),
            arrival_time=datetime(2026, 10, 11, 15, 25)
        )

        flight_return = Flight(
            name="Return Flight - NRT to LAX",
            cost=850.00,
            trip_id=tokyo_trip.id,
            departure_airport="NRT",
            arrival_airport="LAX",
            flight_number="NH174",
            departure_time=datetime(2026, 10, 13, 17, 00),
            arrival_time=datetime(2026, 10, 13, 10, 45)
        )

        hotel = Accommodation(
            name="Shinjuku Park Hotel",
            cost=620.00,
            trip_id=tokyo_trip.id,
            location="Shinjuku, Tokyo",
            address="3-7-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo",
            check_in=date(2026, 10, 11),
            check_out=date(2026, 10, 13),
            room_capacity=2,
            rating=5,
            contact_email="reservations@shinjukupark.jp",
            contact_phone="+81-3-5322-1234"
        )

        jr_pass = Other(
            name="7-Day Whole Japan Rail Pass",
            cost=340.00,
            trip_id=tokyo_trip.id,
            start_time=datetime(2026, 10, 11, 16, 00),
            end_time=datetime(2026, 10, 13, 23, 59),
            location="Narita Airport Exchange Office"
        )

        db.session.add_all([flight_outbound, flight_return, hotel, jr_pass])

        # 5. Create Activities
        act1 = Activity(
            name="Visit Senso-ji Temple & Asakusa Market",
            date=date(2026, 10, 12),
            start_time=time(9, 0),
            end_time=time(12, 0),
            notes="Explore ancient temple grounds and pick up local street food at Nakamise Shopping Street.",
            created_by=alex.id,
            trip_id=tokyo_trip.id
        )

        act2 = Activity(
            name="Shibuya Crossing & teamLab Planets",
            date=date(2026, 10, 12),
            start_time=time(14, 30),
            end_time=time(18, 0),
            notes="Tickets reserved for teamLab entry at 15:00. Wear easy-to-remove shoes.",
            created_by=sam.id,
            trip_id=tokyo_trip.id
        )

        db.session.add_all([act1, act2])

        # Final commit
        db.session.commit()
        print("Database successfully seeded!")

if __name__ == "__main__":
    seed_database()