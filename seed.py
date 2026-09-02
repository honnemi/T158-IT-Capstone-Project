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
    Tours,
    Cruises,
    Budget
)


app = create_app()


def seed_database():
    with app.app_context():

        # ============================================================
        # CLEAR EXISTING DATA
        # ============================================================

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

        db.session.add_all([
            alex,
            sam,
            jordan
        ])

        db.session.commit()


        # ============================================================
        # 2. CONSULTANT
        # ============================================================

        consultant = Consultant(
            name="Sarah Jenkins",
            email="sarah@globetrottertravel.com"
        )

        db.session.add(consultant)
        db.session.commit()


        # ============================================================
        # 3. TRIP
        # ============================================================

        tokyo_trip = Trip(
            name="Tokyo Adventure",
            start_date=date(2026, 10, 10),
            end_date=date(2026, 10, 17),
            consultant_id=consultant.id
        )

        # Add users to trip
        tokyo_trip.users.extend([
            alex,
            sam,
            jordan
        ])

        db.session.add(tokyo_trip)
        db.session.commit()


        # ============================================================
        # 4. BUDGET
        # ============================================================

        trip_budget = Budget(
            name="Tokyo Travel Fund",
            total_amount=5000.00,
            trip_id=tokyo_trip.id
        )

        db.session.add(trip_budget)


        # ============================================================
        # 5. FLIGHTS
        # ============================================================

        flight_outbound = Flight(
            name="Outbound Flight - LAX to NRT",
            cost=850.00,
            trip_id=tokyo_trip.id,

            location="Narita International Airport",
            address="1-1 Furugome, Narita, Chiba 282-0004, Japan",

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

        flight_return = Flight(
            name="Return Flight - NRT to LAX",
            cost=850.00,
            trip_id=tokyo_trip.id,

            location="Narita International Airport",
            address="1-1 Furugome, Narita, Chiba 282-0004, Japan",

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

        # Assign consultant
        flight_outbound.consultants.append(consultant)
        flight_return.consultants.append(consultant)

        db.session.add_all([
            flight_outbound,
            flight_return
        ])


        # ============================================================
        # 6. ACCOMMODATION
        # ============================================================

        hotel = Accommodation(
            name="Shinjuku Park Hotel",
            cost=620.00,
            trip_id=tokyo_trip.id,

            location="Shinjuku, Tokyo",

            address=(
                "3-7-1 Nishi-Shinjuku, "
                "Shinjuku-ku, Tokyo, Japan"
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

        # Assign consultant
        hotel.consultants.append(consultant)

        db.session.add(hotel)


        # ============================================================
        # 7. OTHER BOOKINGS
        # ============================================================

        jr_pass = Other(
            name="Japan Rail Pass",
            cost=340.00,
            trip_id=tokyo_trip.id,

            location="Narita International Airport",
            address=(
                "1-1 Furugome, Narita, Chiba 282-0004, Japan"
            ),

            start_time=datetime(
                2026, 10, 11, 16, 00
            ),

            end_time=datetime(
                2026, 10, 17, 23, 59
            )
        )

        airport_transfer = Other(
            name="Airport Transfer",
            cost=80.00,
            trip_id=tokyo_trip.id,

            location="Narita Airport → Shinjuku",
            address=(
                "Narita International Airport, "
                "1-1 Furugome, Narita, Chiba, Japan"
            ),

            start_time=datetime(
                2026, 10, 11, 16, 00
            ),

            end_time=datetime(
                2026, 10, 11, 17, 30
            )
        )

        dinner_booking = Other(
            name="Shibuya Dinner Reservation",
            cost=120.00,
            trip_id=tokyo_trip.id,

            location="Shibuya, Tokyo",
            address=(
                "2-24-1 Shibuya, "
                "Shibuya-ku, Tokyo, Japan"
            ),

            start_time=datetime(
                2026, 10, 12, 19, 00
            ),

            end_time=datetime(
                2026, 10, 12, 21, 00
            )
        )

        # Assign consultant
        jr_pass.consultants.append(consultant)
        airport_transfer.consultants.append(consultant)
        dinner_booking.consultants.append(consultant)

        db.session.add_all([
            jr_pass,
            airport_transfer,
            dinner_booking
        ])


        # ============================================================
        # 8. TOURS
        # ============================================================

        tokyo_food_tour = Tours(
            name="Tokyo Food Tour",
            cost=150.00,
            trip_id=tokyo_trip.id,

            location="Shibuya, Tokyo",
            address=(
                "Shibuya Station, "
                "Shibuya City, Tokyo, Japan"
            ),

            start_time=datetime(
                2026, 10, 13, 18, 00
            ),

            end_time=datetime(
                2026, 10, 13, 21, 00
            )
        )

        tokyo_walking_tour = Tours(
            name="Tokyo Walking Tour",
            cost=90.00,
            trip_id=tokyo_trip.id,

            location="Asakusa, Tokyo",
            address=(
                "Senso-ji Temple, "
                "Asakusa, Tokyo, Japan"
            ),

            start_time=datetime(
                2026, 10, 14, 10, 30
            ),

            end_time=datetime(
                2026, 10, 14, 13, 00
            )
        )

        # Assign consultant
        tokyo_food_tour.consultants.append(consultant)
        tokyo_walking_tour.consultants.append(consultant)

        db.session.add_all([
            tokyo_food_tour,
            tokyo_walking_tour
        ])


        # ============================================================
        # 9. CRUISES
        # ============================================================

        tokyo_bay_cruise = Cruises(
            name="Tokyo Bay Dinner Cruise",
            cost=180.00,
            trip_id=tokyo_trip.id,

            location="Tokyo Bay",
            address=(
                "Hinode Pier, "
                "Minato City, Tokyo, Japan"
            ),

            startDate=datetime(
                2026, 10, 15, 18, 00
            ),

            endDate=datetime(
                2026, 10, 15, 21, 00
            ),

            boardingLocation="Hinode Pier",
            dropOffLocation="Hinode Pier",
            cruiseLine="Tokyo Bay Cruise"
        )

        japan_coastal_cruise = Cruises(
            name="Japan Coastal Cruise",
            cost=650.00,
            trip_id=tokyo_trip.id,

            location="Yokohama",
            address=(
                "Osanbashi Pier, "
                "Yokohama, Japan"
            ),

            startDate=datetime(
                2026, 10, 16, 8, 00
            ),

            endDate=datetime(
                2026, 10, 16, 20, 00
            ),

            boardingLocation="Yokohama Osanbashi Pier",
            dropOffLocation="Yokohama Osanbashi Pier",
            cruiseLine="Japan Coastal Cruises"
        )

        # Assign consultant
        tokyo_bay_cruise.consultants.append(consultant)
        japan_coastal_cruise.consultants.append(consultant)

        db.session.add_all([
            tokyo_bay_cruise,
            japan_coastal_cruise
        ])


        # ============================================================
        # 10. ACTIVITIES
        # ============================================================

        activities = [

            # --------------------------------------------------------
            # SUNDAY - OCTOBER 11
            # --------------------------------------------------------

            Activity(
                name="Arrive in Tokyo",
                date=date(2026, 10, 11),

                start_time=time(15, 25),
                end_time=time(16, 00),

                location="Narita International Airport",
                address=(
                    "1-1 Furugome, Narita, "
                    "Chiba 282-0004, Japan"
                ),

                notes=(
                    "Arrive at Narita Airport and collect luggage."
                ),

                created_by=alex.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Check in to Hotel",
                date=date(2026, 10, 11),

                start_time=time(17, 30),
                end_time=time(18, 00),

                location="Shinjuku Park Hotel",
                address=(
                    "3-7-1 Nishi-Shinjuku, "
                    "Shinjuku-ku, Tokyo, Japan"
                ),

                notes=(
                    "Check in and settle into the hotel."
                ),

                created_by=sam.id,
                trip_id=tokyo_trip.id
            ),


            # --------------------------------------------------------
            # MONDAY - OCTOBER 12
            # --------------------------------------------------------

            Activity(
                name="Visit Senso-ji Temple",
                date=date(2026, 10, 12),

                start_time=time(9, 00),
                end_time=time(11, 00),

                location="Senso-ji Temple",
                address=(
                    "2-3-1 Asakusa, "
                    "Taito City, Tokyo 111-0032, Japan"
                ),

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

                location="Nakamise Shopping Street",
                address=(
                    "1-36-3 Asakusa, "
                    "Taito City, Tokyo 111-0032, Japan"
                ),

                notes=(
                    "Try local street food and browse the market."
                ),

                created_by=sam.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Shibuya Crossing",
                date=date(2026, 10, 12),

                start_time=time(14, 00),
                end_time=time(15, 00),

                location="Shibuya Crossing",
                address=(
                    "2-24 Shibuya, "
                    "Shibuya City, Tokyo 150-0002, Japan"
                ),

                notes=(
                    "Visit the famous Shibuya Crossing."
                ),

                created_by=jordan.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="teamLab Planets",
                date=date(2026, 10, 12),

                start_time=time(15, 30),
                end_time=time(18, 00),

                location="teamLab Planets TOKYO",
                address=(
                    "6-1-16 Toyosu, "
                    "Koto City, Tokyo 135-0061, Japan"
                ),

                notes=(
                    "Tickets reserved for 15:30. "
                    "Wear easy-to-remove shoes."
                ),

                created_by=sam.id,
                trip_id=tokyo_trip.id
            ),


            # --------------------------------------------------------
            # TUESDAY - OCTOBER 13
            # --------------------------------------------------------

            Activity(
                name="Tokyo Skytree",
                date=date(2026, 10, 13),

                start_time=time(9, 30),
                end_time=time(11, 30),

                location="Tokyo Skytree",
                address=(
                    "1-1-2 Oshiage, "
                    "Sumida City, Tokyo 131-0045, Japan"
                ),

                notes=(
                    "Visit the observation deck."
                ),

                created_by=alex.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Lunch in Akihabara",
                date=date(2026, 10, 13),

                start_time=time(12, 00),
                end_time=time(13, 30),

                location="Akihabara",
                address=(
                    "Sotokanda, Chiyoda City, "
                    "Tokyo 101-0021, Japan"
                ),

                notes=(
                    "Lunch and explore Akihabara."
                ),

                created_by=jordan.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Akihabara Shopping",
                date=date(2026, 10, 13),

                start_time=time(14, 00),
                end_time=time(17, 00),

                location="Akihabara Electric Town",
                address=(
                    "Sotokanda, Chiyoda City, "
                    "Tokyo 101-0021, Japan"
                ),

                notes=(
                    "Explore electronics and anime stores."
                ),

                created_by=sam.id,
                trip_id=tokyo_trip.id
            ),


            # --------------------------------------------------------
            # WEDNESDAY - OCTOBER 14
            # --------------------------------------------------------

            Activity(
                name="Meiji Shrine",
                date=date(2026, 10, 14),

                start_time=time(8, 30),
                end_time=time(10, 30),

                location="Meiji Jingu",
                address=(
                    "1-1 Yoyogikamizonocho, "
                    "Shibuya City, Tokyo 151-8557, Japan"
                ),

                notes=(
                    "Morning visit to Meiji Shrine."
                ),

                created_by=alex.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Harajuku Exploration",
                date=date(2026, 10, 14),

                start_time=time(11, 00),
                end_time=time(13, 00),

                location="Takeshita Street",
                address=(
                    "1-17-1 Jingumae, "
                    "Shibuya City, Tokyo 150-0001, Japan"
                ),

                notes=(
                    "Explore Takeshita Street."
                ),

                created_by=jordan.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Shinjuku Gyoen",
                date=date(2026, 10, 14),

                start_time=time(14, 00),
                end_time=time(16, 30),

                location="Shinjuku Gyoen National Garden",
                address=(
                    "11 Naitomachi, "
                    "Shinjuku City, Tokyo 160-0014, Japan"
                ),

                notes=(
                    "Relax and explore the gardens."
                ),

                created_by=sam.id,
                trip_id=tokyo_trip.id
            ),


            # --------------------------------------------------------
            # THURSDAY - OCTOBER 15
            # --------------------------------------------------------

            Activity(
                name="Mount Fuji Day Trip",
                date=date(2026, 10, 15),

                start_time=time(7, 00),
                end_time=time(18, 00),

                location="Mount Fuji",
                address=(
                    "Fujisan, Kitayama, Fujinomiya, "
                    "Shizuoka 418-0112, Japan"
                ),

                notes=(
                    "Full-day trip to Mount Fuji."
                ),

                created_by=alex.id,
                trip_id=tokyo_trip.id
            ),


            # --------------------------------------------------------
            # FRIDAY - OCTOBER 16
            # --------------------------------------------------------

            Activity(
                name="Tsukiji Outer Market",
                date=date(2026, 10, 16),

                start_time=time(9, 00),
                end_time=time(11, 00),

                location="Tsukiji Outer Market",
                address=(
                    "4-16-2 Tsukiji, "
                    "Chuo City, Tokyo 104-0045, Japan"
                ),

                notes=(
                    "Breakfast and seafood market."
                ),

                created_by=sam.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Imperial Palace",
                date=date(2026, 10, 16),

                start_time=time(12, 00),
                end_time=time(14, 00),

                location="Imperial Palace",
                address=(
                    "1-1 Chiyoda, "
                    "Chiyoda City, Tokyo 100-8111, Japan"
                ),

                notes=(
                    "Explore the Imperial Palace grounds."
                ),

                created_by=jordan.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Tokyo Night Tour",
                date=date(2026, 10, 16),

                start_time=time(19, 00),
                end_time=time(22, 00),

                location="Shinjuku",
                address="Shinjuku City, Tokyo, Japan",

                notes=(
                    "Explore Tokyo nightlife."
                ),

                created_by=alex.id,
                trip_id=tokyo_trip.id
            ),


            # --------------------------------------------------------
            # SATURDAY - OCTOBER 17
            # --------------------------------------------------------

            Activity(
                name="Final Shopping",
                date=date(2026, 10, 17),

                start_time=time(9, 00),
                end_time=time(11, 30),

                location="Shinjuku",
                address="Shinjuku City, Tokyo, Japan",

                notes=(
                    "Last-minute shopping before departure."
                ),

                created_by=sam.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Return to Narita Airport",
                date=date(2026, 10, 17),

                start_time=time(14, 00),
                end_time=time(15, 30),

                location="Narita International Airport",
                address=(
                    "1-1 Furugome, Narita, "
                    "Chiba 282-0004, Japan"
                ),

                notes=(
                    "Travel to Narita Airport for return flight."
                ),

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


        # ============================================================
        # DISPLAY SEEDED DATA
        # ============================================================

        print("\nUSERS:")

        for user in User.query.all():
            print(
                user.id,
                user.name,
                user.email
            )


        print("\nCONSULTANTS:")

        for consultant in Consultant.query.all():
            print(
                consultant.id,
                consultant.name,
                consultant.email
            )


        print("\nTRIPS:")

        for trip in Trip.query.all():
            print(
                trip.id,
                trip.name,
                trip.start_date,
                trip.end_date,
                f"Consultant: {trip.consultant.name}",
                f"Users: {[user.name for user in trip.users]}"
            )


        print("\nBUDGETS:")

        for budget in Budget.query.all():
            print(
                budget.id,
                budget.name,
                budget.total_amount,
                budget.trip_id
            )


        print("\nFLIGHTS:")

        for flight in Flight.query.all():
            print(
                flight.id,
                flight.name,
                flight.flight_number,
                flight.departure_airport,
                flight.arrival_airport,
                flight.departure_time,
                flight.arrival_time,
                f"Consultants: {[c.name for c in flight.consultants]}"
            )


        print("\nACCOMMODATIONS:")

        for accommodation in Accommodation.query.all():
            print(
                accommodation.id,
                accommodation.name,
                accommodation.check_in,
                accommodation.check_out,
                accommodation.room_capacity,
                accommodation.rating,
                f"Consultants: {[c.name for c in accommodation.consultants]}"
            )


        print("\nOTHER BOOKINGS:")

        for other in Other.query.all():
            print(
                other.id,
                other.name,
                other.start_time,
                other.end_time,
                f"Consultants: {[c.name for c in other.consultants]}"
            )


        print("\nTOURS:")

        for tour in Tours.query.all():
            print(
                tour.id,
                tour.name,
                tour.start_time,
                tour.end_time,
                f"Consultants: {[c.name for c in tour.consultants]}"
            )


        print("\nCRUISES:")

        for cruise in Cruises.query.all():
            print(
                cruise.id,
                cruise.name,
                cruise.startDate,
                cruise.endDate,
                cruise.boardingLocation,
                cruise.dropOffLocation,
                cruise.cruiseLine,
                f"Consultants: {[c.name for c in cruise.consultants]}"
            )


        print("\nACTIVITIES:")

        for activity in Activity.query.all():
            print(
                activity.id,
                activity.name,
                activity.date,
                activity.start_time,
                activity.end_time,
                activity.location,
                activity.address,
                f"Created by: {activity.created_by_user.name}"
            )


if __name__ == "__main__":
    seed_database()
