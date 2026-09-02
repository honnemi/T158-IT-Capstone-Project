from datetime import date, datetime, time
from werkzeug.security import generate_password_hash

from app import create_app, db

from app.models import (
    User,
    Consultant,
    Trip,
    Activity,
    Flight,
    Accommodation,
    Other,
    Tour,
    Cruise,
    Budget
)

app = create_app()


def seed_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

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

        consultant = Consultant(
            name="Sarah Jenkins",
            email="sarah@globetrottertravel.com"
        )

        db.session.add(consultant)
        db.session.commit()

        trip = Trip(
            name="Tokyo Adventure",
            start_date=date(2026, 10, 10),
            end_date=date(2026, 10, 17),
            consultant=consultant,
            users=[alex, sam, jordan]
        )

        db.session.add(trip)
        db.session.commit()

        budget = Budget(
            name="Tokyo Travel Fund",
            total_amount=5000,
            trip_id=trip.id
        )

        flight_outbound = Flight(
            name="Outbound Flight - LAX to NRT",
            cost=650,
            location="Los Angeles International Airport",
            address="1 World Way, Los Angeles, CA 90045, USA",
            trip_id=trip.id,
            consultant=consultant,
            departure_airport="LAX",
            departure_address="1 World Way, Los Angeles, CA 90045, USA",
            arrival_airport="NRT",
            arrival_address="1-1 Furugome, Narita, Chiba 282-0004, Japan",
            flight_number="NH175",
            departure_time=datetime(2026, 10, 10, 11, 30),
            arrival_time=datetime(2026, 10, 11, 15, 25)
        )

        flight_return = Flight(
            name="Return Flight - NRT to LAX",
            cost=700,
            location="Narita International Airport",
            address="1-1 Furugome, Narita, Chiba 282-0004, Japan",
            trip_id=trip.id,
            consultant=consultant,
            departure_airport="NRT",
            departure_address="1-1 Furugome, Narita, Chiba 282-0004, Japan",
            arrival_airport="LAX",
            arrival_address="1 World Way, Los Angeles, CA 90045, USA",
            flight_number="NH174",
            departure_time=datetime(2026, 10, 17, 17, 0),
            arrival_time=datetime(2026, 10, 18, 10, 45)
        )

        hotel = Accommodation(
            name="Shinjuku Park Hotel",
            cost=1400,
            location="Shinjuku",
            address="3-7-1 Nishi-Shinjuku, Shinjuku City, Tokyo, Japan",
            trip_id=trip.id,
            consultant=consultant,
            check_in=datetime(2026, 10, 11, 15, 0),
            check_out=datetime(2026, 10, 17, 11, 0),
            room_capacity=3,
            rating=4,
            contact_email="info@shinjukuparkhotel.com",
            contact_phone="+81 3 1234 5678"
        )

        jr_pass = Other(
            name="Japan Rail Pass",
            cost=500,
            location="Tokyo Station",
            address="1 Chome Marunouchi, Chiyoda City, Tokyo, Japan",
            trip_id=trip.id,
            consultant=consultant,
            start_time=datetime(2026, 10, 11, 16, 0),
            end_time=datetime(2026, 10, 17, 23, 59)
        )

        airport_transfer = Other(
            name="Airport Transfer",
            cost=120,
            location="Narita International Airport",
            address="1-1 Furugome, Narita, Chiba 282-0004, Japan",
            trip_id=trip.id,
            consultant=consultant,
            start_time=datetime(2026, 10, 11, 16, 0),
            end_time=datetime(2026, 10, 11, 17, 30)
        )

        dinner_booking = Other(
            name="Shibuya Dinner Reservation",
            cost=180,
            location="Shibuya",
            address="Shibuya, Tokyo, Japan",
            trip_id=trip.id,
            consultant=consultant,
            start_time=datetime(2026, 10, 12, 19, 0),
            end_time=datetime(2026, 10, 12, 21, 0)
        )

        tokyo_food_tour = Tour(
            name="Tokyo Food Tour",
            cost=150,
            location="Tsukiji",
            address="Tsukiji, Chuo City, Tokyo, Japan",
            trip_id=trip.id,
            consultant=consultant,
            start_time=datetime(2026, 10, 13, 18, 0),
            end_time=datetime(2026, 10, 13, 21, 0)
        )

        tokyo_walking_tour = Tour(
            name="Tokyo Walking Tour",
            cost=100,
            location="Asakusa",
            address="Asakusa, Taito City, Tokyo, Japan",
            trip_id=trip.id,
            consultant=consultant,
            start_time=datetime(2026, 10, 14, 10, 30),
            end_time=datetime(2026, 10, 14, 13, 0)
        )

        tokyo_bay_cruise = Cruise(
            name="Tokyo Bay Dinner Cruise",
            cost=250,
            location="Tokyo Bay",
            address="Tokyo Bay, Tokyo, Japan",
            trip_id=trip.id,
            consultant=consultant,
            start_date=datetime(2026, 10, 15, 18, 0),
            end_date=datetime(2026, 10, 15, 21, 0),
            boarding_location="Hinode Pier",
            boarding_address="1-7 Kaigan, Minato City, Tokyo, Japan",
            drop_off_location="Hinode Pier",
            drop_off_address="1-7 Kaigan, Minato City, Tokyo, Japan",
            cruise_line="Tokyo Bay Cruise"
        )

        japan_coastal_cruise = Cruise(
            name="Japan Coastal Cruise",
            cost=600,
            location="Yokohama",
            address="Yokohama Port, Yokohama, Japan",
            trip_id=trip.id,
            consultant=consultant,
            start_date=datetime(2026, 10, 16, 8, 0),
            end_date=datetime(2026, 10, 16, 20, 0),
            boarding_location="Yokohama Port",
            boarding_address="1 Yamashita-cho, Naka Ward, Yokohama, Japan",
            drop_off_location="Yokohama Port",
            drop_off_address="1 Yamashita-cho, Naka Ward, Yokohama, Japan",
            cruise_line="Japan Coastal Lines"
        )

        db.session.add_all([
            budget,
            flight_outbound,
            flight_return,
            hotel,
            jr_pass,
            airport_transfer,
            dinner_booking,
            tokyo_food_tour,
            tokyo_walking_tour,
            tokyo_bay_cruise,
            japan_coastal_cruise
        ])

        activities = [
            Activity(
                name="Arrive in Tokyo",
                date=date(2026, 10, 11),
                start_time=time(15, 25),
                end_time=time(16, 0),
                notes="Arrive at Narita Airport and collect luggage.",
                location="Narita International Airport",
                address="1-1 Furugome, Narita, Chiba 282-0004, Japan",
                created_by=alex.id,
                trip_id=trip.id
            ),
            Activity(
                name="Check in to Hotel",
                date=date(2026, 10, 11),
                start_time=time(17, 30),
                end_time=time(18, 0),
                notes="Check in and settle into the hotel.",
                location="Shinjuku",
                address="3-7-1 Nishi-Shinjuku, Shinjuku City, Tokyo, Japan",
                created_by=sam.id,
                trip_id=trip.id
            ),
            Activity(
                name="Visit Senso-ji Temple",
                date=date(2026, 10, 12),
                start_time=time(9, 0),
                end_time=time(11, 0),
                notes="Explore Tokyo's oldest temple.",
                location="Senso-ji Temple",
                address="2 Chome-3-1 Asakusa, Taito City, Tokyo, Japan",
                created_by=alex.id,
                trip_id=trip.id
            ),
            Activity(
                name="Asakusa Market",
                date=date(2026, 10, 12),
                start_time=time(11, 15),
                end_time=time(12, 30),
                notes="Browse local food and souvenir stalls.",
                location="Nakamise Shopping Street",
                address="1 Chome-36-3 Asakusa, Taito City, Tokyo, Japan",
                created_by=sam.id,
                trip_id=trip.id
            ),
            Activity(
                name="Shibuya Crossing",
                date=date(2026, 10, 12),
                start_time=time(14, 0),
                end_time=time(15, 0),
                notes="Visit the famous Shibuya Crossing.",
                location="Shibuya Crossing",
                address="2 Chome-24-1 Shibuya, Shibuya City, Tokyo, Japan",
                created_by=jordan.id,
                trip_id=trip.id
            ),
            Activity(
                name="teamLab Planets",
                date=date(2026, 10, 12),
                start_time=time(15, 30),
                end_time=time(18, 0),
                notes="Visit the immersive digital art museum.",
                location="teamLab Planets TOKYO",
                address="6 Chome-1-16 Toyosu, Koto City, Tokyo, Japan",
                created_by=sam.id,
                trip_id=trip.id
            ),
            Activity(
                name="Tokyo Skytree",
                date=date(2026, 10, 13),
                start_time=time(9, 30),
                end_time=time(11, 30),
                notes="Visit the Tokyo Skytree observation decks.",
                location="Tokyo Skytree",
                address="1 Chome-1-2 Oshiage, Sumida City, Tokyo, Japan",
                created_by=alex.id,
                trip_id=trip.id
            ),
            Activity(
                name="Lunch in Akihabara",
                date=date(2026, 10, 13),
                start_time=time(12, 0),
                end_time=time(13, 30),
                notes="Lunch and explore local restaurants.",
                location="Akihabara",
                address="Akihabara, Taito City, Tokyo, Japan",
                created_by=jordan.id,
                trip_id=trip.id
            ),
            Activity(
                name="Akihabara Shopping",
                date=date(2026, 10, 13),
                start_time=time(14, 0),
                end_time=time(17, 0),
                notes="Shop for electronics, games and anime merchandise.",
                location="Akihabara",
                address="Akihabara, Taito City, Tokyo, Japan",
                created_by=sam.id,
                trip_id=trip.id
            ),
            Activity(
                name="Meiji Shrine",
                date=date(2026, 10, 14),
                start_time=time(8, 30),
                end_time=time(10, 30),
                notes="Visit the famous Shinto shrine.",
                location="Meiji Jingu",
                address="1-1 Yoyogikamizonocho, Shibuya City, Tokyo, Japan",
                created_by=alex.id,
                trip_id=trip.id
            ),
            Activity(
                name="Harajuku Exploration",
                date=date(2026, 10, 14),
                start_time=time(11, 0),
                end_time=time(13, 0),
                notes="Explore Takeshita Street and surrounding shops.",
                location="Harajuku",
                address="Harajuku, Shibuya City, Tokyo, Japan",
                created_by=jordan.id,
                trip_id=trip.id
            ),
            Activity(
                name="Shinjuku Gyoen",
                date=date(2026, 10, 14),
                start_time=time(14, 0),
                end_time=time(16, 30),
                notes="Walk through the gardens and relax.",
                location="Shinjuku Gyoen National Garden",
                address="11 Naitomachi, Shinjuku City, Tokyo, Japan",
                created_by=sam.id,
                trip_id=trip.id
            ),
            Activity(
                name="Mount Fuji Day Trip",
                date=date(2026, 10, 15),
                start_time=time(7, 0),
                end_time=time(18, 0),
                notes="Full-day trip to Mount Fuji.",
                location="Mount Fuji",
                address="Mount Fuji, Japan",
                created_by=alex.id,
                trip_id=trip.id
            ),
            Activity(
                name="Tsukiji Outer Market",
                date=date(2026, 10, 16),
                start_time=time(9, 0),
                end_time=time(11, 0),
                notes="Explore the market and try local seafood.",
                location="Tsukiji Outer Market",
                address="4 Chome-16-2 Tsukiji, Chuo City, Tokyo, Japan",
                created_by=sam.id,
                trip_id=trip.id
            ),
            Activity(
                name="Imperial Palace",
                date=date(2026, 10, 16),
                start_time=time(12, 0),
                end_time=time(14, 0),
                notes="Explore the Imperial Palace grounds.",
                location="Imperial Palace",
                address="1-1 Chiyoda, Chiyoda City, Tokyo, Japan",
                created_by=jordan.id,
                trip_id=trip.id
            ),
            Activity(
                name="Tokyo Night Tour",
                date=date(2026, 10, 16),
                start_time=time(19, 0),
                end_time=time(22, 0),
                notes="Explore Tokyo's nightlife.",
                location="Shinjuku",
                address="Shinjuku, Tokyo, Japan",
                created_by=alex.id,
                trip_id=trip.id
            ),
            Activity(
                name="Final Shopping",
                date=date(2026, 10, 17),
                start_time=time(9, 0),
                end_time=time(11, 30),
                notes="Last-minute shopping and souvenirs.",
                location="Shibuya",
                address="Shibuya, Tokyo, Japan",
                created_by=sam.id,
                trip_id=trip.id
            ),
            Activity(
                name="Return to Narita Airport",
                date=date(2026, 10, 17),
                start_time=time(14, 0),
                end_time=time(15, 30),
                notes="Travel from Tokyo to Narita Airport.",
                location="Narita International Airport",
                address="1-1 Furugome, Narita, Chiba 282-0004, Japan",
                created_by=alex.id,
                trip_id=trip.id
            )
        ]

        db.session.add_all(activities)
        db.session.commit()

        print("Database seeded successfully.")
        print()
        print(f"Users: {User.query.count()}")
        print(f"Consultants: {Consultant.query.count()}")
        print(f"Trips: {Trip.query.count()}")
        print(f"Activities: {Activity.query.count()}")
        print(f"Flights: {Flight.query.count()}")
        print(f"Accommodations: {Accommodation.query.count()}")
        print(f"Other bookings: {Other.query.count()}")
        print(f"Tours: {Tour.query.count()}")
        print(f"Cruises: {Cruise.query.count()}")
        print(f"Budgets: {Budget.query.count()}")
        print()

        for flight in Flight.query.all():
            print(
                f"Flight: {flight.name} | "
                f"{flight.departure_airport} → {flight.arrival_airport} | "
                f"Consultant: {flight.consultant.name}"
            )

        for accommodation in Accommodation.query.all():
            print(
                f"Accommodation: {accommodation.name} | "
                f"Consultant: {accommodation.consultant.name}"
            )

        for other in Other.query.all():
            print(
                f"Other: {other.name} | "
                f"Consultant: {other.consultant.name}"
            )

        for tour in Tour.query.all():
            print(
                f"Tour: {tour.name} | "
                f"Consultant: {tour.consultant.name}"
            )

        for cruise in Cruise.query.all():
            print(
                f"Cruise: {cruise.name} | "
                f"{cruise.boarding_location} → {cruise.drop_off_location} | "
                f"Consultant: {cruise.consultant.name}"
            )


if __name__ == "__main__":
    seed_database()