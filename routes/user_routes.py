from flask import Blueprint, request, jsonify
from core.database import db
from models.users import User
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt

user_bp = Blueprint("users", __name__, url_prefix="/users")


# --------------------------
# CHECK ADMIN
# --------------------------
def _is_admin():
    claims = get_jwt()
    return claims.get("role") == "admin"


# --------------------------
# LIST USERS
# --------------------------
@user_bp.route("/", methods=["GET"])
@jwt_required()
def list_users():
    if not _is_admin():
        return {"error": "admin only"}, 403

    users = User.query.order_by(User.created_at.desc()).all()

    return [{
        "id": u.id,
        "full_name": u.full_name,
        "email": u.email,
        "role": u.role,
        "state": u.state,
        "supplier_id": u.supplier_id,
        "active": u.is_active,
        "created_at": u.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for u in users], 200


# --------------------------
# ADD USER
# --------------------------
@user_bp.route("/add", methods=["POST"])
@jwt_required()
def add_user():
    if not _is_admin():
        return {"error": "admin only"}, 403

    data = request.get_json()

    if User.query.filter_by(email=data["email"]).first():
        return {"error": "Email already exists"}, 400

    user = User(
        full_name=data.get("full_name"),
        email=data.get("email"),
        role=data.get("role", "user"),
        supplier_id=data.get("supplier_id"),
        state=data.get("state"),
        is_active=True
    )
    user.password_hash = generate_password_hash(data["password"])

    db.session.add(user)
    db.session.commit()

    return {"message": "User added", "id": user.id}, 201


# --------------------------
# UPDATE USER
# --------------------------
@user_bp.route("/update/<int:uid>", methods=["PUT"])
@jwt_required()
def update_user(uid):
    if not _is_admin():
        return {"error": "admin only"}, 403

    user = User.query.get(uid)
    if not user:
        return {"error": "User not found"}, 404

    data = request.get_json()

    user.full_name = data.get("full_name", user.full_name)
    user.email = data.get("email", user.email)
    user.role = data.get("role", user.role)
    user.state = data.get("state", user.state)
    user.supplier_id = data.get("supplier_id", user.supplier_id)
    user.is_active = data.get("active", user.is_active)

    db.session.commit()
    return {"message": "User updated"}, 200


# --------------------------
# RESET PASSWORD
# --------------------------
@user_bp.route("/reset-password/<int:uid>", methods=["PUT"])
@jwt_required()
def reset_password(uid):
    if not _is_admin():
        return {"error": "admin only"}, 403

    user = User.query.get(uid)
    if not user:
        return {"error": "User not found"}, 404

    data = request.get_json()

    user.password_hash = generate_password_hash(data["password"])
    db.session.commit()

    return {"message": "Password updated"}, 200


# --------------------------
# DELETE USER
# --------------------------
@user_bp.route("/delete/<int:uid>", methods=["DELETE"])
@jwt_required()
def delete_user(uid):
    if not _is_admin():
        return {"error": "admin only"}, 403

    user = User.query.get(uid)
    if not user:
        return {"error": "User not found"}, 404

    db.session.delete(user)
    db.session.commit()

    return {"message": "User deleted"}, 200


# -----------------------------------------------------------
# CREATE FIRST ADMIN USER (ONE-TIME USE)
# -----------------------------------------------------------
@user_bp.route("/create-initial-admin", methods=["POST"])
def create_initial_admin():
    # Prevent creating multiple super admins
    if User.query.filter_by(role="admin").first():
        return {"error": "Admin already exists"}, 400

    data = request.get_json()

    user = User(
        full_name=data["name"],
        email=data["email"],
        role="admin",
        is_active=True,
        state="UP",            # Default state
        supplier_id=None
    )
    user.password_hash = generate_password_hash(data["password"])

    db.session.add(user)
    db.session.commit()

    return {"message": "Admin created successfully"}, 201
