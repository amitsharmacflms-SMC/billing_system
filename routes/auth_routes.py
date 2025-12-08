from flask import Blueprint, request, jsonify
from core.database import db
from models.users import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

# ------------------------------
# AUTH BLUEPRINT
# ------------------------------
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ------------------------------
# LOGIN ROUTE
# ------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "Email and password required"}, 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"error": "Invalid email or password"}, 401

    if not check_password_hash(user.password, password):
        return {"error": "Invalid email or password"}, 401

    token = create_access_token(
        identity=user.id,
        additional_claims={
            "role": user.role,
            "state": user.state,
            "supplier_id": user.supplier_id
        },
        expires_delta=timedelta(days=1)
    )

    return {
        "access_token": token,
        "role": user.role,
        "state": user.state,
        "supplier_id": user.supplier_id
    }, 200


# ------------------------------
# GET LOGGED-IN USER DETAILS
# ------------------------------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    uid = get_jwt_identity()
    user = User.query.get(uid)

    if not user:
        return {"error": "User not found"}, 404

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "state": user.state,
        "supplier_id": user.supplier_id
    }, 200
