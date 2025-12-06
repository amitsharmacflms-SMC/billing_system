from flask import Blueprint, request, jsonify
from core.database import db
from models.suppliers import Supplier

supplier_bp = Blueprint("suppliers", __name__, url_prefix="/suppliers")

# ---------------------------------------------------
# GET ALL SUPPLIERS
# ---------------------------------------------------
@supplier_bp.route("/", methods=["GET"])
def get_all_suppliers():
    suppliers = Supplier.query.all()
    data = []
    for s in suppliers:
        data.append({
            "id": s.id,
            "unique_key": getattr(s, "unique_key", None),
            "name": s.name,
            "address": s.address,
            "city": getattr(s, "city", None),
            "state": getattr(s, "state", None),
            "pincode": getattr(s, "pincode", None),
            "gstin": getattr(s, "gstin", None),
            "contact_person": getattr(s, "contact_person", None),
            "phone": getattr(s, "phone", None),
            "email": getattr(s, "email", None)
        })
    return jsonify(data)


# ---------------------------------------------------
# GET SINGLE SUPPLIER
# ---------------------------------------------------
@supplier_bp.route("/<int:supplier_id>", methods=["GET"])
def get_supplier(supplier_id):
    s = Supplier.query.get(supplier_id)
    if not s:
        return jsonify({"error": "Supplier not found"}), 404

    return jsonify({
        "id": s.id,
        "unique_key": getattr(s, "unique_key", None),
        "name": s.name,
        "address": s.address,
        "city": getattr(s, "city", None),
        "state": getattr(s, "state", None),
        "pincode": getattr(s, "pincode", None),
        "gstin": getattr(s, "gstin", None),
        "contact_person": getattr(s, "contact_person", None),
        "phone": getattr(s, "phone", None),
        "email": getattr(s, "email", None)
    })


# ---------------------------------------------------
# ADD SUPPLIER
# ---------------------------------------------------
@supplier_bp.route("/add", methods=["POST"])
def add_supplier():
    data = request.get_json() or {}

    # minimal required fields
    if not data.get("name"):
        return jsonify({"error": "Supplier name is required"}), 400

    new_supplier = Supplier(
        unique_key=data.get("unique_key"),
        name=data.get("name"),
        address=data.get("address"),
        city=data.get("city"),
        state=data.get("state"),
        pincode=data.get("pincode"),
        gstin=data.get("gstin"),
        contact_person=data.get("contact_person"),
        phone=data.get("phone"),
        email=data.get("email"),
    )

    try:
        db.session.add(new_supplier)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Supplier added", "id": new_supplier.id})


# ---------------------------------------------------
# UPDATE SUPPLIER
# ---------------------------------------------------
@supplier_bp.route("/update/<int:supplier_id>", methods=["PUT"])
def update_supplier(supplier_id):
    s = Supplier.query.get(supplier_id)
    if not s:
        return jsonify({"error": "Supplier not found"}), 404

    data = request.get_json() or {}

    s.unique_key = data.get("unique_key", s.unique_key)
    s.name = data.get("name", s.name)
    s.address = data.get("address", s.address)
    s.city = data.get("city", s.city)
    s.state = data.get("state", s.state)
    s.pincode = data.get("pincode", s.pincode)
    s.gstin = data.get("gstin", s.gstin)
    s.contact_person = data.get("contact_person", s.contact_person)
    s.phone = data.get("phone", s.phone)
    s.email = data.get("email", s.email)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Supplier updated"})


# ---------------------------------------------------
# DELETE SUPPLIER
# ---------------------------------------------------
@supplier_bp.route("/delete/<int:supplier_id>", methods=["DELETE"])
def delete_supplier(supplier_id):
    s = Supplier.query.get(supplier_id)
    if not s:
        return jsonify({"error": "Supplier not found"}), 404

    try:
        db.session.delete(s)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Supplier deleted"})
