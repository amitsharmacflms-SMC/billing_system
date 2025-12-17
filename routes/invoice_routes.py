from flask import Blueprint, request, jsonify
from core.database import db
from sqlalchemy import func
from decimal import Decimal
from datetime import datetime

from models.invoices import Invoice
from models.invoice_items import InvoiceItem
from models.products import Product
from models.stock import StockEntry

# ---------------------------------------------------
# BLUEPRINT (THIS WAS MISSING)
# ---------------------------------------------------
invoice_bp = Blueprint("invoice", __name__, url_prefix="/api/invoices")

# ---------------------------------------------------
# STOCK HELPER
# ---------------------------------------------------
def get_available_cs(product_id):
    received = db.session.query(
        func.coalesce(func.sum(StockEntry.received_cs), 0)
    ).filter(
        StockEntry.product_id == product_id
    ).scalar()

    issued = db.session.query(
        func.coalesce(func.sum(InvoiceItem.cs), 0)
    ).filter(
        InvoiceItem.product_id == product_id
    ).scalar()

    return int(received) - int(issued)

# ---------------------------------------------------
# CREATE INVOICE (NEGATIVE STOCK BLOCKED)
# ---------------------------------------------------
@invoice_bp.route("/create", methods=["POST"])
def create_invoice():
    data = request.get_json() or {}

    invoice_no = data.get("invoice_no")
    distributor_id = data.get("buyer_id")
    items = data.get("items", [])

    if not invoice_no or not distributor_id:
        return jsonify({"error": "Invoice number and distributor required"}), 400

    if not items:
        return jsonify({"error": "Invoice items required"}), 400

    # -----------------------------
    # 🔒 STOCK VALIDATION
    # -----------------------------
    for it in items:
        product_id = it.get("product_id")
        cs = int(it.get("cs", 0))

        if cs <= 0:
            continue

        available_cs = get_available_cs(product_id)

        if cs > available_cs:
            product = Product.query.get(product_id)
            name = product.name if product else f"Product ID {product_id}"

            return jsonify({
                "error": (
                    f"Insufficient stock for {name}. "
                    f"Available CS: {available_cs}, Requested CS: {cs}"
                )
            }), 400

    # -----------------------------
    # CREATE INVOICE
    # -----------------------------
    inv = Invoice(
        invoice_number=invoice_no,
        date=datetime.utcnow(),
        distributor_id=distributor_id,
        total_amount=0,
        total_tax=0,
        grand_total=0
    )

    db.session.add(inv)
    db.session.flush()  # get inv.id

    total_taxable = Decimal("0.00")
    total_gst = Decimal("0.00")
    grand_total = Decimal("0.00")

    for it in items:
        product_id = it.get("product_id")
        product = Product.query.get(product_id)

        pcs = int(it.get("pcs", 0))
        cs = int(it.get("cs", 0))
        rate = Decimal(str(it.get("rate", 0)))
        disc = Decimal(str(it.get("disc_percent", 0)))
        gst_percent = Decimal(str(it.get("gst_percent", 0)))

        taxable = rate * pcs * (Decimal("1.00") - (disc / Decimal("100")))
        gst_amount = taxable * (gst_percent / Decimal("100"))
        line_total = taxable + gst_amount

        item = InvoiceItem(
            invoice_id=inv.id,
            product_id=product_id,
            product_name=product.name if product else it.get("product_name", ""),
            hsn=product.hsn if product else it.get("hsn"),
            pcs=pcs,
            cs=cs,
            rate=rate,
            disc_percent=disc,
            taxable=taxable,
            gst_percent=gst_percent,
            gst_amount=gst_amount,
            total=line_total
        )

        db.session.add(item)

        total_taxable += taxable
        total_gst += gst_amount
        grand_total += line_total

    inv.total_amount = float(total_taxable)
    inv.total_tax = float(total_gst)
    inv.grand_total = float(grand_total)

    db.session.commit()

    return jsonify({
        "message": "Invoice created successfully",
        "invoice_id": inv.id
    })
