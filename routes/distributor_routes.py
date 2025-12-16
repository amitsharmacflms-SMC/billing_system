from flask import Blueprint, jsonify, request
from core.database import db
from models.distributors import Distributor
from models.invoices import Invoice   # adjust if invoice model name differs

distributor_bp = Blueprint("distributors", __name__, url_prefix="/distributors")

# ---------------------------------------------------
# GET ALL DISTRIBUTORS
# ---------------------------------------------------
@distributor_bp.route("/", methods=["GET"])
def list_distributors():
    items = Distributor.query.order_by(Distributor.name).all()
    return jsonify([{
        "id": d.id,
        "unique_key": d.unique_key,
        "name": d.name,
        "contact_person": d.contact_person,
        "address": d.address,
        "city": d.city,
        "state": d.state,
        "pincode": d.pincode,
        "gstin": d.gstin,
        "phone": d.phone,
        "email": d.email,
        "supplier_id": d.supplier_id
    } for d in items])


# ---------------------------------------------------
# ADD DISTRIBUTOR
# ---------------------------------------------------
@distributor_bp.route("/add", methods=["POST"])
def add_distributor():
    data = request.get_json() or {}

    if not data.get("name"):
        return {"error": "Distributor name required"}, 400

    d = Distributor(
        unique_key=data.get("unique_key"),
        name=data["name"],
        contact_person=data.get("contact_person"),
        address=data.get("address"),
        city=data.get("city"),
        state=data.get("state"),
        pincode=data.get("pincode"),
        gstin=data.get("gstin"),
        phone=data.get("phone"),
        email=data.get("email"),
        supplier_id=data.get("supplier_id")
    )

    db.session.add(d)
    db.session.commit()
    return {"message": "Distributor added", "id": d.id}


# ---------------------------------------------------
# UPDATE DISTRIBUTOR
# ---------------------------------------------------
@distributor_bp.route("/update/<int:dist_id>", methods=["PUT"])
def update_distributor(dist_id):
    d = Distributor.query.get_or_404(dist_id)
    data = request.get_json() or {}

    d.unique_key = data.get("unique_key", d.unique_key)
    d.name = data.get("name", d.name)
    d.contact_person = data.get("contact_person", d.contact_person)
    d.address = data.get("address", d.address)
    d.city = data.get("city", d.city)
    d.state = data.get("state", d.state)
    d.pincode = data.get("pincode", d.pincode)
    d.gstin = data.get("gstin", d.gstin)
    d.phone = data.get("phone", d.phone)
    d.email = data.get("email", d.email)
    d.supplier_id = data.get("supplier_id", d.supplier_id)

    db.session.commit()
    return {"message": "Distributor updated"}


# ---------------------------------------------------
# DELETE DISTRIBUTOR (BLOCK IF USED IN INVOICES)
# ---------------------------------------------------
@distributor_bp.route("/delete/<int:dist_id>", methods=["DELETE"])
def delete_distributor(dist_id):
    d = Distributor.query.get_or_404(dist_id)

    used = db.session.query(Invoice.id)\
        .filter(Invoice.distributor_id == dist_id)\
        .first()

    if used:
        return {
            "error": "Distributor is used in invoices and cannot be deleted"
        }, 400

    db.session.delete(d)
    db.session.commit()
    return {"message": "Distributor deleted"}
