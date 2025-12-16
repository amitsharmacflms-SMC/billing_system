from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from datetime import datetime
from io import BytesIO
import pandas as pd

from core.database import db
from models.stock import StockEntry
from models.products import Product
from models.invoice_items import InvoiceItem

# -------------------------------------------------
# BLUEPRINT
# -------------------------------------------------
stock_bp = Blueprint("stock", __name__, url_prefix="/stock")

# -------------------------------------------------
# BULK ADD STOCK (RECEIVED STOCK PAGE)
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

        entry = StockEntry(
            product_id=int(row["product_id"]),
            bill_no=bill_no,
            bill_date=bill_date,
            received_date=received_date,
            received_cs=qty,
            remarks=data.get("remarks", "")
        )
        db.session.add(entry)
        count += 1

    db.session.commit()
    return {"message": f"{count} items saved"}, 200


# -------------------------------------------------
# ALL PRODUCTS (FOR RECEIVED STOCK PAGE)
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
# STOCK SUMMARY (NO DATE / NO MONTH)
# Opening = 0 (BUSINESS RULE)
# -------------------------------------------------
@stock_bp.route("/stock-summary", methods=["GET"])
@jwt_required()
def stock_summary():

    rows = []

    products = Product.query.order_by(Product.name).all()

    for p in products:
        opening_qty = 0

        received_qty = db.session.query(
            func.coalesce(func.sum(StockEntry.received_cs), 0)
        ).filter(
            StockEntry.product_id == p.id
        ).scalar()

        out_qty = db.session.query(
            func.coalesce(func.sum(InvoiceItem.cs), 0)
        ).filter(
            InvoiceItem.product_id == p.id
        ).scalar()

        balance_qty = opening_qty + received_qty - out_qty

        rows.append({
            "product": p.name,
            "opening_qty": float(opening_qty),
            "received_qty": float(received_qty),
            "out_qty": float(out_qty),
            "balance_qty": float(balance_qty)
        })

    return jsonify(rows)


# -------------------------------------------------
# EXPORT STOCK SUMMARY (EXCEL)
# -------------------------------------------------
@stock_bp.route("/stock-summary/export", methods=["GET"])
@jwt_required()
def stock_summary_export():

    data = stock_summary().json
    df = pd.DataFrame(data)

    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(
        output,
        download_name="Stock_Summary.xlsx",
        as_attachment=True
    )
