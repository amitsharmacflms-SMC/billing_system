from flask import Blueprint, request, jsonify
from core.database import db
from models.invoices import Invoice
from models.invoice_items import InvoiceItem
from models.products import Product
from models.distributors import Distributor
from models.suppliers import Supplier
from decimal import Decimal
from datetime import datetime

invoice_bp = Blueprint("invoice", __name__, url_prefix="/api/invoices")

@invoice_bp.route("/create", methods=["POST"])
def create_invoice():
    data = request.get_json()
    # Minimal validation (expand as needed)
    supplier_id = data.get("supplier_id")
    buyer_id = data.get("buyer_id")
    shipto_id = data.get("shipto_id")
    invoice_no = data.get("invoice_no")
    items = data.get("items", [])  # list of dicts

    if not (supplier_id and buyer_id and invoice_no):
        return jsonify({"error": "supplier_id, buyer_id and invoice_no required"}), 400

    inv = Invoice(
        invoice_no=invoice_no,
        date=datetime.utcnow(),
        supplier_id=supplier_id,
        buyer_id=buyer_id,
        shipto_id=shipto_id
    )

    db.session.add(inv)
    db.session.flush()  # get invoice id

    total_pcs = 0
    total_cs = 0
    taxable_value = Decimal("0.00")
    total_gst = Decimal("0.00")
    grand_total = Decimal("0.00")

    for it in items:
        product_id = it.get("product_id")
        product = Product.query.get(product_id) if product_id else None
        product_name = (product.name if product else it.get("product_name")) or "Unknown"
        pcs = int(it.get("pcs", 0))
        cs = int(it.get("cs", 0))
        rate = Decimal(str(it.get("rate", "0")))
        disc = Decimal(str(it.get("disc_percent", "0")))
        gst_percent = Decimal(str(it.get("gst_percent", "0")))

        # taxable calculation example (rate * qty) less discount
        qty_multiplier = pcs  # or compute from cs * pack if needed
        raw_amount = rate * qty_multiplier
        taxable = raw_amount * (1 - (disc / 100))
        gst_amount = taxable * (gst_percent / 100)
        line_total = taxable + gst_amount

        item = InvoiceItem(
            invoice_id=inv.id,
            product_id=product_id,
            product_name=product_name,
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

        total_pcs += pcs
        total_cs += cs
        taxable_value += taxable
        total_gst += gst_amount
        grand_total += line_total

    inv.total_pcs = total_pcs
    inv.total_cs = total_cs
    inv.taxable_value = taxable_value
    inv.total_gst = total_gst
    inv.grand_total = grand_total

    db.session.commit()

    return jsonify({"message": "invoice created", "invoice_id": inv.id})
