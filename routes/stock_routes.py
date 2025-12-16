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

# ✅ DEFINE BLUEPRINT FIRST (THIS FIXES YOUR ERROR)
stock_bp = Blueprint("stock", __name__, url_prefix="/stock")


# -------------------------------------------------
# STOCK SUMMARY (NO DATE / NO MONTH)
# -------------------------------------------------
@stock_bp.route("/stock-summary", methods=["GET"])
@jwt_required()
def stock_summary():

    rows = []

    products = Product.query.order_by(Product.name).all()

    for p in products:
        opening_qty = 0  # LOCKED

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
# OPTIONAL: EXPORT EXCEL
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
