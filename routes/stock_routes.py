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

@stock_bp.route("/all-products", methods=["GET"])
@jwt_required()
def all_products():
    products = Product.query.order_by(Product.name).all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name
        }
        for p in products
    ])
# -------------------------------------------------
# STOCK REGISTER (MONTH / DATE FILTER)
# -------------------------------------------------
@stock_bp.route("/stock-register", methods=["GET"])
@jwt_required()
def stock_register():

    month = request.args.get("month")        # YYYY-MM
    filter_date = request.args.get("date")   # YYYY-MM-DD

    if not month and not filter_date:
        return jsonify([])

    # -----------------------------
    # DATE RANGE
    # -----------------------------
    if month:
        year, mon = map(int, month.split("-"))
        start_date = date(year, mon, 1)
        end_date = date(year, mon, monthrange(year, mon)[1])
    else:
        start_date = datetime.strptime(filter_date, "%Y-%m-%d").date()
        end_date = start_date

    rows = []

    products = Product.query.order_by(Product.name).all()

    for p in products:

        # -----------------------------
        # OPENING STOCK
        # -----------------------------
        opening_in = db.session.query(
            func.coalesce(func.sum(StockEntry.received_cs), 0)
        ).filter(
            StockEntry.product_id == p.id,
            StockEntry.received_date < start_date
        ).scalar()

        opening_out = db.session.query(
            func.coalesce(func.sum(InvoiceItem.cs), 0)
        ).filter(
            InvoiceItem.product_id == p.id,
            InvoiceItem.created_at < start_date
        ).scalar()

        opening_qty = opening_in - opening_out

        # -----------------------------
        # RECEIVED IN PERIOD
        # -----------------------------
        received_qty = db.session.query(
            func.coalesce(func.sum(StockEntry.received_cs), 0)
        ).filter(
            StockEntry.product_id == p.id,
            StockEntry.received_date.between(start_date, end_date)
        ).scalar()

        # -----------------------------
        # SOLD IN PERIOD
        # -----------------------------
        out_qty = db.session.query(
            func.coalesce(func.sum(InvoiceItem.cs), 0)
        ).filter(
            InvoiceItem.product_id == p.id,
            InvoiceItem.created_at.between(start_date, end_date)
        ).scalar()

        balance_qty = opening_qty + received_qty - out_qty

        if opening_qty == 0 and received_qty == 0 and out_qty == 0:
            continue

        rows.append({
            "month": start_date.strftime("%b-%Y"),
            "date": start_date.strftime("%Y-%m-%d"),
            "opening_qty": float(opening_qty),
            "received_qty": float(received_qty),
            "out_qty": float(out_qty),
            "balance_qty": float(balance_qty)
        })

    return jsonify(rows)


# -------------------------------------------------
# EXPORT STOCK REGISTER (EXCEL)
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
