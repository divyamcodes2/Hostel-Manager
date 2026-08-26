from flask import Blueprint, request, jsonify, session

from backend.models.user import User


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    if not user.active:
        return jsonify({
            "error": "Account is inactive"
        }), 403

    session.clear()

    session["user_id"] = user.id
    session["role"] = user.role

    room_data = None

    if user.room:
        room_data = {
            "id": user.room.id,
            "hostel_block": user.room.hostel_block,
            "room_number": user.room.room_number
        }

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "room_id": user.room_id,
            "room": room_data
        }
    }), 200


@auth_bp.route("/me", methods=["GET"])
def me():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "Not authenticated"
        }), 401

    user = User.query.get(user_id)

    if not user or not user.active:
        session.clear()

        return jsonify({
            "error": "Not authenticated"
        }), 401

    room_data = None

    if user.room:
        room_data = {
            "id": user.room.id,
            "hostel_block": user.room.hostel_block,
            "room_number": user.room.room_number
        }

    return jsonify({
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "room_id": user.room_id,
            "room": room_data
        }
    }), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({
        "message": "Logout successful"
    }), 200
