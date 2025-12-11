from flask import Blueprint, request, jsonify
from core.database import db
from models.stock import StockEntry
from models.products import Product
from flask_jwt_extended import jwt_required
from datetime import datetime

stock_bp = Blueprint("stock", __name__, url_prefix="/stock")


# GET PRODUCT LIST
@stock_bp.route("/products", methods=["GET"])
@jwt_required()
def get_products():
    products = Product.query.order_by(Product.name.asc()).all()
    return jsonify([{"id": p.id, "name": p.name} for p in products])


# ADD STOCK ENTRY
@stock_bp.route("/add", methods=["POST"])
@jwt_required()
def add_stock():
    data = request.get_json()

    try:
        entry = StockEntry(
            product_id=data["product_id"],
            bill_no=data["bill_no"],
            bill_date=datetime.strptime(data["bill_date"], "%Y-%m-%d"),
            received_cs=float(data["received_cs"]),
            remarks=data.get("remarks", "")
        )

        db.session.add(entry)
        db.session.commit()

        return jsonify({"message": "Stock added successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
