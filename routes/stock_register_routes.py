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
# HELPER: BUILD STOCK REGISTER DATA
# -------------------------------------------------
def _build_stock_register(month=None, filter_date=None):

    if not month and not filter_date:
        return []

    # Date range
    if month:
        year, mon = map(int, month.split("-"))
        start_date = date(year, mon, 1)
        last_day = monthrange(year, mon)[1]
        end_date = date(year, mon, last_day)
    else:
        start_date = datetime.strptime(filter_date, "%Y-%m-%d").date()
        end_date = start_date

    results = []

    products = Product.query.order_by(Product.name).all()

    for product in products:

        # Opening stock
        opening_received = db.session.query(
            func.coalesce(func.sum(StockEntry.received_cs), 0)
        ).filter(
            StockEntry.product_id == product.id,
            StockEntry.received_date < start_date
        ).scalar()

        opening_out = db.session.query(
            func.coalesce(func.sum(InvoiceItem.cs), 0)
        ).filter(
            InvoiceItem.product_id == product.id,
            InvoiceItem.created_at < start_date
        ).scalar()

        opening_qty = opening_received - opening_out

        # Received during period
        received_qty = db.session.query(
            func.coalesce(func.sum(StockEntry.received_cs), 0)
        ).filter(
            StockEntry.product_id == product.id,
            StockEntry.received_date.between(start_date, end_date)
        ).scalar()

        # Sold during period
        out_qty = db.session.query(
            func.coalesce(func.sum(InvoiceItem.cs), 0)
        ).filter(
            InvoiceItem.product_id == product.id,
            InvoiceItem.created_at.between(start_date, end_date)
        ).scalar()

        balance_qty = opening_qty + received_qty - out_qty

        # Skip zero rows
        if opening_qty == 0 and received_qty == 0 and out_qty == 0:
            continue

        results.append({
            "month": start_date.strftime("%b-%Y"),
            "date": start_date.strftime("%Y-%m-%d"),
            "opening_qty": float(opening_qty),
            "received_qty": float(received_qty),
            "out_qty": float(out_qty),
            "balance_qty": float(balance_qty)
        })

    return results


# -------------------------------------------------
# GET ALL PRODUCTS (DROPDOWNS)
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
        if float(row["qty"]) <= 0:
            continue

        entry = StockEntry(
            product_id=int(row["product_id"]),
            bill_no=bill_no,
            bill_date=bill_date,
            received_date=received_date,
            received_cs=float(row["qty"]),
            remarks=data.get("remarks", "")
        )
        db.session.add(entry)
        count += 1

    db.session.commit()
    return {"message": f"{count} items saved"}, 200


# -------------------------------------------------
# STOCK REGISTER API
# -------------------------------------------------
@stock_bp.route("/stock-register", methods=["GET"])
@jwt_required()
def stock_register():
    month = request.args.get("month")
    filter_date = request.args.get("date")
    return jsonify(_build_stock_register(month, filter_date))


# -------------------------------------------------
# STOCK REGISTER EXPORT (EXCEL)
# -------------------------------------------------
@stock_bp.route("/stock-register/export", methods=["GET"])
@jwt_required()
def stock_register_export():
    month = request.args.get("month")
    filter_date = request.args.get("date")

    data = _build_stock_register(month, filter_date)

    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(
        output,
        download_name="Stock_Register.xlsx",
        as_attachment=True
    )
