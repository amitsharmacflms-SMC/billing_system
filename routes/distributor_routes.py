from flask import Blueprint, request, jsonify
from core.database import db
from models.distributors import Distributor
from models.invoices import Invoice   # ensure this exists
import re

distributor_bp = Blueprint("distributors", __name__, url_prefix="/distributors")

GSTIN_REGEX = re.compile(
    r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$"
)

# ---------------------------------------------------
# LIST ALL
# ---------------------------------------------------
@distributor_bp.route("/", methods=["GET"])
def list_distributors():
    items = Distributor.query.order_by(Distributor.name).all()
    return jsonify([{
        "id": d.id,
        "unique_key": d.unique_key,
        "name": d.name,
        "city": d.city,
        "state": d.state,
        "gstin": d.gstin
    } for d in items])


# ---------------------------------------------------
# GET SINGLE (FIXES 404 + JSON ERROR)
# ---------------------------------------------------
@distributor_bp.route("/<int:dist_id>", methods=["GET"])
def get_distributor(dist_id):
    d = Distributor.query.get(dist_id)
    if not d:
        return {"error": "Distributor not found"}, 404

    return {
        "id": d.id,
        "unique_key": d.unique_key,
        "name": d.name,
        "contact_person": d.contact_person,
        "phone": d.phone,
        "email": d.email,
        "address": d.address,
        "city": d.city,
        "state": d.state,
        "pincode": d.pincode,
        "gstin": d.gstin,
        "supplier_id": d.supplier_id
    }


# ---------------------------------------------------
# ADD
# ---------------------------------------------------
@distributor_bp.route("/add", methods=["POST"])
def add_distributor():
    data = request.get_json() or {}

    if not data.get("unique_key") or not data.get("name") or not data.get("gstin"):
        return {"error": "Distributor Code, Name and GSTIN are required"}, 400

    gstin = data["gstin"].upper()
    if not GSTIN_REGEX.match(gstin):
        return {"error": "Invalid GSTIN format"}, 400

    if Distributor.query.filter_by(unique_key=data["unique_key"]).first():
        return {"error": "Distributor Code already exists"}, 400

    if Distributor.query.filter_by(gstin=gstin).first():
        return {"error": "GSTIN already exists"}, 400

    d = Distributor(
        unique_key=data["unique_key"],
        name=data["name"],
        contact_person=data.get("contact_person"),
        phone=data.get("phone"),
        email=data.get("email"),
        address=data.get("address"),
        city=data.get("city"),
        state=data.get("state"),
        pincode=data.get("pincode"),
        gstin=gstin,
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

    if "unique_key" in data and data["unique_key"] != d.unique_key:
        if Distributor.query.filter(
            Distributor.unique_key == data["unique_key"],
            Distributor.id != dist_id
        ).first():
            return {"error": "Distributor Code already exists"}, 400
        d.unique_key = data["unique_key"]

    if "gstin" in data:
        gstin = data["gstin"].upper()
        if not GSTIN_REGEX.match(gstin):
            return {"error": "Invalid GSTIN format"}, 400
        if Distributor.query.filter(
            Distributor.gstin == gstin,
            Distributor.id != dist_id
        ).first():
            return {"error": "GSTIN already exists"}, 400
        d.gstin = gstin

    d.name = data.get("name", d.name)
    d.contact_person = data.get("contact_person", d.contact_person)
    d.phone = data.get("phone", d.phone)
    d.email = data.get("email", d.email)
    d.address = data.get("address", d.address)
    d.city = data.get("city", d.city)
    d.state = data.get("state", d.state)
    d.pincode = data.get("pincode", d.pincode)
    d.supplier_id = data.get("supplier_id", d.supplier_id)

    db.session.commit()
    return {"message": "Distributor updated successfully"}


# ---------------------------------------------------
# DELETE (BLOCK IF USED)
# ---------------------------------------------------
@distributor_bp.route("/delete/<int:dist_id>", methods=["DELETE"])
def delete_distributor(dist_id):
    used = db.session.query(Invoice.id)\
        .filter(Invoice.distributor_id == dist_id)\
        .first()

    if used:
        return {"error": "Distributor is used in invoices and cannot be deleted"}, 400

    d = Distributor.query.get_or_404(dist_id)
    db.session.delete(d)
    db.session.commit()
    return {"message": "Distributor deleted successfully"}
