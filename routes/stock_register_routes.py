from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from core.database import db
from models.stock import StockEntry
from models.invoice_items import InvoiceItem
from datetime import date

stock_register_bp = Blueprint(
    "stock_register",
    __name__,
    url_prefix="/stock-register"
)


@stock_register_bp.route("/yearly", methods=["GET"])
@jwt_required()
def yearly_stock_register():
    product_id = request.args.get("product_id")
    year = request.args.get("year")

    if not product_id or not year:
        return {"error": "product_id and year required"}, 400

    year = int(year)
    product_id = int(product_id)

    # -------------------------------
    # Opening stock before Jan 1
    # -------------------------------
    year_start = date(year, 1, 1)

    opening_received = db.session.query(
        db.func.coalesce(db.func.sum(StockEntry.received_cs), 0)
    ).filter(
        StockEntry.product_id == product_id,
        StockEntry.received_date < year_start
    ).scalar()

    opening_sold = db.session.query(
        db.func.coalesce(db.func.sum(InvoiceItem.cs), 0)
    ).filter(
        InvoiceItem.product_id == product_id,
        InvoiceItem.created_at < year_start
    ).scalar()

    opening_balance = float(opening_received) - float(opening_sold)

    results = []
    running_balance = opening_balance

    # -------------------------------
    # Loop through 12 months
    # -------------------------------
    for month in range(1, 13):

        received = db.session.query(
            db.func.coalesce(db.func.sum(StockEntry.received_cs), 0)
        ).filter(
            StockEntry.product_id == product_id,
            db.extract("year", StockEntry.received_date) == year,
            db.extract("month", StockEntry.received_date) == month
        ).scalar()

        sold = db.session.query(
            db.func.coalesce(db.func.sum(InvoiceItem.cs), 0)
        ).filter(
            InvoiceItem.product_id == product_id,
            db.extract("year", InvoiceItem.created_at) == year,
            db.extract("month", InvoiceItem.created_at) == month
        ).scalar()

        received = float(received)
        sold = float(sold)

        closing = running_balance + received - sold

        results.append({
            "month": f"{year}-{month:02d}",
            "opening_qty": round(running_balance, 2),
            "received_qty": round(received, 2),
            "out_qty": round(sold, 2),
            "balance_qty": round(closing, 2)
        })

        running_balance = closing

    return jsonify(results), 200
