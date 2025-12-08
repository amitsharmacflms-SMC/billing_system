from flask import Blueprint, request, jsonify
from core.database import db
from models.suppliers import Supplier
from models.distributors import Distributor
from flask_jwt_extended import jwt_required, get_jwt

map_bp = Blueprint("mapping", __name__, url_prefix="/mapping")

def _is_admin():
    claims = get_jwt()
    return claims.get("role") == "admin"

@map_bp.route("/assign", methods=["POST"])
@jwt_required()
def assign():
    if not _is_admin(): return jsonify({"error":"admin only"}), 403
    data = request.get_json()
    supplier_id = data.get("supplier_id")
    distributor_ids = data.get("distributor_ids", [])
    # simple approach: assign each distributor to supplier
    for did in distributor_ids:
        d = Distributor.query.get(did)
        if d:
            d.supplier_id = supplier_id
    db.session.commit()
    return jsonify({"message":"Assigned"}), 200

@map_bp.route("/by-supplier/<int:supplier_id>", methods=["GET"])
@jwt_required()
def get_by_supplier(supplier_id):
    ds = Distributor.query.filter_by(supplier_id=supplier_id).all()
    return jsonify([{"id":d.id, "name":d.name} for d in ds])
