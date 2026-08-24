from app import create_app, db
from app.auth import create_demo_user

app = create_app()

with app.app_context():
    db.create_all()
    create_demo_user()

if __name__ == "__main__":
    app.run(debug=True)