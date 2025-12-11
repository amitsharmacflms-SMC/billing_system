from flask import Blueprint, request, jsonify
from core.database import db
from models.stock import StockEntry
from models.products import Product
from flask_jwt_extended import jwt_required
from datetime import datetime

stock_bp = Blueprint("stock", __name__, url_prefix="/stock")


# GET PRODUCT LIST
@stock_bp.route("/all-products", methods=["GET"])
@jwt_required()
def all_products():
    from models.products import Product
    products = Product.query.order_by(Product.name.asc()).all()
    return jsonify([
        {"id": p.id, "name": p.name}
        for p in products
    ])


# ADD STOCK ENTRY
@stock_bp.route("/bulk-add", methods=["POST"])
@jwt_required()
def bulk_add_stock():
    data = request.get_json()
    
    bill_no = data.get("bill_no")
    bill_date = data.get("bill_date")
    entries = data.get("entries", [])

    if not bill_no or not bill_date:
        return jsonify({"error": "Bill number and date required"}), 400

    try:
        bill_date_parsed = datetime.strptime(bill_date, "%Y-%m-%d")
        
        saved_count = 0

        for item in entries:
            qty = float(item.get("qty", 0))
            if qty <= 0:
                continue  # skip empty rows

            entry = StockEntry(
                product_id=item["product_id"],
                bill_no=bill_no,
                bill_date=bill_date_parsed,
                received_cs=qty,
                remarks=""
            )
            db.session.add(entry)
            saved_count += 1

        db.session.commit()
        return jsonify({"message": f"{saved_count} items saved"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
