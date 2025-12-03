from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from models.users import User
from core.database import db
import jwt
import datetime
import os

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# -------------------------------
# Generate JWT Token
# -------------------------------
def generate_token(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }
    token = jwt.encode(payload, os.getenv("FLASK_SECRET_KEY"), algorithm="HS256")
    return token


# -------------------------------
# LOGIN
# -------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email & password required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        if not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid password"}), 401

        token = generate_token(user)

        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role
            }
        })

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500


# -------------------------------
# CHECK TOKEN (Authentication API)
# -------------------------------
@auth_bp.route("/verify", methods=["GET"])
def verify_token():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"}), 401

    try:
        decoded = jwt.decode(token, os.getenv("FLASK_SECRET_KEY"), algorithms=["HS256"])
        return jsonify({"valid": True, "user": decoded})

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401

    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
