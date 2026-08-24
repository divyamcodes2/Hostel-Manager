from flask import Blueprint, request, jsonify, session

from backend.app import db
from backend.models.user import User
from backend.models.complaint import Complaint


complaints_bp = Blueprint(
    "complaints",
    __name__,
    url_prefix="/api/complaints"
)


@complaints_bp.route("", methods=["POST"])
def create_complaint():
    # Get the ID of the currently logged-in user
    user_id = session.get("user_id")

    # User is not logged in
    if not user_id:
        return jsonify({
            "error": "Not authenticated"
        }), 401

    # Find the logged-in user in the database
    user = User.query.get(user_id)

    # User doesn't exist or account is inactive
    if not user or not user.active:
        session.clear()

        return jsonify({
            "error": "Not authenticated"
        }), 401

    # Only students can create complaints
    if user.role != "student":
        return jsonify({
            "error": "Only students can create complaints"
        }), 403

    # Student must have a room
    if not user.room_id:
        return jsonify({
            "error": "Student is not assigned to a room"
        }), 400

    # Get JSON body from the request
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    # Get complaint fields from the request
    category = data.get("category")
    title = data.get("title")
    description = data.get("description")

    # Validate required fields
    if not category or not title or not description:
        return jsonify({
            "error": "Category, title and description are required"
        }), 400

    # Create the complaint
    complaint = Complaint(
        user_id=user.id,
        room_id=user.room_id,
        category=category,
        title=title,
        description=description
    )

    # Add complaint to the database
    db.session.add(complaint)

    # Save the complaint
    db.session.commit()

    return jsonify({
        "message": "Complaint created successfully",
        "complaint": {
            "complaint_id": complaint.complaint_id,
            "category": complaint.category,
            "title": complaint.title,
            "description": complaint.description,
            "priority": complaint.priority,
            "status": complaint.status,
            "user_id": complaint.user_id,
            "room_id": complaint.room_id,
            "created_at": complaint.created_at.isoformat()
        }
    }), 201


@complaints_bp.route("", methods=["GET"])
def get_my_complaints():
    # Get the ID of the currently logged-in user
    user_id = session.get("user_id")

    # User is not logged in
    if not user_id:
        return jsonify({
            "error": "Not authenticated"
        }), 401

    # Find the logged-in user
    user = User.query.get(user_id)

    # User doesn't exist or account is inactive
    if not user or not user.active:
        session.clear()

        return jsonify({
            "error": "Not authenticated"
        }), 401

    # Only students can use this endpoint
    if user.role != "student":
        return jsonify({
            "error": "Only students can view their complaints"
        }), 403

    # Get only complaints belonging to this user
    complaints = Complaint.query.filter_by(
        user_id=user.id
    ).order_by(
        Complaint.created_at.desc()
    ).all()

    complaint_list = []

    for complaint in complaints:
        complaint_list.append({
            "complaint_id": complaint.complaint_id,
            "category": complaint.category,
            "title": complaint.title,
            "description": complaint.description,
            "priority": complaint.priority,
            "status": complaint.status,
            "room_id": complaint.room_id,
            "created_at": complaint.created_at.isoformat(),
            "updated_at": complaint.updated_at.isoformat(),
            "resolved_at": (
                complaint.resolved_at.isoformat()
                if complaint.resolved_at
                else None
            )
        })

    return jsonify({
        "complaints": complaint_list
    }), 200
