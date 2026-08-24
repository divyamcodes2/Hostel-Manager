from backend.app import db


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    hostel_block = db.Column(db.String(50), nullable=False)
    room_number = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    users = db.relationship("User", backref="room", lazy=True)
