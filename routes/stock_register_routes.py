from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from core.database import db
from models.stock import StockEntry
from models.invoice_items import InvoiceItem
from datetime import date

stock_register_bp = Blueprint("stock_register", __name__, url_prefix="/stock-register")


@stock_register_bp.route("/monthly", methods=["GET"])
@jwt_required()
def monthly_stock_register():
    product_id = request.args.get("product_id")
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))

    if not product_id:
        return {"error": "product_id required"}, 400

    month_start = date(year, month, 1)

    # -------------------------
    # OPENING STOCK
    # -------------------------
    opening_received = db.session.query(
        db.func.coalesce(db.func.sum(StockEntry.received_cs), 0)
    ).filter(
        StockEntry.product_id == product_id,
        StockEntry.received_date < month_start
    ).scalar()

    opening_sold = db.session.query(
        db.func.coalesce(db.func.sum(InvoiceItem.cs), 0)
    ).filter(
        InvoiceItem.product_id == product_id,
        InvoiceItem.created_at < month_start
    ).scalar()

    opening_qty = float(opening_received) - float(opening_sold)

    # -------------------------
    # RECEIVED IN MONTH
    # -------------------------
    received_qty = db.session.query(
        db.func.coalesce(db.func.sum(StockEntry.received_cs), 0)
    ).filter(
        StockEntry.product_id == product_id,
        db.extract("year", StockEntry.received_date) == year,
        db.extract("month", StockEntry.received_date) == month
    ).scalar()

    # -------------------------
    # SOLD IN MONTH
    # -------------------------
    sold_qty = db.session.query(
        db.func.coalesce(db.func.sum(InvoiceItem.cs), 0)
    ).filter(
        InvoiceItem.product_id == product_id,
        db.extract("year", InvoiceItem.created_at) == year,
        db.extract("month", InvoiceItem.created_at) == month
    ).scalar()

    balance_qty = opening_qty + float(received_qty) - float(sold_qty)

    return jsonify({
        "month": f"{year}-{month:02d}",
        "opening_qty": round(opening_qty, 2),
        "received_qty": round(float(received_qty), 2),
        "out_qty": round(float(sold_qty), 2),
        "balance_qty": round(balance_qty, 2)
    })
