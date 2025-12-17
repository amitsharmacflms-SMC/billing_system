from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from datetime import datetime

from core.database import db
from models.invoice import Invoice
from models.invoice_items import InvoiceItem
from models.stock import StockEntry

invoice_bp = Blueprint("invoice", __name__, url_prefix="/api/invoices")


# -------------------------------------------------
# HELPER: GET AVAILABLE STOCK
# -------------------------------------------------
def get_available_stock(product_id):
    received = db.session.query(
        func.coalesce(func.sum(StockEntry.received_cs), 0)
    ).filter(
        StockEntry.product_id == product_id
    ).scalar()

    sold = db.session.query(
        func.coalesce(func.sum(InvoiceItem.cs), 0)
    ).filter(
        InvoiceItem.product_id == product_id
    ).scalar()

    return float(received - sold)


# -------------------------------------------------
# CREATE INVOICE  🔒 STOCK PROTECTED
# -------------------------------------------------
@invoice_bp.route("/create", methods=["POST"])
@jwt_required()
def create_invoice():
    data = request.get_json()
    items = data.get("items", [])

    if not items:
        return {"error": "Invoice items required"}, 400

    # 🔒 STOCK VALIDATION
    for item in items:
        product_id = int(item["product_id"])
        qty = float(item["cs"])

        available = get_available_stock(product_id)

        if qty > available:
            return {
                "error": "Insufficient stock",
                "product_id": product_id,
                "available_stock": available
            }, 400

    # -------------------------------------------------
    # CREATE INVOICE (SAFE)
    # -------------------------------------------------
    invoice = Invoice(
        invoice_no=data.get("invoice_no"),
        invoice_date=datetime.strptime(data.get("invoice_date"), "%Y-%m-%d").date(),
        customer_name=data.get("customer_name")
    )
    db.session.add(invoice)
    db.session.flush()

    for item in items:
        row = InvoiceItem(
            invoice_id=invoice.id,
            product_id=int(item["product_id"]),
            cs=float(item["cs"])
        )
        db.session.add(row)

    db.session.commit()

    return {"message": "Invoice created successfully"}, 201
