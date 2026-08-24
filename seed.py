from datetime import date, datetime, time
from werkzeug.security import generate_password_hash

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

        # ============================================================
        # 1. USERS
        # ============================================================

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

        jordan = User(
            name="Jordan Lee",
            email="jordan@example.com",
            password=generate_password_hash("Test123!"),
            password_changed=True
        )

        db.session.add_all([alex, sam, jordan])
        db.session.commit()


        # ============================================================
        # 2. TRIP
        # ============================================================

        tokyo_trip = Trip(
            name="Tokyo Adventure",
            start_date=date(2026, 10, 10),
            end_date=date(2026, 10, 17),
            consultant_name="Sarah Jenkins (GlobeTrotter Travel)"
        )

        tokyo_trip.users.extend([alex, sam, jordan])

        db.session.add(tokyo_trip)
        db.session.commit()


        # ============================================================
        # 3. BUDGET
        # ============================================================

        trip_budget = Budget(
            name="Tokyo Travel Fund",
            total_amount=5000.00,
            trip_id=tokyo_trip.id
        )

        db.session.add(trip_budget)


        # ============================================================
        # 4. FLIGHTS
        # ============================================================

        # OUTBOUND
        # LAX -> NRT
        flight_outbound = Flight(
            name="Outbound Flight - LAX to NRT",
            cost=850.00,
            trip_id=tokyo_trip.id,

            departure_airport="LAX",
            arrival_airport="NRT",
            flight_number="NH175",

            departure_time=datetime(
                2026, 10, 10, 11, 30
            ),

            arrival_time=datetime(
                2026, 10, 11, 15, 25
            )
        )

        # RETURN
        # NRT -> LAX
        #
        # For simplicity, this uses a later date for arrival
        # so your calendar does not treat it as backwards.
        flight_return = Flight(
            name="Return Flight - NRT to LAX",
            cost=850.00,
            trip_id=tokyo_trip.id,

            departure_airport="NRT",
            arrival_airport="LAX",
            flight_number="NH174",

            departure_time=datetime(
                2026, 10, 17, 17, 00
            ),

            arrival_time=datetime(
                2026, 10, 18, 10, 45
            )
        )

        db.session.add_all([
            flight_outbound,
            flight_return
        ])


        # ============================================================
        # 5. ACCOMMODATION
        # ============================================================

        hotel = Accommodation(
            name="Shinjuku Park Hotel",
            cost=620.00,
            trip_id=tokyo_trip.id,

            location="Shinjuku, Tokyo",

            address=(
                "3-7-1 Nishi-Shinjuku, "
                "Shinjuku-ku, Tokyo"
            ),

            check_in=datetime(
                2026, 10, 11, 15, 00
            ),

            check_out=datetime(
                2026, 10, 17, 11, 00
            ),

            room_capacity=3,
            rating=5,

            contact_email="reservations@example.com",
            contact_phone="+81-3-5555-1234"
        )

        db.session.add(hotel)


        # ============================================================
        # 6. OTHER BOOKINGS
        # ============================================================

        jr_pass = Other(
            name="Japan Rail Pass",
            cost=340.00,
            trip_id=tokyo_trip.id,

            start_time=datetime(
                2026, 10, 11, 16, 00
            ),

            end_time=datetime(
                2026, 10, 17, 23, 59
            ),

            location="Narita Airport"
        )

        airport_transfer = Other(
            name="Airport Transfer",
            cost=80.00,
            trip_id=tokyo_trip.id,

            start_time=datetime(
                2026, 10, 11, 16, 00
            ),

            end_time=datetime(
                2026, 10, 11, 17, 30
            ),

            location="Narita Airport → Shinjuku"
        )

        dinner_booking = Other(
            name="Shibuya Dinner Reservation",
            cost=120.00,
            trip_id=tokyo_trip.id,

            start_time=datetime(
                2026, 10, 12, 19, 00
            ),

            end_time=datetime(
                2026, 10, 12, 21, 00
            ),

            location="Shibuya"
        )

        db.session.add_all([
            jr_pass,
            airport_transfer,
            dinner_booking
        ])


        # ============================================================
        # 7. ACTIVITIES
        # ============================================================

        activities = [

            # -------------------------
            # SUNDAY - OCT 11
            # -------------------------

            Activity(
                name="Arrive in Tokyo",
                date=date(2026, 10, 11),

                start_time=time(15, 25),
                end_time=time(16, 00),

                notes="Arrive at Narita Airport and collect luggage.",

                created_by=alex.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Check in to Hotel",
                date=date(2026, 10, 11),

                start_time=time(17, 30),
                end_time=time(18, 00),

                notes="Check in and settle into the hotel.",

                created_by=sam.id,
                trip_id=tokyo_trip.id
            ),


            # -------------------------
            # MONDAY - OCT 12
            # -------------------------

            Activity(
                name="Visit Senso-ji Temple",
                date=date(2026, 10, 12),

                start_time=time(9, 00),
                end_time=time(11, 00),

                notes=(
                    "Explore Senso-ji Temple "
                    "and Nakamise Shopping Street."
                ),

                created_by=alex.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Asakusa Market",
                date=date(2026, 10, 12),

                start_time=time(11, 15),
                end_time=time(12, 30),

                notes="Try local street food and browse the market.",

                created_by=sam.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Shibuya Crossing",
                date=date(2026, 10, 12),

                start_time=time(14, 00),
                end_time=time(15, 00),

                notes="Visit the famous Shibuya Crossing.",

                created_by=jordan.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="teamLab Planets",
                date=date(2026, 10, 12),

                start_time=time(15, 30),
                end_time=time(18, 00),

                notes=(
                    "Tickets reserved for 15:30. "
                    "Wear easy-to-remove shoes."
                ),

                created_by=sam.id,
                trip_id=tokyo_trip.id
            ),


            # -------------------------
            # TUESDAY - OCT 13
            # -------------------------

            Activity(
                name="Tokyo Skytree",
                date=date(2026, 10, 13),

                start_time=time(9, 30),
                end_time=time(11, 30),

                notes="Visit the observation deck.",

                created_by=alex.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Lunch in Akihabara",
                date=date(2026, 10, 13),

                start_time=time(12, 00),
                end_time=time(13, 30),

                notes="Lunch and explore Akihabara.",

                created_by=jordan.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Akihabara Shopping",
                date=date(2026, 10, 13),

                start_time=time(14, 00),
                end_time=time(17, 00),

                notes="Explore electronics and anime stores.",

                created_by=sam.id,
                trip_id=tokyo_trip.id
            ),


            # -------------------------
            # WEDNESDAY - OCT 14
            # -------------------------

            Activity(
                name="Meiji Shrine",
                date=date(2026, 10, 14),

                start_time=time(8, 30),
                end_time=time(10, 30),

                notes="Morning visit to Meiji Shrine.",

                created_by=alex.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Harajuku Exploration",
                date=date(2026, 10, 14),

                start_time=time(11, 00),
                end_time=time(13, 00),

                notes="Explore Takeshita Street.",

                created_by=jordan.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Shinjuku Gyoen",
                date=date(2026, 10, 14),

                start_time=time(14, 00),
                end_time=time(16, 30),

                notes="Relax and explore the gardens.",

                created_by=sam.id,
                trip_id=tokyo_trip.id
            ),


            # -------------------------
            # THURSDAY - OCT 15
            # -------------------------

            Activity(
                name="Mount Fuji Day Trip",
                date=date(2026, 10, 15),

                start_time=time(7, 00),
                end_time=time(18, 00),

                notes="Full-day trip to Mount Fuji.",

                created_by=alex.id,
                trip_id=tokyo_trip.id
            ),


            # -------------------------
            # FRIDAY - OCT 16
            # -------------------------

            Activity(
                name="Tsukiji Outer Market",
                date=date(2026, 10, 16),

                start_time=time(9, 00),
                end_time=time(11, 00),

                notes="Breakfast and seafood market.",

                created_by=sam.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Imperial Palace",
                date=date(2026, 10, 16),

                start_time=time(12, 00),
                end_time=time(14, 00),

                notes="Explore the Imperial Palace grounds.",

                created_by=jordan.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Tokyo Night Tour",
                date=date(2026, 10, 16),

                start_time=time(19, 00),
                end_time=time(22, 00),

                notes="Explore Tokyo nightlife.",

                created_by=alex.id,
                trip_id=tokyo_trip.id
            ),


            # -------------------------
            # SATURDAY - OCT 17
            # -------------------------

            Activity(
                name="Final Shopping",
                date=date(2026, 10, 17),

                start_time=time(9, 00),
                end_time=time(11, 30),

                notes="Last-minute shopping before departure.",

                created_by=sam.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Return to Narita Airport",
                date=date(2026, 10, 17),

                start_time=time(14, 00),
                end_time=time(15, 30),

                notes="Travel to Narita Airport for return flight.",

                created_by=alex.id,
                trip_id=tokyo_trip.id
            )
        ]

        db.session.add_all(activities)


        # ============================================================
        # FINAL COMMIT
        # ============================================================

        db.session.commit()

        print("Database successfully seeded!")
        print(f"Trip ID: {tokyo_trip.id}")
        print(f"Activities created: {len(activities)}")

        print("\nTRIPS:")
        for trip in Trip.query.all():
            print(trip.id, trip.name, trip.start_date, trip.end_date)

        print("\nACTIVITIES:")
        for activity in Activity.query.all():
            print(
                activity.id,
                activity.name,
                activity.date,
                activity.start_time,
                activity.end_time
            )


if __name__ == "__main__":
    seed_database()