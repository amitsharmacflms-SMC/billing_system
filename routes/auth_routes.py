from flask import Blueprint, request, jsonify
from models.users import User
from core.database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return jsonify({"msg": "Bad credentials"}), 401

    access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=8))
    return jsonify({"access_token": access_token})

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    uid = get_jwt_identity()
    user = User.query.get(uid)
    return jsonify({"id": user.id, "email": user.email, "name": user.full_name, "role": user.role})
