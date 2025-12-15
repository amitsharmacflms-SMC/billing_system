from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from datetime import datetime, date
from calendar import monthrange
from io import BytesIO
import pandas as pd

from core.database import db
from models.stock import StockEntry
from models.invoice_items import InvoiceItem
from models.products import Product

stock_bp = Blueprint("stock", __name__, url_prefix="/stock")


# -------------------------------------------------
# PING (DEBUG)
# -------------------------------------------------
@stock_bp.route("/__ping__", methods=["GET"])
def stock_ping():
    return {"status": "stock blueprint loaded"}


# -------------------------------------------------
# ALL PRODUCTS (DROPDOWN)
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

    saved = 0

    for row in entries:
        qty = float(row.get("qty", 0))
        if qty <= 0:
            continue

        db.session.add(StockEntry(
            product_id=int(row["product_id"]),
            bill_no=bill_no,
            bill_date=bill_date,
            received_date=received_date,
            received_cs=qty,
            remarks=data.get("remarks", "")
        ))
        saved += 1

    db.session.commit()
    return {"message": f"{saved} items saved"}, 200


# -------------------------------------------------
# STOCK REGISTER (MONTH / DATE)
# -------------------------------------------------
@stock_bp.route("/stock-register", methods=["GET"])
@jwt_required()
def stock_register():

    month = request.args.get("month")        # YYYY-MM
    filter_date = request.args.get("date")   # YYYY-MM-DD

    # -----------------------------
    # Decide date range (SAFE)
    # -----------------------------
    if month:
        try:
            year, mon = map(int, month.split("-"))
            start_date = date(year, mon, 1)
            end_date = date(year, mon, monthrange(year, mon)[1])
        except Exception:
            return {"error": "Invalid month format"}, 400

    elif filter_date:
        try:
            start_date = datetime.strptime(filter_date, "%Y-%m-%d").date()
            end_date = start_date
        except Exception:
            return {"error": "Invalid date format"}, 400

    else:
        return jsonify([])

    rows = []
    products = Product.query.order_by(Product.name).all()

    for p in products:

        opening_in = db.session.query(
            func.coalesce(func.sum(StockEntry.received_cs), 0)
        ).filter(
            StockEntry.product_id == p.id,
            StockEntry.date < start_date
        ).scalar()

        opening_out = db.session.query(
            func.coalesce(func.sum(InvoiceItem.cs), 0)
        ).filter(
            InvoiceItem.product_id == p.id,
            InvoiceItem.created_at < start_date
        ).scalar()

        opening = opening_in - opening_out

        received = db.session.query(
            func.coalesce(func.sum(StockEntry.received_cs), 0)
        ).filter(
            StockEntry.product_id == p.id,
            StockEntry.date.between(start_date, end_date)
        ).scalar()

        sold = db.session.query(
            func.coalesce(func.sum(InvoiceItem.cs), 0)
        ).filter(
            InvoiceItem.product_id == p.id,
            InvoiceItem.created_at.between(start_date, end_date)
        ).scalar()

        balance = opening + received - sold

        if opening == received == sold == 0:
            continue

        rows.append({
            "product": p.name,
            "opening_qty": float(opening),
            "received_qty": float(received),
            "out_qty": float(sold),
            "balance_qty": float(balance)
        })

    return jsonify(rows)


# -------------------------------------------------
# EXPORT STOCK REGISTER (ALL PRODUCTS)
# -------------------------------------------------
@stock_bp.route("/stock-register/export", methods=["GET"])
@jwt_required()
def stock_register_export():

    month = request.args.get("month")
    filter_date = request.args.get("date")

    with stock_bp.test_request_context(
        f"/stock-register?month={month}&date={filter_date}"
    ):
        data = stock_register().json

    df = pd.DataFrame(data)

    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(
        output,
        download_name="Stock_Register.xlsx",
        as_attachment=True
    )
