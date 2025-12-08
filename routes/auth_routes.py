from flask import Blueprint, request, jsonify
from core.database import db
from models.users import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta

# ----------------------------------------------------------
# DEFINE BLUEPRINT (The missing part that caused the crash)
# ----------------------------------------------------------
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ----------------------------------------------------------
# LOGIN ROUTE
# ----------------------------------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"error": "Invalid Email or Password"}, 401

    if not check_password_hash(user.password, password):
        return {"error": "Invalid Email or Password"}, 401

    from flask_jwt_extended import create_access_token

    # CONTENT FOR TOKEN (required by frontend)
    payload = {
        "role": user.role,
        "state": user.state,
        "supplier_id": user.supplier_id
    }

    token = create_access_token(identity=user.id, additional_claims=payload)

    # 🚨 MUST MATCH login.js EXACTLY
    return {
        "access_token": token,
        "role": user.role,
        "state": user.state,
        "supplier_id": user.supplier_id
    }, 200


# ----------------------------------------------------------
# RETURN LOGGED-IN USER DETAILS
# ----------------------------------------------------------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    uid = get_jwt_identity()
    user = User.query.get(uid)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "state": user.state,
        "supplier_id": user.supplier_id
    }), 200
