from flask import Blueprint, jsonify, session, request

from backend.app import db
from backend.models.user import User


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
