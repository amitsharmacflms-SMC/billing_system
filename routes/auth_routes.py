from flask import Blueprint, request, jsonify
from core.database import db
from models.users import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.active:
        return jsonify({"error": "Invalid credentials"}), 401

    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # create token with identity containing user id and role/state/supplier
    additional_claims = {
        "role": user.role,
        "state": user.state,
        "supplier_id": user.supplier_id
    }
    token = create_access_token(identity=user.id, additional_claims=additional_claims, expires_delta=timedelta(days=1))

    return jsonify({
        "access_token": token,
        "role": user.role,
        "state": user.state,
        "supplier_id": user.supplier_id
    }), 200


@auth_bp.route("/me", methods=["GET"])
def me():
    # optional: return user details from token (or query DB)
    from flask_jwt_extended import get_jwt_identity
    uid = get_jwt_identity()
    user = User.query.get(uid)
    if not user: return jsonify({}), 404
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "state": user.state,
        "supplier_id": user.supplier_id
    })
