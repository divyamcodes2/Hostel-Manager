from flask import Blueprint, jsonify, session, request

from backend.app import db
from backend.models.user import User
from backend.models.room import Room


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/admin"
)


# ============================================================
# CREATE USER
# ============================================================

@admin_bp.route("/users", methods=["POST"])
def create_user():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "Not authenticated"
        }), 401

    admin = User.query.get(user_id)

    if not admin or not admin.active:

        session.clear()

        return jsonify({
            "error": "Not authenticated"
        }), 401

    if admin.role != "admin":

        return jsonify({
            "error": "Only admins can create users"
        }), 403

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Request body is required"
        }), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

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

    allowed_roles = [
        "student",
        "warden"
    ]

    if role not in allowed_roles:

        return jsonify({
            "error": "Invalid role",
            "allowed_roles": allowed_roles
        }), 400

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:

        return jsonify({
            "error": "Email already registered"
        }), 409

    user = User(
        name=name,
        email=email,
        role=role,
        active=True
    )

    user.set_password(password)

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


# ============================================================
# GET USERS
# ============================================================

@admin_bp.route("/users", methods=["GET"])
def get_users():

    user_id = session.get("user_id")

    if not user_id:

        return jsonify({
            "error": "Not authenticated"
        }), 401

    admin = User.query.get(user_id)

    if not admin or not admin.active:

        session.clear()

        return jsonify({
            "error": "Not authenticated"
        }), 401

    if admin.role != "admin":

        return jsonify({
            "error": "Only admins can view users"
        }), 403

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

            "created_at":
                user.created_at.isoformat()

        })

    return jsonify({
        "users": user_list
    }), 200


# ============================================================
# CREATE ROOM
# ============================================================

@admin_bp.route("/rooms", methods=["POST"])
def create_room():

    user_id = session.get("user_id")

    if not user_id:

        return jsonify({
            "error": "Not authenticated"
        }), 401

    admin = User.query.get(user_id)

    if not admin or not admin.active:

        session.clear()

        return jsonify({
            "error": "Not authenticated"
        }), 401

    if admin.role != "admin":

        return jsonify({
            "error": "Only admins can create rooms"
        }), 403

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Request body is required"
        }), 400

    hostel_block = data.get(
        "hostel_block"
    )

    room_number = data.get(
        "room_number"
    )

    capacity = data.get(
        "capacity"
    )

    if not hostel_block:

        return jsonify({
            "error": "Hostel block is required"
        }), 400

    if not room_number:

        return jsonify({
            "error": "Room number is required"
        }), 400

    if capacity is None:

        return jsonify({
            "error": "Capacity is required"
        }), 400

    try:

        capacity = int(capacity)

    except (TypeError, ValueError):

        return jsonify({
            "error": "Capacity must be a number"
        }), 400

    if capacity <= 0:

        return jsonify({
            "error": "Capacity must be greater than 0"
        }), 400

    hostel_block = str(
        hostel_block
    ).strip()

    room_number = str(
        room_number
    ).strip()

    if not hostel_block:

        return jsonify({
            "error": "Hostel block is required"
        }), 400

    if not room_number:

        return jsonify({
            "error": "Room number is required"
        }), 400

    existing_room = Room.query.filter_by(
        hostel_block=hostel_block,
        room_number=room_number
    ).first()

    if existing_room:

        return jsonify({
            "error": "This room already exists"
        }), 409

    room = Room(

        hostel_block=hostel_block,

        room_number=room_number,

        capacity=capacity

    )

    db.session.add(room)

    db.session.commit()

    return jsonify({

        "message":
            "Room created successfully",

        "room": {

            "id":
                room.id,

            "hostel_block":
                room.hostel_block,

            "room_number":
                room.room_number,

            "capacity":
                room.capacity,

            "occupied":
                0,

            "available":
                room.capacity

        }

    }), 201


# ============================================================
# GET ROOMS
# ============================================================

@admin_bp.route("/rooms", methods=["GET"])
def get_rooms():

    user_id = session.get("user_id")

    if not user_id:

        return jsonify({
            "error": "Not authenticated"
        }), 401

    admin = User.query.get(user_id)

    if not admin or not admin.active:

        session.clear()

        return jsonify({
            "error": "Not authenticated"
        }), 401

    if admin.role != "admin":

        return jsonify({
            "error": "Only admins can view rooms"
        }), 403

    rooms = Room.query.order_by(
        Room.id.asc()
    ).all()

    room_list = []

    for room in rooms:

        student_count = User.query.filter_by(

            room_id=room.id,

            role="student",

            active=True

        ).count()

        room_list.append({

            "id":
                room.id,

            "hostel_block":
                room.hostel_block,

            "room_number":
                room.room_number,

            "capacity":
                room.capacity,

            "occupied":
                student_count,

            "available":
                room.capacity - student_count

        })

    return jsonify({
        "rooms": room_list
    }), 200


# ============================================================
# ASSIGN / REMOVE STUDENT FROM ROOM
# ============================================================

@admin_bp.route(
    "/users/<int:user_id>/room",
    methods=["PATCH"]
)
def assign_room(user_id):

    admin_id = session.get(
        "user_id"
    )

    if not admin_id:

        return jsonify({
            "error": "Not authenticated"
        }), 401

    admin = User.query.get(
        admin_id
    )

    if not admin or not admin.active:

        session.clear()

        return jsonify({
            "error": "Not authenticated"
        }), 401

    if admin.role != "admin":

        return jsonify({
            "error": "Only admins can assign rooms"
        }), 403

    user = User.query.get(
        user_id
    )

    if not user:

        return jsonify({
            "error": "User not found"
        }), 404

    if user.role != "student":

        return jsonify({
            "error":
                "Only students can be assigned to rooms"
        }), 400

    data = request.get_json()

    if not data:

        return jsonify({
            "error":
                "Request body is required"
        }), 400

    room_id = data.get(
        "room_id"
    )

    # --------------------------------------------------------
    # REMOVE STUDENT FROM ROOM
    # --------------------------------------------------------

    if room_id is None:

        user.room_id = None

        db.session.commit()

        return jsonify({

            "message":
                "Student removed from room successfully",

            "user": {

                "id":
                    user.id,

                "name":
                    user.name,

                "room_id":
                    user.room_id

            }

        }), 200

    # --------------------------------------------------------
    # FIND ROOM
    # --------------------------------------------------------

    room = Room.query.get(
        room_id
    )

    if not room:

        return jsonify({
            "error": "Room not found"
        }), 404

    # --------------------------------------------------------
    # STUDENT ALREADY IN THIS ROOM
    # --------------------------------------------------------

    if user.room_id == room.id:

        return jsonify({

            "message":
                "Student is already assigned to this room",

            "user": {

                "id":
                    user.id,

                "name":
                    user.name,

                "room_id":
                    user.room_id

            }

        }), 200

    # --------------------------------------------------------
    # COUNT CURRENT STUDENTS
    # --------------------------------------------------------

    student_count = User.query.filter_by(

        room_id=room.id,

        role="student",

        active=True

    ).count()

    # --------------------------------------------------------
    # CHECK ROOM CAPACITY
    # --------------------------------------------------------

    if student_count >= room.capacity:

        return jsonify({
            "error": "Room is already full"
        }), 409

    # --------------------------------------------------------
    # ASSIGN STUDENT
    # --------------------------------------------------------

    user.room_id = room.id

    db.session.commit()

    return jsonify({

        "message":
            "Student assigned to room successfully",

        "user": {

            "id":
                user.id,

            "name":
                user.name,

            "room_id":
                user.room_id

        },

        "room": {

            "id":
                room.id,

            "hostel_block":
                room.hostel_block,

            "room_number":
                room.room_number

        }

    }), 200


# ============================================================
# UPDATE USER STATUS
# ============================================================

@admin_bp.route(
    "/users/<int:user_id>/status",
    methods=["PATCH"]
)
def update_user_status(user_id):

    admin_id = session.get(
        "user_id"
    )

    if not admin_id:

        return jsonify({
            "error": "Not authenticated"
        }), 401

    admin = User.query.get(
        admin_id
    )

    if not admin or not admin.active:

        session.clear()

        return jsonify({
            "error": "Not authenticated"
        }), 401

    if admin.role != "admin":

        return jsonify({
            "error":
                "Only admins can change user status"
        }), 403

    user = User.query.get(
        user_id
    )

    if not user:

        return jsonify({
            "error": "User not found"
        }), 404

    if user.id == admin.id:

        return jsonify({
            "error":
                "Admin cannot deactivate their own account"
        }), 400

    data = request.get_json()

    if not data:

        return jsonify({
            "error":
                "Request body is required"
        }), 400

    active = data.get(
        "active"
    )

    if active is None:

        return jsonify({
            "error":
                "Active status is required"
        }), 400

    if not isinstance(
        active,
        bool
    ):

        return jsonify({
            "error":
                "Active must be true or false"
        }), 400

    user.active = active

    db.session.commit()

    return jsonify({

        "message":
            "User status updated successfully",

        "user": {

            "id":
                user.id,

            "name":
                user.name,

            "email":
                user.email,

            "role":
                user.role,

            "active":
                user.active

        }

    }), 200
