from flask import Blueprint, jsonify, session, request

from backend.app import db
from backend.models.user import User
from backend.models.room import Room


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/admin"
)


@admin_bp.route("/users", methods=["POST"])
def create_user():
    # Get the ID of the currently logged-in user
    user_id = session.get("user_id")

    # User is not logged in
    if not user_id:
        return jsonify({
            "error": "Not authenticated"
        }), 401

    # Find the logged-in user
    admin = User.query.get(user_id)

    # Admin account doesn't exist or is inactive
    if not admin or not admin.active:
        session.clear()

        return jsonify({
            "error": "Not authenticated"
        }), 401

    # Only admins can create users
    if admin.role != "admin":
        return jsonify({
            "error": "Only admins can create users"
        }), 403

    # Get JSON request body
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    # Get required fields
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    # Validate required fields
    if not name:
        return jsonify({
            "error": "Name is required"
        }), 400

    if not email:
        return jsonify({
            "error": "Email is required"
        }), 400

    if not password:
        return jsonify({
            "error": "Password is required"
        }), 400

    if not role:
        return jsonify({
            "error": "Role is required"
        }), 400

    # Only allow student and warden accounts
    allowed_roles = [
        "student",
        "warden"
    ]

    if role not in allowed_roles:
        return jsonify({
            "error": "Invalid role",
            "allowed_roles": allowed_roles
        }), 400

    # Check whether email is already registered
    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            "error": "Email already registered"
        }), 409

    # Create the new user
    user = User(
        name=name,
        email=email,
        role=role,
        active=True
    )

    # Hash the password
    user.set_password(password)

    # Save user to database
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "active": user.active
        }
    }), 201


@admin_bp.route("/users", methods=["GET"])
def get_users():
    # Get the ID of the currently logged-in user
    user_id = session.get("user_id")

    # User is not logged in
    if not user_id:
        return jsonify({
            "error": "Not authenticated"
        }), 401

    # Find the logged-in user
    admin = User.query.get(user_id)

    # Admin account doesn't exist or is inactive
    if not admin or not admin.active:
        session.clear()

        return jsonify({
            "error": "Not authenticated"
        }), 401

    # Only admins can view users
    if admin.role != "admin":
        return jsonify({
            "error": "Only admins can view users"
        }), 403

    # Get all users
    users = User.query.order_by(
        User.id.asc()
    ).all()

    user_list = []

    for user in users:
        user_list.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "room_id": user.room_id,
            "active": user.active,
            "created_at": user.created_at.isoformat()
        })

    return jsonify({
        "users": user_list
    }), 200


@admin_bp.route("/rooms", methods=["GET"])
def get_rooms():
    # Get the ID of the currently logged-in user
    user_id = session.get("user_id")

    # User is not logged in
    if not user_id:
        return jsonify({
            "error": "Not authenticated"
        }), 401

    # Find the logged-in user
    admin = User.query.get(user_id)

    # Admin account doesn't exist or is inactive
    if not admin or not admin.active:
        session.clear()

        return jsonify({
            "error": "Not authenticated"
        }), 401

    # Only admins can view rooms
    if admin.role != "admin":
        return jsonify({
            "error": "Only admins can view rooms"
        }), 403

    # Get all rooms
    rooms = Room.query.order_by(
        Room.id.asc()
    ).all()

    room_list = []

    for room in rooms:
        # Count students currently assigned to this room
        student_count = User.query.filter_by(
            room_id=room.id,
            role="student",
            active=True
        ).count()

        room_list.append({
            "id": room.id,
            "hostel_block": room.hostel_block,
            "room_number": room.room_number,
            "capacity": room.capacity,
            "occupied": student_count,
            "available": room.capacity - student_count
        })

    return jsonify({
        "rooms": room_list
    }), 200


@admin_bp.route("/users/<int:user_id>/room", methods=["PATCH"])
def assign_room(user_id):
    # Get the ID of the currently logged-in admin
    admin_id = session.get("user_id")

    # Admin is not logged in
    if not admin_id:
        return jsonify({
            "error": "Not authenticated"
        }), 401

    # Find the logged-in admin
    admin = User.query.get(admin_id)

    # Admin account doesn't exist or is inactive
    if not admin or not admin.active:
        session.clear()

        return jsonify({
            "error": "Not authenticated"
        }), 401

    # Only admins can assign rooms
    if admin.role != "admin":
        return jsonify({
            "error": "Only admins can assign rooms"
        }), 403

    # Find the student
    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    # Only students can be assigned to rooms
    if user.role != "student":
        return jsonify({
            "error": "Only students can be assigned to rooms"
        }), 400

    # Get JSON request body
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    room_id = data.get("room_id")

    # Allow room_id to be null to remove a student from a room
    if room_id is None:
        user.room_id = None

        db.session.commit()

        return jsonify({
            "message": "Student removed from room successfully",
            "user": {
                "id": user.id,
                "name": user.name,
                "room_id": user.room_id
            }
        }), 200

    # Find the requested room
    room = Room.query.get(room_id)

    if not room:
        return jsonify({
            "error": "Room not found"
        }), 404

    # Count currently assigned students
    student_count = User.query.filter_by(
        room_id=room.id,
        role="student",
        active=True
    ).count()

    # If student is already in this room, don't count them again
    if user.room_id == room.id:
        return jsonify({
            "message": "Student is already assigned to this room",
            "user": {
                "id": user.id,
                "name": user.name,
                "room_id": user.room_id
            }
        }), 200

    # Check room capacity
    if student_count >= room.capacity:
        return jsonify({
            "error": "Room is already full"
        }), 409

    # Assign student to room
    user.room_id = room.id

    db.session.commit()

    return jsonify({
        "message": "Student assigned to room successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "room_id": user.room_id
        },
        "room": {
            "id": room.id,
            "hostel_block": room.hostel_block,
            "room_number": room.room_number
        }
    }), 200
