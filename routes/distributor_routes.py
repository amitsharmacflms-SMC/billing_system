from flask import Blueprint, jsonify, request
from core.database import db
from models.distributors import Distributor

distributor_bp = Blueprint("distributors", __name__, url_prefix="/distributors")

@distributor_bp.route("/", methods=["GET"])
def list_distributors():
    items = Distributor.query.order_by(Distributor.name).all()
    return jsonify([{
        "id": d.id, "name": d.name, "city": d.city, "state": d.state,
        "gstin": d.gstin, "supplier_id": d.supplier_id
    } for d in items])

@distributor_bp.route("/by-supplier/<int:supplier_id>", methods=["GET"])
def distributors_by_supplier(supplier_id):
    items = Distributor.query.filter_by(supplier_id=supplier_id).order_by(Distributor.name).all()
    return jsonify([{
        "id": d.id, "name": d.name, "city": d.city, "state": d.state, "gstin": d.gstin
    } for d in items])

# keep your existing add/update/delete endpoints as is but ensure they set supplier_id if provided

# ---------------------------------------------------
# GET SINGLE DISTRIBUTOR
# ---------------------------------------------------
@distributor_bp.route("/<int:dist_id>", methods=["GET"])
def get_distributor(dist_id):
    d = Distributor.query.get(dist_id)
    if not d:
        return jsonify({"error": "Distributor not found"}), 404

    return jsonify({
        "id": d.id,
        "unique_key": d.unique_key,
        "name": d.name,
        "address": d.address,
        "city": d.city,
        "state": d.state,
        "pincode": d.pincode,
        "gstin": d.gstin,
        "contact_person": d.contact_person,
        "phone": d.phone,
        "email": d.email
    })

# ---------------------------------------------------
# ADD DISTRIBUTOR
# ---------------------------------------------------
@distributor_bp.route("/add", methods=["POST"])
def add_distributor():
    data = request.get_json()

    required = ["name", "city", "state", "pincode"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    new_dist = Distributor(
        unique_key=data.get("unique_key"),
        name=data["name"],
        address=data.get("address"),
        city=data["city"],
        state=data["state"],
        pincode=data["pincode"],
        gstin=data.get("gstin"),
        contact_person=data.get("contact_person"),
        phone=data.get("phone"),
        email=data.get("email"),
    )

    db.session.add(new_dist)
    db.session.commit()

    return jsonify({"message": "Distributor added", "id": new_dist.id})

# ---------------------------------------------------
# UPDATE DISTRIBUTOR
# ---------------------------------------------------
@distributor_bp.route("/update/<int:dist_id>", methods=["PUT"])
def update_distributor(dist_id):
    d = Distributor.query.get(dist_id)
    if not d:
        return jsonify({"error": "Distributor not found"}), 404

    data = request.get_json()

    d.unique_key = data.get("unique_key", d.unique_key)
    d.name = data.get("name", d.name)
    d.address = data.get("address", d.address)
    d.city = data.get("city", d.city)
    d.state = data.get("state", d.state)
    d.pincode = data.get("pincode", d.pincode)
    d.gstin = data.get("gstin", d.gstin)
    d.contact_person = data.get("contact_person", d.contact_person)
    d.phone = data.get("phone", d.phone)
    d.email = data.get("email", d.email)

    db.session.commit()

    return jsonify({"message": "Distributor updated"})

# ---------------------------------------------------
# DELETE DISTRIBUTOR
# ---------------------------------------------------
@distributor_bp.route("/delete/<int:dist_id>", methods=["DELETE"])
def delete_distributor(dist_id):
    d = Distributor.query.get(dist_id)
    if not d:
        return jsonify({"error": "Distributor not found"}), 404

    db.session.delete(d)
    db.session.commit()

    return jsonify({"message": "Distributor deleted"})
