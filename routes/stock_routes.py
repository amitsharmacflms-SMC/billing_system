from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from datetime import datetime, date
from calendar import monthrange

from core.database import db
from models.stock import StockEntry
from models.invoice_items import InvoiceItem
from models.products import Product

stock_bp = Blueprint("stock", __name__, url_prefix="/stock")


@stock_bp.route("/__ping__")
def ping():
    return {"status": "stock blueprint loaded"}


# -----------------------------------------
# ALL PRODUCTS
# -----------------------------------------
@stock_bp.route("/all-products", methods=["GET"])
@jwt_required()
def all_products():
    products = Product.query.order_by(Product.name).all()
    return jsonify([
        {"id": p.id, "name": p.name}
        for p in products
    ])


# -----------------------------------------
# BULK ADD STOCK
# -----------------------------------------
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

        entry = StockEntry(
            product_id=int(row["product_id"]),
            received_cs=qty,
            bill_no=bill_no,
            bill_date=bill_date,
            received_date=received_date,
            remarks=data.get("remarks", "")
        )
        db.session.add(entry)
        saved += 1

    db.session.commit()
    return {"message": f"{saved} items saved"}, 200


# -----------------------------------------
# STOCK REGISTER
# -----------------------------------------
@stock_bp.route("/stock-register", methods=["GET"])
@jwt_required()
def stock_register():

    month = request.args.get("month")   # YYYY-MM
    day = request.args.get("date")      # YYYY-MM-DD

    if not month and not day:
        return jsonify([])

    if month:
        y, m = map(int, month.split("-"))
        start_date = date(y, m, 1)
        end_date = date(y, m, monthrange(y, m)[1])
    else:
        start_date = datetime.strptime(day, "%Y-%m-%d").date()
        end_date = start_date

    rows = []

    products = Product.query.order_by(Product.name).all()

    for p in products:

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

        received_qty = db.session.query(
            func.coalesce(func.sum(StockEntry.received_cs), 0)
        ).filter(
            StockEntry.product_id == p.id,
            StockEntry.received_date.between(start_date, end_date)
        ).scalar()

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
