from flask import Blueprint, jsonify, request
from core.database import db
from models.distributors import Distributor
from models.invoices import Invoice   # adjust if your model name differs
import re

distributor_bp = Blueprint("distributors", __name__, url_prefix="/distributors")

GSTIN_REGEX = re.compile(
    r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$"
)

# ---------------------------------------------------
# LIST
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
# ADD
# ---------------------------------------------------
@distributor_bp.route("/add", methods=["POST"])
def add_distributor():
    data = request.get_json() or {}

    if not data.get("unique_key"):
        return {"error": "Distributor Code is required"}, 400

    if not data.get("gstin"):
        return {"error": "GSTIN is required"}, 400

    gstin = data["gstin"].upper()
    if not GSTIN_REGEX.match(gstin):
        return {"error": "Invalid GSTIN format"}, 400

    if Distributor.query.filter_by(unique_key=data["unique_key"]).first():
        return {"error": "Distributor Code already exists"}, 400

    if Distributor.query.filter_by(gstin=gstin).first():
        return {"error": "GSTIN already exists"}, 400

    d = Distributor(
        unique_key=data["unique_key"],
        name=data.get("name"),
        contact_person=data.get("contact_person"),
        address=data.get("address"),
        city=data.get("city"),
        state=data.get("state"),
        pincode=data.get("pincode"),
        gstin=gstin,
        phone=data.get("phone"),
        email=data.get("email"),
        supplier_id=data.get("supplier_id")
    )

    db.session.add(d)
    db.session.commit()
    return {"message": "Distributor added successfully"}


# ---------------------------------------------------
# UPDATE
# ---------------------------------------------------
@distributor_bp.route("/update/<int:dist_id>", methods=["PUT"])
def update_distributor(dist_id):
    d = Distributor.query.get_or_404(dist_id)
    data = request.get_json() or {}

    if "unique_key" in data:
        exists = Distributor.query.filter(
            Distributor.unique_key == data["unique_key"],
            Distributor.id != dist_id
        ).first()
        if exists:
            return {"error": "Distributor Code already exists"}, 400
        d.unique_key = data["unique_key"]

    if "gstin" in data:
        gstin = data["gstin"].upper()
        if not GSTIN_REGEX.match(gstin):
            return {"error": "Invalid GSTIN format"}, 400
        exists = Distributor.query.filter(
            Distributor.gstin == gstin,
            Distributor.id != dist_id
        ).first()
        if exists:
            return {"error": "GSTIN already exists"}, 400
        d.gstin = gstin

    d.name = data.get("name", d.name)
    d.city = data.get("city", d.city)
    d.state = data.get("state", d.state)

    db.session.commit()
    return {"message": "Distributor updated successfully"}


# ---------------------------------------------------
# DELETE (BLOCK IF INVOICES EXIST)
# ---------------------------------------------------
@distributor_bp.route("/delete/<int:dist_id>", methods=["DELETE"])
def delete_distributor(dist_id):
    used = db.session.query(Invoice.id)\
        .filter(Invoice.distributor_id == dist_id)\
        .first()

    if used:
        return {
            "error": "Distributor is used in invoices and cannot be deleted"
        }, 400

    d = Distributor.query.get_or_404(dist_id)
    db.session.delete(d)
    db.session.commit()
    return {"message": "Distributor deleted successfully"}
