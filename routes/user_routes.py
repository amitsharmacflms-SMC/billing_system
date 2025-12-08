from flask import Blueprint, request, jsonify
from core.database import db
from models.users import User
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt

user_bp = Blueprint("users", __name__, url_prefix="/users")

def _is_admin():
    claims = get_jwt()
    return claims.get("role") == "admin"

@user_bp.route("/", methods=["GET"])
@jwt_required()
def list_users():
    if not _is_admin():
        return jsonify({"error":"admin only"}), 403
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([{
        "id": u.id, "name": u.name, "email": u.email,
        "role": u.role, "state": u.state, "supplier_id": u.supplier_id,
        "active": u.active
    } for u in users])


@user_bp.route("/add", methods=["POST"])
@jwt_required()
def add_user():
    if not _is_admin(): return jsonify({"error":"admin only"}), 403
    data = request.get_json()
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error":"Email exists"}), 400
    hashed = generate_password_hash(data["password"])
    u = User(name=data["name"], email=data["email"], password=hashed,
             role=data.get("role","user"), state=data.get("state"), supplier_id=data.get("supplier_id"))
    db.session.add(u); db.session.commit()
    return jsonify({"message":"User added","id":u.id}), 201


@user_bp.route("/update/<int:uid>", methods=["PUT"])
@jwt_required()
def update_user(uid):
    if not _is_admin(): return jsonify({"error":"admin only"}), 403
    u = User.query.get(uid)
    if not u: return jsonify({"error":"not found"}), 404
    data = request.get_json()
    u.name = data["name"]; u.email = data["email"]
    u.role = data.get("role", u.role)
    u.state = data.get("state", u.state)
    u.supplier_id = data.get("supplier_id", u.supplier_id)
    u.active = data.get("active", u.active)
    db.session.commit()
    return jsonify({"message":"updated"}), 200


@user_bp.route("/reset-password/<int:uid>", methods=["PUT"])
@jwt_required()
def reset_password(uid):
    if not _is_admin(): return jsonify({"error":"admin only"}), 403
    data = request.get_json()
    u = User.query.get(uid)
    if not u: return jsonify({"error":"not found"}), 404
    u.password = generate_password_hash(data["password"])
    db.session.commit()
    return jsonify({"message":"password updated"})


@user_bp.route("/delete/<int:uid>", methods=["DELETE"])
@jwt_required()
def delete_user(uid):
    if not _is_admin(): return jsonify({"error":"admin only"}), 403
    u = User.query.get(uid)
    if not u: return jsonify({"error":"not found"}), 404
    db.session.delete(u); db.session.commit()
    return jsonify({"message":"deleted"})


# -----------------------------------------------------------
# TEMPORARY ROUTE: CREATE FIRST ADMIN USER
# REMOVE AFTER FIRST USE
# -----------------------------------------------------------
@user_bp.route("/create-initial-admin", methods=["POST"])
def create_initial_admin():
    from werkzeug.security import generate_password_hash
    data = request.get_json()

    existing_admin = User.query.filter_by(role="admin").first()
    if existing_admin:
        return {"error": "Admin already exists"}, 400

    hashed = generate_password_hash(data["password"])

    new_admin = User(
        name=data["AMIT SHARMA"],
        email=data["amit@gmail.com"],
        password=password@1,
        role="admin",
        state=data.get("state", "Uttar Pradesh"),
        active=True
    )
    db.session.add(new_admin)
    db.session.commit()

    return {"message": "Initial admin created"}, 201



