from flask import Blueprint, jsonify, session, request

from backend.app import db
from backend.models.user import User
from backend.models.complaint import Complaint


warden_bp = Blueprint(
    "warden",
    __name__,
    url_prefix="/api/warden"
)


@warden_bp.route("/complaints", methods=["GET"])
def get_complaints():
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

    # Only wardens can access this endpoint
    if user.role != "warden":
        return jsonify({
            "error": "Only wardens can view complaints"
        }), 403

    # Get all complaints
    complaints = Complaint.query.order_by(
        Complaint.created_at.desc()
    ).all()

    complaint_list = []

    for complaint in complaints:
        complaint_list.append({
            "complaint_id": complaint.complaint_id,
            "user_id": complaint.user_id,
            "room_id": complaint.room_id,
            "category": complaint.category,
            "title": complaint.title,
            "description": complaint.description,
            "priority": complaint.priority,
            "status": complaint.status,
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


@warden_bp.route(
    "/complaints/<string:complaint_id>",
    methods=["PATCH"]
)
def update_complaint_status(complaint_id):
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

    # Only wardens can update complaints
    if user.role != "warden":
        return jsonify({
            "error": "Only wardens can update complaints"
        }), 403

    # Find the complaint
    complaint = Complaint.query.filter_by(
        complaint_id=complaint_id
    ).first()

    # Complaint does not exist
    if not complaint:
        return jsonify({
            "error": "Complaint not found"
        }), 404

    # Get JSON request body
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    # Get the new status
    new_status = data.get("status")

    # Make sure status was provided
    if not new_status:
        return jsonify({
            "error": "Status is required"
        }), 400

    # Allowed complaint statuses
    allowed_statuses = [
        "Pending",
        "In Progress",
        "Resolved"
    ]

    # Validate status
    if new_status not in allowed_statuses:
        return jsonify({
            "error": "Invalid status",
            "allowed_statuses": allowed_statuses
        }), 400

    # Update the complaint status
    complaint.status = new_status

    # Update resolved_at when complaint is resolved
    if new_status == "Resolved":
        from datetime import datetime

        complaint.resolved_at = datetime.utcnow()

    else:
        complaint.resolved_at = None

    # Save changes
    db.session.commit()

    return jsonify({
        "message": "Complaint status updated successfully",
        "complaint": {
            "complaint_id": complaint.complaint_id,
            "status": complaint.status,
            "resolved_at": (
                complaint.resolved_at.isoformat()
                if complaint.resolved_at
                else None
            ),
            "updated_at": complaint.updated_at.isoformat()
        }
    }), 200
