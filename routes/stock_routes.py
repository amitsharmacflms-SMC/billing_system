from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from datetime import datetime

from core.database import db
from models.stock import StockEntry
from models.products import Product

stock_bp = Blueprint("stock", __name__, url_prefix="/stock")


# -------------------------------------------------
# ALL PRODUCTS (Received Stock Page)
# -------------------------------------------------
@stock_bp.route("/all-products", methods=["GET"])
@jwt_required()
def all_products():
    products = Product.query.order_by(Product.name).all()
    return jsonify([
        {"id": p.id, "name": p.name}
        for p in products
    ])


# -------------------------------------------------
# BULK ADD STOCK
# -------------------------------------------------
@stock_bp.route("/bulk-add", methods=["POST"])
@jwt_required()
def bulk_add_stock():
    data = request.get_json()

    bill_no = data.get("bill_no")
    bill_date = data.get("bill_date")
    received_date = data.get("received_date")
    entries = data.get("entries", [])

    if not bill_no or not bill_date or not received_date:
        return {"error": "Bill number and date required"}, 400

    bill_date = datetime.strptime(bill_date, "%Y-%m-%d").date()
    received_date = datetime.strptime(received_date, "%Y-%m-%d").date()

    count = 0

    for row in entries:
        qty = float(row.get("qty", 0))
        if qty <= 0:
            continue

        db.session.add(
            StockEntry(
                product_id=int(row["product_id"]),
                bill_no=bill_no,
                bill_date=bill_date,
                received_date=received_date,
                received_cs=qty
            )
        )
        count += 1

    db.session.commit()
    return {"message": f"{count} items saved"}, 200
