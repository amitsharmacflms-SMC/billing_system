from flask import Blueprint, request, jsonify
from core.database import db
from models.distributors import Distributor
from models.invoices import Invoice   # <-- correct import

distributor_bp = Blueprint("distributors", __name__, url_prefix="/distributors")

# --------------------------------------------------
# GET ALL DISTRIBUTORS
# --------------------------------------------------
@distributor_bp.route("/", methods=["GET"])
def get_all_distributors():
    distributors = Distributor.query.all()
    data = []

    for d in distributors:
        data.append({
            "id": d.id,
            "name": d.name,
            "gstin": d.gstin,
            "address": d.address,
            "state": d.state,
            "state_code": d.state_code,
            "contact": d.contact
        })

    return jsonify(data)


# --------------------------------------------------
# ADD NEW DISTRIBUTOR
# --------------------------------------------------
@distributor_bp.route("/add", methods=["POST"])
def add_distributor():
    try:
        data = request.get_json()

        name = data.get("name")
        gstin = data.get("gstin")
        address = data.get("address")
        state = data.get("state")
        state_code = data.get("state_code")
        contact = data.get("contact")

        if not name:
            return jsonify({"error": "Distributor name is required"}), 400

        new_distributor = Distributor(
            name=name,
            gstin=gstin,
            address=address,
            state=state,
            state_code=state_code,
            contact=contact
        )

        db.session.add(new_distributor)
        db.session.commit()

        return jsonify({"message": "Distributor added", "id": new_distributor.id})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------
# GET SINGLE DISTRIBUTOR
# --------------------------------------------------
@distributor_bp.route("/<int:dist_id>", methods=["GET"])
def get_distributor(dist_id):
    distributor = Distributor.query.get(dist_id)
    if not distributor:
        return jsonify({"error": "Distributor not found"}), 404

    return jsonify({
        "id": distributor.id,
        "name": distributor.name,
        "gstin": distributor.gstin,
        "address": distributor.address,
        "state": distributor.state,
        "state_code": distributor.state_code,
        "contact": distributor.contact
    })


# --------------------------------------------------
# UPDATE DISTRIBUTOR
# --------------------------------------------------
@distributor_bp.route("/update/<int:dist_id>", methods=["PUT"])
def update_distributor(dist_id):
    try:
        distributor = Distributor.query.get(dist_id)
        if not distributor:
            return jsonify({"error": "Distributor not found"}), 404

        data = request.get_json()

        distributor.name = data.get("name", distributor.name)
        distributor.gstin = data.get("gstin", distributor.gstin)
        distributor.address = data.get("address", distributor.address)
        distributor.state = data.get("state", distributor.state)
        distributor.state_code = data.get("state_code", distributor.state_code)
        distributor.contact = data.get("contact", distributor.contact)

        db.session.commit()

        return jsonify({"message": "Distributor updated"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------
# DELETE DISTRIBUTOR
# --------------------------------------------------
@distributor_bp.route("/delete/<int:dist_id>", methods=["DELETE"])
def delete_distributor(dist_id):
    try:
        distributor = Distributor.query.get(dist_id)
        if not distributor:
            return jsonify({"error": "Distributor not found"}), 404

        db.session.delete(distributor)
        db.session.commit()

        return jsonify({"message": "Distributor deleted"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------
# SEARCH DISTRIBUTORS
# --------------------------------------------------
@distributor_bp.route("/search", methods=["GET"])
def search_distributors():
    query = request.args.get("q", "")

    results = Distributor.query.filter(
        Distributor.name.ilike(f"%{query}%")
    ).all()

    data = []
    for d in results:
        data.append({
            "id": d.id,
            "name": d.name,
            "gstin": d.gstin,
            "state": d.state,
            "contact": d.contact
        })

    return jsonify(data)


# --------------------------------------------------
# GET DISTRIBUTOR WITH INVOICES
# --------------------------------------------------
@distributor_bp.route("/<int:dist_id>/invoices", methods=["GET"])
def get_distributor_invoices(dist_id):
    distributor = Distributor.query.get(dist_id)
    if not distributor:
        return jsonify({"error": "Distributor not found"}), 404

    invoices = Invoice.query.filter_by(distributor_id=dist_id).all()

    invoice_list = []
    for inv in invoices:
        invoice_list.append({
            "id": inv.id,
            "invoice_number": inv.invoice_number,   # <-- fixed
            "date": str(inv.date),                  # <-- fixed
            "grand_total": inv.grand_total          # <-- fixed
        })

    return jsonify({
        "distributor": distributor.name,
        "invoices": invoice_list
    })
