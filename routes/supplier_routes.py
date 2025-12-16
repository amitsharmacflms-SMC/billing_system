from flask import Blueprint, request, jsonify
from core.database import db
from models.suppliers import Supplier

supplier_bp = Blueprint("suppliers", __name__, url_prefix="/suppliers")

# ---------------------------------------------------
# GET ALL SUPPLIERS
# ---------------------------------------------------
@supplier_bp.route("/", methods=["GET"])
def get_all_suppliers():
    suppliers = Supplier.query.order_by(Supplier.name).all()
    return jsonify([
        {
            "id": s.id,
            "unique_key": s.unique_key,
            "name": s.name,
            "contact_person": s.contact_person,
            "address": s.address,
            "city": s.city,
            "state": s.state,
            "state_code": s.state_code,
            "pincode": s.pincode,
            "gstin": s.gstin,
            "phone": s.phone,
            "email": s.email
        } for s in suppliers
    ])


# ---------------------------------------------------
# ADD SUPPLIER
# ---------------------------------------------------
@supplier_bp.route("/add", methods=["POST"])
def add_supplier():
    data = request.get_json() or {}

    if not data.get("name"):
        return {"error": "Supplier name required"}, 400

    s = Supplier(
        unique_key=data.get("unique_key"),
        name=data["name"],
        contact_person=data.get("contact_person"),
        address=data.get("address"),
        city=data.get("city"),
        state=data.get("state"),
        state_code=data.get("state_code"),
        pincode=data.get("pincode"),
        gstin=data.get("gstin"),
        phone=data.get("phone"),
        email=data.get("email")
    )

    db.session.add(s)
    db.session.commit()
    return {"message": "Supplier added", "id": s.id}


# ---------------------------------------------------
# UPDATE SUPPLIER
# ---------------------------------------------------
@supplier_bp.route("/update/<int:supplier_id>", methods=["PUT"])
def update_supplier(supplier_id):
    s = Supplier.query.get_or_404(supplier_id)
    data = request.get_json() or {}

    s.unique_key = data.get("unique_key", s.unique_key)
    s.name = data.get("name", s.name)
    s.contact_person = data.get("contact_person", s.contact_person)
    s.address = data.get("address", s.address)
    s.city = data.get("city", s.city)
    s.state = data.get("state", s.state)
    s.state_code = data.get("state_code", s.state_code)
    s.pincode = data.get("pincode", s.pincode)
    s.gstin = data.get("gstin", s.gstin)
    s.phone = data.get("phone", s.phone)
    s.email = data.get("email", s.email)

    db.session.commit()
    return {"message": "Supplier updated"}


# ---------------------------------------------------
# DELETE SUPPLIER
# ---------------------------------------------------
@supplier_bp.route("/delete/<int:supplier_id>", methods=["DELETE"])
def delete_supplier(supplier_id):
    s = Supplier.query.get_or_404(supplier_id)
    db.session.delete(s)
    db.session.commit()
    return {"message": "Supplier deleted"}
