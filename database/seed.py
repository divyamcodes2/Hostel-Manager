from backend.app import create_app, db
from backend.models.user import User
from backend.models.room import Room


app = create_app()


def seed_database():
    with app.app_context():

        if User.query.first():
            print("Database already contains users.")
            return

        room_101 = Room(
            hostel_block="A",
            room_number="101",
            capacity=3
        )

        room_102 = Room(
            hostel_block="A",
            room_number="102",
            capacity=3
        )

        db.session.add(room_101)
        db.session.add(room_102)

        db.session.flush()

        admin = User(
            name="Demo Admin",
            email="admin@example.com",
            role="admin",
            active=True
        )

        admin.set_password("Admin@123")

        student = User(
            name="Demo Student",
            email="student@example.com",
            role="student",
            room_id=room_101.id,
            active=True
        )

        student.set_password("student@123")

        warden = User(
            name="Demo Warden",
            email="warden@example.com",
            role="warden",
            active=True
        )

        warden.set_password("Warden@123")

        db.session.add(admin)
        db.session.add(student)
        db.session.add(warden)

        db.session.commit()

        print("Database seeded successfully.")
        print()
        print("Admin:   admin@example.com / Admin@123")
        print("Student: student@example.com / student@123")
        print("Warden:  warden@example.com / Warden@123")


if __name__ == "__main__":
    seed_database()
