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

        # ============================================================
        # USERS
        # ============================================================

        alex = User(
            name="Alex Morgan",
            email="alex.morgan@example.com",
            password=generate_password_hash("Test123!"),
            password_changed=True
        )

        sam = User(
            name="Sam Taylor",
            email="sam.taylor@example.com",
            password=generate_password_hash("Test123!"),
            password_changed=False
        )

        jordan = User(
            name="Jordan Lee",
            email="jordan.lee@example.com",
            password=generate_password_hash("Test123!"),
            password_changed=False
        )

        emily = User(
            name="Emily Carter",
            email="emily.carter@example.com",
            password=generate_password_hash("Test123!"),
            password_changed=True
        )

        liam = User(
            name="Liam Wilson",
            email="liam.wilson@example.com",
            password=generate_password_hash("Test123!"),
            password_changed=False
        )

        mia = User(
            name="Mia Anderson",
            email="mia.anderson@example.com",
            password=generate_password_hash("Test123!"),
            password_changed=True
        )

        db.session.add_all([
            alex,
            sam,
            jordan,
            emily,
            liam,
            mia
        ])
        db.session.commit()

        # ============================================================
        # CONSULTANTS
        # ============================================================

        sarah = Consultant(
            name="Sarah Jenkins",
            email="sarah.jenkins@flightcentre.com.au"
        )

        daniel = Consultant(
            name="Daniel Kim",
            email="daniel.kim@flightcentre.com.au"
        )

        priya = Consultant(
            name="Priya Shah",
            email="priya.shah@flightcentre.com.au"
        )

        michael = Consultant(
            name="Michael Thompson",
            email="michael.thompson@flightcentre.com.au"
        )

        db.session.add_all([
            sarah,
            daniel,
            priya,
            michael
        ])
        db.session.commit()

        # ============================================================
        # TRIP 1 - UPCOMING GROUP TRIP
        # ============================================================

        tokyo_trip = Trip(
            name="Tokyo Adventure",
            start_date=date(2026, 10, 10),
            end_date=date(2026, 10, 17),
            timezone_id="Asia/Tokyo",
            whiteboard=(
                "Tokyo ideas: Shibuya, Harajuku, teamLab, "
                "Mount Fuji and late-night ramen."
            ),
            consultant=sarah,
            users=[alex, sam, jordan]
        )

        # ============================================================
        # TRIP 2 - PAST GROUP TRIP
        # ============================================================

        melbourne_trip = Trip(
            name="Melbourne Food & Culture",
            start_date=date(2026, 6, 12),
            end_date=date(2026, 6, 15),
            timezone_id="Australia/Melbourne",
            whiteboard=(
                "Queen Victoria Market, NGV, laneway restaurants "
                "and coffee spots."
            ),
            consultant=daniel,
            users=[alex, sam]
        )

        # ============================================================
        # TRIP 3 - UPCOMING SOLO TRIP
        # ============================================================

        seoul_trip = Trip(
            name="Seoul Solo Escape",
            start_date=date(2026, 11, 5),
            end_date=date(2026, 11, 11),
            timezone_id="Asia/Seoul",
            whiteboard=(
                "Hongdae, Seoul Forest, cafes, vinyl shops "
                "and Gyeongbokgung."
            ),
            consultant=priya,
            users=[alex]
        )

        # ============================================================
        # TRIP 4 - UPCOMING GROUP TRIP
        # ============================================================

        singapore_trip = Trip(
            name="Singapore Friends Getaway",
            start_date=date(2026, 12, 4),
            end_date=date(2026, 12, 8),
            timezone_id="Asia/Singapore",
            whiteboard=(
                "Gardens by the Bay, Sentosa, hawker centres, "
                "Marina Bay and Chinatown."
            ),
            consultant=michael,
            users=[emily, liam, mia]
        )

        db.session.add_all([
            tokyo_trip,
            melbourne_trip,
            seoul_trip,
            singapore_trip
        ])

        db.session.commit()

        # ============================================================
        # BUDGETS
        # ============================================================

        tokyo_budget = Budget(
            name="Tokyo Travel Fund",
            total_amount=5000,
            trip_id=tokyo_trip.id,
            updated_by=alex.id
        )

        melbourne_budget = Budget(
            name="Melbourne Weekend Fund",
            total_amount=2200,
            trip_id=melbourne_trip.id,
            updated_by=sam.id
        )

        seoul_budget = Budget(
            name="Seoul Solo Fund",
            total_amount=3500,
            trip_id=seoul_trip.id,
            updated_by=alex.id
        )

        singapore_budget = Budget(
            name="Singapore Group Fund",
            total_amount=4200,
            trip_id=singapore_trip.id,
            updated_by=emily.id
        )

        db.session.add_all([
            tokyo_budget,
            melbourne_budget,
            seoul_budget,
            singapore_budget
        ])

        db.session.commit()

        # ============================================================
        # TOKYO BOOKINGS
        # ============================================================

        tokyo_flight_out = Flight(
            name="Outbound Flight - Brisbane to Tokyo",
            cost=980,
            location="Brisbane Airport",
            address="1 Airport Dr, Brisbane QLD 4008, Australia",
            timezone_id="Australia/Brisbane",
            updated_by=alex.id,
            trip_id=tokyo_trip.id,
            consultant=sarah,

            departure_airport="BNE",
            departure_address="1 Airport Dr, Brisbane QLD 4008, Australia",
            arrival_airport="NRT",
            arrival_address="1-1 Furugome, Narita, Chiba 282-0004, Japan",

            departure_timezone_id="Australia/Brisbane",

            flight_number="JQ15",
            departure_time=datetime(2026, 10, 10, 9, 30),
            arrival_time=datetime(2026, 10, 11, 17, 20)
        )

        tokyo_flight_return = Flight(
            name="Return Flight - Tokyo to Brisbane",
            cost=920,
            location="Narita International Airport",
            address="1-1 Furugome, Narita, Chiba 282-0004, Japan",
            timezone_id="Asia/Tokyo",
            updated_by=alex.id,
            trip_id=tokyo_trip.id,
            consultant=sarah,

            departure_airport="NRT",
            departure_address="1-1 Furugome, Narita, Chiba 282-0004, Japan",
            arrival_airport="BNE",
            arrival_address="1 Airport Dr, Brisbane QLD 4008, Australia",

            departure_timezone_id="Asia/Tokyo",

            flight_number="JQ16",
            departure_time=datetime(2026, 10, 17, 19, 0),
            arrival_time=datetime(2026, 10, 18, 5, 20)
        )

        tokyo_hotel = Accommodation(
            name="Shinjuku Park Hotel",
            cost=1400,
            location="Shinjuku",
            address="3-7-1 Nishi-Shinjuku, Shinjuku City, Tokyo, Japan",
            timezone_id="Asia/Tokyo",
            updated_by=sam.id,
            trip_id=tokyo_trip.id,
            consultant=sarah,

            check_in=datetime(2026, 10, 11, 15, 0),
            check_out=datetime(2026, 10, 17, 11, 0),
            room_capacity=3,
            rating=4,
            contact_email="reservations@shinjukupark.example",
            contact_phone="+81 3 5550 1842"
        )

        jr_pass = Other(
            name="Japan Rail Pass",
            cost=500,
            location="Tokyo Station",
            address="1 Chome Marunouchi, Chiyoda City, Tokyo, Japan",
            timezone_id="Asia/Tokyo",
            updated_by=alex.id,
            trip_id=tokyo_trip.id,
            consultant=sarah,
            start_time=datetime(2026, 10, 11, 16, 0),
            end_time=datetime(2026, 10, 17, 23, 59)
        )

        airport_transfer = Other(
            name="Narita Airport Transfer",
            cost=120,
            location="Narita International Airport",
            address="1-1 Furugome, Narita, Chiba 282-0004, Japan",
            timezone_id="Asia/Tokyo",
            updated_by=sam.id,
            trip_id=tokyo_trip.id,
            consultant=sarah,
            start_time=datetime(2026, 10, 11, 17, 30),
            end_time=datetime(2026, 10, 11, 19, 0)
        )

        dinner_booking = Other(
            name="Shibuya Dinner Reservation",
            cost=180,
            location="Shibuya",
            address="Shibuya, Tokyo, Japan",
            timezone_id="Asia/Tokyo",
            updated_by=jordan.id,
            trip_id=tokyo_trip.id,
            consultant=sarah,
            start_time=datetime(2026, 10, 12, 19, 0),
            end_time=datetime(2026, 10, 12, 21, 0)
        )

        tokyo_food_tour = Tour(
            name="Tokyo Food Tour",
            cost=150,
            location="Tsukiji",
            address="Tsukiji, Chuo City, Tokyo, Japan",
            timezone_id="Asia/Tokyo",
            updated_by=alex.id,
            trip_id=tokyo_trip.id,
            consultant=sarah,
            start_time=datetime(2026, 10, 13, 18, 0),
            end_time=datetime(2026, 10, 13, 21, 0)
        )

        tokyo_walking_tour = Tour(
            name="Asakusa Walking Tour",
            cost=100,
            location="Asakusa",
            address="Asakusa, Taito City, Tokyo, Japan",
            timezone_id="Asia/Tokyo",
            updated_by=sam.id,
            trip_id=tokyo_trip.id,
            consultant=sarah,
            start_time=datetime(2026, 10, 14, 10, 30),
            end_time=datetime(2026, 10, 14, 13, 0)
        )

        tokyo_bay_cruise = Cruise(
            name="Tokyo Bay Dinner Cruise",
            cost=250,
            location="Tokyo Bay",
            address="Tokyo Bay, Tokyo, Japan",
            timezone_id="Asia/Tokyo",
            updated_by=jordan.id,
            trip_id=tokyo_trip.id,
            consultant=sarah,

            start_date=datetime(2026, 10, 15, 18, 0),
            end_date=datetime(2026, 10, 15, 21, 0),

            boarding_location="Hinode Pier",
            boarding_address="1-7 Kaigan, Minato City, Tokyo, Japan",

            drop_off_location="Hinode Pier",
            drop_off_address="1-7 Kaigan, Minato City, Tokyo, Japan",

            cruise_line="Tokyo Bay Cruise"
        )

        db.session.add_all([
            tokyo_flight_out,
            tokyo_flight_return,
            tokyo_hotel,
            jr_pass,
            airport_transfer,
            dinner_booking,
            tokyo_food_tour,
            tokyo_walking_tour,
            tokyo_bay_cruise
        ])

        db.session.commit()

        # ============================================================
        # MELBOURNE BOOKINGS - PAST
        # ============================================================

        melbourne_flight_out = Flight(
            name="Brisbane to Melbourne",
            cost=220,
            location="Brisbane Airport",
            address="1 Airport Dr, Brisbane QLD 4008, Australia",
            timezone_id="Australia/Brisbane",
            updated_by=sam.id,
            trip_id=melbourne_trip.id,
            consultant=daniel,

            departure_airport="BNE",
            departure_address="1 Airport Dr, Brisbane QLD 4008, Australia",
            arrival_airport="MEL",
            arrival_address="Arrival Dr, Melbourne VIC 3045, Australia",

            departure_timezone_id="Australia/Brisbane",

            flight_number="VA321",
            departure_time=datetime(2026, 6, 12, 8, 0),
            arrival_time=datetime(2026, 6, 12, 10, 20)
        )

        melbourne_flight_return = Flight(
            name="Melbourne to Brisbane",
            cost=220,
            location="Melbourne Airport",
            address="Arrival Dr, Melbourne VIC 3045, Australia",
            timezone_id="Australia/Melbourne",
            updated_by=alex.id,
            trip_id=melbourne_trip.id,
            consultant=daniel,

            departure_airport="MEL",
            departure_address="Arrival Dr, Melbourne VIC 3045, Australia",
            arrival_airport="BNE",
            arrival_address="1 Airport Dr, Brisbane QLD 4008, Australia",

            departure_timezone_id="Australia/Melbourne",

            flight_number="VA334",
            departure_time=datetime(2026, 6, 15, 18, 0),
            arrival_time=datetime(2026, 6, 15, 20, 15)
        )

        melbourne_hotel = Accommodation(
            name="The Langham Melbourne",
            cost=720,
            location="Southbank",
            address="1 Southgate Ave, Southbank VIC 3006, Australia",
            timezone_id="Australia/Melbourne",
            updated_by=sam.id,
            trip_id=melbourne_trip.id,
            consultant=daniel,

            check_in=datetime(2026, 6, 12, 14, 0),
            check_out=datetime(2026, 6, 15, 11, 0),
            room_capacity=2,
            rating=5,
            contact_email="reservations@langham.example",
            contact_phone="+61 3 5550 2100"
        )

        melbourne_tour = Tour(
            name="Melbourne Laneway Food Tour",
            cost=130,
            location="Melbourne CBD",
            address="Melbourne CBD, VIC, Australia",
            timezone_id="Australia/Melbourne",
            updated_by=alex.id,
            trip_id=melbourne_trip.id,
            consultant=daniel,
            start_time=datetime(2026, 6, 13, 11, 0),
            end_time=datetime(2026, 6, 13, 14, 0)
        )

        melbourne_other = Other(
            name="NGV Entry",
            cost=60,
            location="National Gallery of Victoria",
            address="180 St Kilda Rd, Melbourne VIC 3006, Australia",
            timezone_id="Australia/Melbourne",
            updated_by=sam.id,
            trip_id=melbourne_trip.id,
            consultant=daniel,
            start_time=datetime(2026, 6, 14, 13, 0),
            end_time=datetime(2026, 6, 14, 16, 0)
        )

        melbourne_cruise = Cruise(
            name="Yarra River Evening Cruise",
            cost=85,
            location="Yarra River",
            address="Southbank, Melbourne VIC 3006, Australia",
            timezone_id="Australia/Melbourne",
            updated_by=alex.id,
            trip_id=melbourne_trip.id,
            consultant=daniel,

            start_date=datetime(2026, 6, 14, 18, 0),
            end_date=datetime(2026, 6, 14, 20, 0),

            boarding_location="Southbank Promenade",
            boarding_address="Southbank Promenade, Southbank VIC 3006, Australia",

            drop_off_location="Southbank Promenade",
            drop_off_address="Southbank Promenade, Southbank VIC 3006, Australia",

            cruise_line="Melbourne River Cruises"
        )

        db.session.add_all([
            melbourne_flight_out,
            melbourne_flight_return,
            melbourne_hotel,
            melbourne_tour,
            melbourne_other,
            melbourne_cruise
        ])

        db.session.commit()

        # ============================================================
        # SEOUL BOOKINGS - SOLO
        # ============================================================

        seoul_flight_out = Flight(
            name="Brisbane to Seoul",
            cost=780,
            location="Brisbane Airport",
            address="1 Airport Dr, Brisbane QLD 4008, Australia",
            timezone_id="Australia/Brisbane",
            updated_by=alex.id,
            trip_id=seoul_trip.id,
            consultant=priya,

            departure_airport="BNE",
            departure_address="1 Airport Dr, Brisbane QLD 4008, Australia",
            arrival_airport="ICN",
            arrival_address="272 Gonghang-ro, Jung-gu, Incheon, South Korea",

            departure_timezone_id="Australia/Brisbane",

            flight_number="KE408",
            departure_time=datetime(2026, 11, 5, 8, 30),
            arrival_time=datetime(2026, 11, 5, 18, 0)
        )

        seoul_flight_return = Flight(
            name="Seoul to Brisbane",
            cost=780,
            location="Incheon International Airport",
            address="272 Gonghang-ro, Jung-gu, Incheon, South Korea",
            timezone_id="Asia/Seoul",
            updated_by=alex.id,
            trip_id=seoul_trip.id,
            consultant=priya,

            departure_airport="ICN",
            departure_address="272 Gonghang-ro, Jung-gu, Incheon, South Korea",
            arrival_airport="BNE",
            arrival_address="1 Airport Dr, Brisbane QLD 4008, Australia",

            departure_timezone_id="Asia/Seoul",

            flight_number="KE407",
            departure_time=datetime(2026, 11, 11, 19, 30),
            arrival_time=datetime(2026, 11, 12, 5, 30)
        )

        seoul_hotel = Accommodation(
            name="Hongdae Design Hotel",
            cost=900,
            location="Hongdae",
            address="Hongik-ro, Mapo-gu, Seoul, South Korea",
            timezone_id="Asia/Seoul",
            updated_by=alex.id,
            trip_id=seoul_trip.id,
            consultant=priya,

            check_in=datetime(2026, 11, 5, 15, 0),
            check_out=datetime(2026, 11, 11, 11, 0),
            room_capacity=1,
            rating=4,
            contact_email="stay@hongdaedesign.example",
            contact_phone="+82 2 5550 2714"
        )

        seoul_cafe_tour = Tour(
            name="Seoul Cafe & Vinyl Tour",
            cost=110,
            location="Hongdae",
            address="Hongdae, Mapo-gu, Seoul, South Korea",
            timezone_id="Asia/Seoul",
            updated_by=alex.id,
            trip_id=seoul_trip.id,
            consultant=priya,
            start_time=datetime(2026, 11, 7, 14, 0),
            end_time=datetime(2026, 11, 7, 17, 0)
        )

        seoul_other = Other(
            name="DMZ Shuttle",
            cost=90,
            location="Seoul Station",
            address="405 Hangang-daero, Yongsan-gu, Seoul, South Korea",
            timezone_id="Asia/Seoul",
            updated_by=alex.id,
            trip_id=seoul_trip.id,
            consultant=priya,
            start_time=datetime(2026, 11, 9, 7, 0),
            end_time=datetime(2026, 11, 9, 18, 0)
        )

        db.session.add_all([
            seoul_flight_out,
            seoul_flight_return,
            seoul_hotel,
            seoul_cafe_tour,
            seoul_other
        ])

        db.session.commit()

        # ============================================================
        # SINGAPORE BOOKINGS - GROUP TRIP
        # ============================================================

        singapore_flight_out = Flight(
            name="Brisbane to Singapore",
            cost=620,
            location="Brisbane Airport",
            address="1 Airport Dr, Brisbane QLD 4008, Australia",
            timezone_id="Australia/Brisbane",
            updated_by=emily.id,
            trip_id=singapore_trip.id,
            consultant=michael,

            departure_airport="BNE",
            departure_address="1 Airport Dr, Brisbane QLD 4008, Australia",
            arrival_airport="SIN",
            arrival_address="Airport Blvd, Singapore 819642",

            departure_timezone_id="Australia/Brisbane",

            flight_number="SQ256",
            departure_time=datetime(2026, 12, 4, 9, 0),
            arrival_time=datetime(2026, 12, 4, 15, 20)
        )

        singapore_flight_return = Flight(
            name="Singapore to Brisbane",
            cost=590,
            location="Singapore Changi Airport",
            address="Airport Blvd, Singapore 819642",
            timezone_id="Asia/Singapore",
            updated_by=liam.id,
            trip_id=singapore_trip.id,
            consultant=michael,

            departure_airport="SIN",
            departure_address="Airport Blvd, Singapore 819642",
            arrival_airport="BNE",
            arrival_address="1 Airport Dr, Brisbane QLD 4008, Australia",

            departure_timezone_id="Asia/Singapore",

            flight_number="SQ245",
            departure_time=datetime(2026, 12, 8, 18, 30),
            arrival_time=datetime(2026, 12, 8, 4, 45)
        )

        singapore_hotel = Accommodation(
            name="Marina Bay City Hotel",
            cost=1100,
            location="Marina Bay",
            address="10 Bayfront Ave, Singapore 018956",
            timezone_id="Asia/Singapore",
            updated_by=emily.id,
            trip_id=singapore_trip.id,
            consultant=michael,

            check_in=datetime(2026, 12, 4, 15, 0),
            check_out=datetime(2026, 12, 8, 11, 0),
            room_capacity=3,
            rating=4,
            contact_email="stay@marinabaycity.example",
            contact_phone="+65 5550 3321"
        )

        singapore_tour = Tour(
            name="Singapore Street Food Tour",
            cost=120,
            location="Chinatown",
            address="Chinatown, Singapore",
            timezone_id="Asia/Singapore",
            updated_by=liam.id,
            trip_id=singapore_trip.id,
            consultant=michael,
            start_time=datetime(2026, 12, 5, 18, 0),
            end_time=datetime(2026, 12, 5, 21, 0)
        )

        singapore_sentosa = Tour(
            name="Sentosa Island Adventure",
            cost=180,
            location="Sentosa Island",
            address="Sentosa Island, Singapore",
            timezone_id="Asia/Singapore",
            updated_by=mia.id,
            trip_id=singapore_trip.id,
            consultant=michael,
            start_time=datetime(2026, 12, 6, 10, 0),
            end_time=datetime(2026, 12, 6, 17, 0)
        )

        singapore_cruise = Cruise(
            name="Marina Bay Sunset Cruise",
            cost=150,
            location="Marina Bay",
            address="Marina Bay, Singapore",
            timezone_id="Asia/Singapore",
            updated_by=emily.id,
            trip_id=singapore_trip.id,
            consultant=michael,

            start_date=datetime(2026, 12, 7, 18, 30),
            end_date=datetime(2026, 12, 7, 20, 30),

            boarding_location="Marina South Pier",
            boarding_address="31 Marina Coastal Dr, Singapore",

            drop_off_location="Marina South Pier",
            drop_off_address="31 Marina Coastal Dr, Singapore",

            cruise_line="Singapore Bay Cruises"
        )

        singapore_other = Other(
            name="Gardens by the Bay Entry",
            cost=75,
            location="Gardens by the Bay",
            address="18 Marina Gardens Dr, Singapore 018953",
            timezone_id="Asia/Singapore",
            updated_by=liam.id,
            trip_id=singapore_trip.id,
            consultant=michael,
            start_time=datetime(2026, 12, 5, 10, 0),
            end_time=datetime(2026, 12, 5, 13, 0)
        )

        db.session.add_all([
            singapore_flight_out,
            singapore_flight_return,
            singapore_hotel,
            singapore_tour,
            singapore_sentosa,
            singapore_cruise,
            singapore_other
        ])

        db.session.commit()

        # ============================================================
        # ACTIVITIES
        # ============================================================

        activities = [

            # ========================================================
            # TOKYO
            # ========================================================

            Activity(
                name="Arrive in Tokyo",
                date=date(2026, 10, 11),
                start_time=time(17, 20),
                end_time=time(18, 0),
                notes="Arrive at Narita Airport and collect luggage.",
                location="Narita International Airport",
                address="1-1 Furugome, Narita, Chiba 282-0004, Japan",
                timezone_id="Asia/Tokyo",
                created_by=alex.id,
                updated_by=alex.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Check in to Hotel",
                date=date(2026, 10, 11),
                start_time=time(19, 0),
                end_time=time(19, 30),
                notes="Check in and settle into the hotel.",
                location="Shinjuku",
                address="3-7-1 Nishi-Shinjuku, Shinjuku City, Tokyo, Japan",
                timezone_id="Asia/Tokyo",
                created_by=sam.id,
                updated_by=sam.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Visit Senso-ji Temple",
                date=date(2026, 10, 12),
                start_time=time(9, 0),
                end_time=time(11, 0),
                notes="Explore Tokyo's oldest temple.",
                location="Senso-ji Temple",
                address="2 Chome-3-1 Asakusa, Taito City, Tokyo, Japan",
                timezone_id="Asia/Tokyo",
                created_by=alex.id,
                updated_by=sam.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Shibuya Crossing",
                date=date(2026, 10, 12),
                start_time=time(14, 0),
                end_time=time(15, 0),
                notes="Visit the famous Shibuya Crossing.",
                location="Shibuya Crossing",
                address="2 Chome-24-1 Shibuya, Shibuya City, Tokyo, Japan",
                timezone_id="Asia/Tokyo",
                created_by=jordan.id,
                updated_by=alex.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="teamLab Planets",
                date=date(2026, 10, 12),
                start_time=time(15, 30),
                end_time=time(18, 0),
                notes="Visit the immersive digital art museum.",
                location="teamLab Planets TOKYO",
                address="6 Chome-1-16 Toyosu, Koto City, Tokyo, Japan",
                timezone_id="Asia/Tokyo",
                created_by=sam.id,
                updated_by=sam.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Tokyo Skytree",
                date=date(2026, 10, 13),
                start_time=time(9, 30),
                end_time=time(11, 30),
                notes="Visit the Tokyo Skytree observation decks.",
                location="Tokyo Skytree",
                address="1 Chome-1-2 Oshiage, Sumida City, Tokyo, Japan",
                timezone_id="Asia/Tokyo",
                created_by=alex.id,
                updated_by=alex.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Akihabara Shopping",
                date=date(2026, 10, 13),
                start_time=time(14, 0),
                end_time=time(17, 0),
                notes="Shop for electronics, games and anime merchandise.",
                location="Akihabara",
                address="Akihabara, Taito City, Tokyo, Japan",
                timezone_id="Asia/Tokyo",
                created_by=sam.id,
                updated_by=jordan.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Meiji Shrine",
                date=date(2026, 10, 14),
                start_time=time(8, 30),
                end_time=time(10, 30),
                notes="Visit the famous Shinto shrine.",
                location="Meiji Jingu",
                address="1-1 Yoyogikamizonocho, Shibuya City, Tokyo, Japan",
                timezone_id="Asia/Tokyo",
                created_by=alex.id,
                updated_by=alex.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Harajuku Exploration",
                date=date(2026, 10, 14),
                start_time=time(11, 0),
                end_time=time(13, 0),
                notes="Explore Takeshita Street and surrounding shops.",
                location="Harajuku",
                address="Harajuku, Shibuya City, Tokyo, Japan",
                timezone_id="Asia/Tokyo",
                created_by=jordan.id,
                updated_by=jordan.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Mount Fuji Day Trip",
                date=date(2026, 10, 15),
                start_time=time(7, 0),
                end_time=time(18, 0),
                notes="Full-day trip to Mount Fuji.",
                location="Mount Fuji",
                address="Mount Fuji, Japan",
                timezone_id="Asia/Tokyo",
                created_by=alex.id,
                updated_by=sam.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Tokyo Night Tour",
                date=date(2026, 10, 16),
                start_time=time(19, 0),
                end_time=time(22, 0),
                notes="Explore Tokyo's nightlife.",
                location="Shinjuku",
                address="Shinjuku, Tokyo, Japan",
                timezone_id="Asia/Tokyo",
                created_by=alex.id,
                updated_by=jordan.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Final Shopping",
                date=date(2026, 10, 17),
                start_time=time(9, 0),
                end_time=time(11, 30),
                notes="Last-minute shopping and souvenirs.",
                location="Shibuya",
                address="Shibuya, Tokyo, Japan",
                timezone_id="Asia/Tokyo",
                created_by=sam.id,
                updated_by=sam.id,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Ramen Dinner",
                date=date(2026, 10, 16),
                start_time=time(18, 0),
                end_time=time(19, 0),
                notes="Find a local ramen restaurant for dinner.",
                location="Shinjuku",
                address=None,
                timezone_id="Asia/Tokyo",
                created_by=jordan.id,
                updated_by=None,
                trip_id=tokyo_trip.id
            ),

            Activity(
                name="Free Evening",
                date=date(2026, 10, 16),
                start_time=None,
                end_time=None,
                notes="Decide on an activity closer to the date.",
                location=None,
                address=None,
                timezone_id="Asia/Tokyo",
                created_by=sam.id,
                updated_by=None,
                trip_id=tokyo_trip.id
            ),

            # ========================================================
            # MELBOURNE - PAST
            # ========================================================

            Activity(
                name="Arrive in Melbourne",
                date=date(2026, 6, 12),
                start_time=time(10, 20),
                end_time=time(11, 0),
                notes="Arrive at Melbourne Airport and collect luggage.",
                location="Melbourne Airport",
                address="Arrival Dr, Melbourne VIC 3045, Australia",
                timezone_id="Australia/Melbourne",
                created_by=alex.id,
                updated_by=alex.id,
                trip_id=melbourne_trip.id
            ),

            Activity(
                name="Queen Victoria Market",
                date=date(2026, 6, 12),
                start_time=time(13, 0),
                end_time=time(15, 0),
                notes="Explore the market and grab lunch.",
                location="Queen Victoria Market",
                address="Queen St, Melbourne VIC 3000, Australia",
                timezone_id="Australia/Melbourne",
                created_by=sam.id,
                updated_by=sam.id,
                trip_id=melbourne_trip.id
            ),

            Activity(
                name="Southbank Walk",
                date=date(2026, 6, 12),
                start_time=time(16, 0),
                end_time=time(17, 30),
                notes="Walk along the Yarra River and Southbank.",
                location="Southbank",
                address="Southbank Promenade, Southbank VIC 3006, Australia",
                timezone_id="Australia/Melbourne",
                created_by=alex.id,
                updated_by=sam.id,
                trip_id=melbourne_trip.id
            ),

            Activity(
                name="Laneway Dinner",
                date=date(2026, 6, 13),
                start_time=time(19, 0),
                end_time=time(21, 0),
                notes="Dinner at one of Melbourne's laneway restaurants.",
                location="Melbourne CBD",
                address="Melbourne CBD, VIC, Australia",
                timezone_id="Australia/Melbourne",
                created_by=alex.id,
                updated_by=sam.id,
                trip_id=melbourne_trip.id
            ),

            Activity(
                name="National Gallery of Victoria",
                date=date(2026, 6, 14),
                start_time=time(13, 0),
                end_time=time(16, 0),
                notes="Visit the NGV.",
                location="National Gallery of Victoria",
                address="180 St Kilda Rd, Melbourne VIC 3006, Australia",
                timezone_id="Australia/Melbourne",
                created_by=sam.id,
                updated_by=alex.id,
                trip_id=melbourne_trip.id
            ),

            Activity(
                name="Coffee Crawl",
                date=date(2026, 6, 15),
                start_time=time(7, 30),
                end_time=time(9, 0),
                notes="Try a few Melbourne specialty coffee spots before the flight.",
                location="Melbourne CBD",
                address=None,
                timezone_id="Australia/Melbourne",
                created_by=alex.id,
                updated_by=None,
                trip_id=melbourne_trip.id
            ),

            # ========================================================
            # SEOUL - SOLO
            # ========================================================

            Activity(
                name="Arrive in Seoul",
                date=date(2026, 11, 5),
                start_time=time(18, 0),
                end_time=time(19, 0),
                notes="Arrive at Incheon Airport and travel to the hotel.",
                location="Incheon International Airport",
                address="272 Gonghang-ro, Jung-gu, Incheon, South Korea",
                timezone_id="Asia/Seoul",
                created_by=alex.id,
                updated_by=alex.id,
                trip_id=seoul_trip.id
            ),

            Activity(
                name="Explore Hongdae",
                date=date(2026, 11, 6),
                start_time=time(10, 0),
                end_time=time(14, 0),
                notes="Explore independent shops, cafes and street performances.",
                location="Hongdae",
                address="Hongdae, Mapo-gu, Seoul, South Korea",
                timezone_id="Asia/Seoul",
                created_by=alex.id,
                updated_by=alex.id,
                trip_id=seoul_trip.id
            ),

            Activity(
                name="Seoul Forest",
                date=date(2026, 11, 7),
                start_time=time(9, 0),
                end_time=time(12, 0),
                notes="Morning walk through Seoul Forest.",
                location="Seoul Forest",
                address="273 Ttukseom-ro, Seongdong-gu, Seoul, South Korea",
                timezone_id="Asia/Seoul",
                created_by=alex.id,
                updated_by=alex.id,
                trip_id=seoul_trip.id
            ),

            Activity(
                name="Vinyl Shopping",
                date=date(2026, 11, 7),
                start_time=time(14, 0),
                end_time=time(17, 0),
                notes="Browse independent record stores around Hongdae.",
                location="Hongdae",
                address="Hongdae, Mapo-gu, Seoul, South Korea",
                timezone_id="Asia/Seoul",
                created_by=alex.id,
                updated_by=alex.id,
                trip_id=seoul_trip.id
            ),

            Activity(
                name="Gyeongbokgung Palace",
                date=date(2026, 11, 8),
                start_time=time(10, 0),
                end_time=time(13, 0),
                notes="Explore the palace and surrounding historical district.",
                location="Gyeongbokgung Palace",
                address="161 Sajik-ro, Jongno-gu, Seoul, South Korea",
                timezone_id="Asia/Seoul",
                created_by=alex.id,
                updated_by=alex.id,
                trip_id=seoul_trip.id
            ),

            Activity(
                name="Han River Evening",
                date=date(2026, 11, 10),
                start_time=time(18, 0),
                end_time=time(21, 0),
                notes="Relax by the Han River before the final day.",
                location="Han River",
                address="Yeouido, Seoul, South Korea",
                timezone_id="Asia/Seoul",
                created_by=alex.id,
                updated_by=alex.id,
                trip_id=seoul_trip.id
            ),

            Activity(
                name="Cafe Recommendation",
                date=date(2026, 11, 9),
                start_time=None,
                end_time=None,
                notes="Find a quiet cafe to work from.",
                location="Seongsu",
                address=None,
                timezone_id="Asia/Seoul",
                created_by=alex.id,
                updated_by=None,
                trip_id=seoul_trip.id
            ),

            # ========================================================
            # SINGAPORE - GROUP
            # ========================================================

            Activity(
                name="Arrive in Singapore",
                date=date(2026, 12, 4),
                start_time=time(15, 20),
                end_time=time(16, 30),
                notes="Arrive at Changi Airport and collect luggage.",
                location="Singapore Changi Airport",
                address="Airport Blvd, Singapore 819642",
                timezone_id="Asia/Singapore",
                created_by=emily.id,
                updated_by=emily.id,
                trip_id=singapore_trip.id
            ),

            Activity(
                name="Hotel Check-in",
                date=date(2026, 12, 4),
                start_time=time(17, 0),
                end_time=time(17, 30),
                notes="Check into the hotel and drop off luggage.",
                location="Marina Bay",
                address="10 Bayfront Ave, Singapore 018956",
                timezone_id="Asia/Singapore",
                created_by=liam.id,
                updated_by=liam.id,
                trip_id=singapore_trip.id
            ),

            Activity(
                name="Gardens by the Bay",
                date=date(2026, 12, 5),
                start_time=time(10, 0),
                end_time=time(13, 0),
                notes="Visit the Flower Dome and Cloud Forest.",
                location="Gardens by the Bay",
                address="18 Marina Gardens Dr, Singapore 018953",
                timezone_id="Asia/Singapore",
                created_by=emily.id,
                updated_by=liam.id,
                trip_id=singapore_trip.id
            ),

            Activity(
                name="Chinatown Food Tour",
                date=date(2026, 12, 5),
                start_time=time(18, 0),
                end_time=time(21, 0),
                notes="Try local dishes and hawker food.",
                location="Chinatown",
                address="Chinatown, Singapore",
                timezone_id="Asia/Singapore",
                created_by=liam.id,
                updated_by=mia.id,
                trip_id=singapore_trip.id
            ),

            Activity(
                name="Sentosa Island",
                date=date(2026, 12, 6),
                start_time=time(10, 0),
                end_time=time(17, 0),
                notes="Spend the day exploring Sentosa.",
                location="Sentosa Island",
                address="Sentosa Island, Singapore",
                timezone_id="Asia/Singapore",
                created_by=mia.id,
                updated_by=mia.id,
                trip_id=singapore_trip.id
            ),

            Activity(
                name="Marina Bay Evening",
                date=date(2026, 12, 7),
                start_time=time(18, 30),
                end_time=time(21, 0),
                notes="Watch the sunset and explore Marina Bay.",
                location="Marina Bay",
                address="Marina Bay, Singapore",
                timezone_id="Asia/Singapore",
                created_by=emily.id,
                updated_by=liam.id,
                trip_id=singapore_trip.id
            ),

            Activity(
                name="Last Minute Shopping",
                date=date(2026, 12, 8),
                start_time=None,
                end_time=None,
                notes="Leave the morning open for shopping.",
                location="Orchard Road",
                address="Orchard Road, Singapore",
                timezone_id="Asia/Singapore",
                created_by=mia.id,
                updated_by=None,
                trip_id=singapore_trip.id
            )
        ]

        db.session.add_all(activities)
        db.session.commit()

        # ============================================================
        # OUTPUT / VERIFICATION
        # ============================================================

        print("==============================================")
        print("Database seeded successfully.")
        print("==============================================")
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

        print("USERS")
        print("----------------------------------------------")

        for user in User.query.all():
            status = (
                "Password reset"
                if user.password_changed
                else "Password not reset"
            )

            print(
                f"{user.name} | "
                f"{user.email} | "
                f"{status}"
            )

        print()

        print("TRIPS")
        print("----------------------------------------------")

        for trip in Trip.query.all():
            trip_type = (
                "Solo"
                if len(trip.users) == 1
                else "Group"
            )

            status = (
                "Past"
                if trip.end_date < date.today()
                else "Upcoming"
            )

            print(
                f"{trip.name} | "
                f"{status} | "
                f"{trip_type} | "
                f"{trip.start_date} → {trip.end_date} | "
                f"Timezone: {trip.timezone_id} | "
                f"Consultant: {trip.consultant.name} | "
                f"Travellers: {', '.join(user.name for user in trip.users)}"
            )

        print()

        print("FLIGHTS")
        print("----------------------------------------------")

        for flight in Flight.query.all():
            print(
                f"{flight.name} | "
                f"{flight.departure_airport} → {flight.arrival_airport} | "
                f"Timezone: {flight.timezone_id} | "
                f"Departure timezone: {flight.departure_timezone_id} | "
                f"Consultant: {flight.consultant.name}"
            )

        print()

        print("ACCOMMODATIONS")
        print("----------------------------------------------")

        for accommodation in Accommodation.query.all():
            print(
                f"{accommodation.name} | "
                f"Timezone: {accommodation.timezone_id} | "
                f"Capacity: {accommodation.room_capacity} | "
                f"Rating: {accommodation.rating} | "
                f"Consultant: {accommodation.consultant.name}"
            )

        print()

        print("OTHER BOOKINGS")
        print("----------------------------------------------")

        for other in Other.query.all():
            print(
                f"{other.name} | "
                f"Timezone: {other.timezone_id} | "
                f"Consultant: {other.consultant.name}"
            )

        print()

        print("TOURS")
        print("----------------------------------------------")

        for tour in Tour.query.all():
            print(
                f"{tour.name} | "
                f"Timezone: {tour.timezone_id} | "
                f"Consultant: {tour.consultant.name}"
            )

        print()

        print("CRUISES")
        print("----------------------------------------------")

        for cruise in Cruise.query.all():
            print(
                f"{cruise.name} | "
                f"{cruise.boarding_location} → "
                f"{cruise.drop_off_location} | "
                f"Timezone: {cruise.timezone_id} | "
                f"Consultant: {cruise.consultant.name}"
            )

        print()

        print("ACTIVITIES")
        print("----------------------------------------------")

        for activity in Activity.query.all():
            updated_by = (
                activity.updated_by_user.name
                if activity.updated_by_user
                else "None"
            )

            print(
                f"{activity.name} | "
                f"Date: {activity.date} | "
                f"Timezone: {activity.timezone_id} | "
                f"Created by: {activity.created_by_user.name} | "
                f"Updated by: {updated_by}"
            )

        print()

        print("BUDGETS")
        print("----------------------------------------------")

        for budget in Budget.query.all():
            updated_by = (
                budget.updated_by_user.name
                if budget.updated_by_user
                else "None"
            )

            print(
                f"{budget.name} | "
                f"${budget.total_amount:.2f} | "
                f"Updated by: {updated_by}"
            )

        print()

        print("DEMO LOGIN DETAILS")
        print("----------------------------------------------")
        print("Alex Morgan:   alex.morgan@example.com / Test123!")
        print("Sam Taylor:    sam.taylor@example.com / Test123!")
        print("Jordan Lee:    jordan.lee@example.com / Test123!")
        print("Emily Carter:  emily.carter@example.com / Test123!")
        print("Liam Wilson:   liam.wilson@example.com / Test123!")
        print("Mia Anderson:  mia.anderson@example.com / Test123!")


if __name__ == "__main__":
    seed_database()