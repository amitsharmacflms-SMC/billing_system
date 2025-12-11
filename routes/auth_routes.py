from flask import Blueprint, request, jsonify
from core.database import db
from models.users import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# -----------------------
# LOGIN
# -----------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "Email and password required"}, 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"error": "Invalid login"}, 401

    if not check_password_hash(user.password_hash, password):
        return {"error": "Invalid login"}, 401

    if not user.is_active:
        return {"error": "User disabled"}, 403

    # Create JWT with custom claims
    access_token = create_access_token(
    identity=str(user.id),
    additional_claims={
        "role": user.role,
        "supplier_id": user.supplier_id,
        "state": user.state
    }
)


    return {
        "message": "Login successful",
        "token": token,
        "role": user.role,
        "supplier_id": user.supplier_id,
        "state": user.state,
        "full_name": user.full_name
    }, 200


# -----------------------
# GET CURRENT USER INFO
# -----------------------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    claims = get_jwt()
    user_id = claims["sub"]

    user = User.query.get(user_id)

    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "supplier_id": user.supplier_id,
        "state": user.state,
        "active": user.is_active
    }, 200
