from flask import Blueprint, request, jsonify
from core.database import db
from models.stock import StockEntry
from models.products import Product
from models.invoices import Invoice
from models.invoice_items import InvoiceItem   # ✅ Correct import
from datetime import datetime
from sqlalchemy import func

stock_bp = Blueprint("stock", __name__, url_prefix="/stock")


# --------------------------------------
# Helper: Parse date
# --------------------------------------
def _parse_date(d):
    if not d:
        return datetime.utcnow().date()
    try:
        return datetime.strptime(d, "%Y-%m-%d").date()
    except:
        return datetime.utcnow().date()


# --------------------------------------
# ADD STOCK ENTRY (STOCK IN)
# --------------------------------------
@stock_bp.route("/add", methods=["POST"])
def add_stock():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON payload required"}), 400

    product_id = data.get("product_id")
    received_cs = data.get("received_cs")

    if not product_id:
        return jsonify({"error": "product_id required"}), 400

    if not received_cs:
        return jsonify({"error": "received_cs required"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    entry = StockEntry(
        product_id=product_id,
        date=_parse_date(data.get("date")),
        received_cs=float(received_cs),
        invoice_no=data.get("invoice_no"),
        remarks=data.get("remarks")
    )

    db.session.add(entry)
    db.session.commit()

    return jsonify({"message": "Stock Added Successfully"}), 200


# --------------------------------------
# STOCK SUMMARY (FULL INVENTORY)
# --------------------------------------
@stock_bp.route("/summary", methods=["GET"])
def stock_summary():

    products = Product.query.all()
    result = []

    for p in products:

        # Total received CS from StockEntry table
        received_cs = db.session.query(
            func.coalesce(func.sum(StockEntry.received_cs), 0)
        ).filter(StockEntry.product_id == p.id).scalar()

        # Total sold PCS from invoice items
        sold_pcs = db.session.query(
            func.coalesce(func.sum(InvoiceItem.pcs), 0)
        ).filter(InvoiceItem.product_id == p.id).scalar()

        # Convert PCS → CS using product pack size
        try:
            pack = float(p.pack or 1)
            if pack == 0:
                pack = 1
        except:
            pack = 1

        sold_cs = sold_pcs / pack

        current_stock = received_cs - sold_cs

        result.append({
            "product_id": p.id,
            "product_name": p.name,
            "received_cs": round(received_cs, 3),
            "sold_pcs": sold_pcs,
            "sold_cs": round(sold_cs, 3),
            "current_stock_cs": round(current_stock, 3),
            "pack": pack,
        })

    return jsonify(result), 200


# --------------------------------------
# STOCK LEDGER (LIST ENTRIES)
# --------------------------------------
@stock_bp.route("/entries", methods=["GET"])
def stock_entries():

    product_id = request.args.get("product_id")
    q = StockEntry.query.order_by(StockEntry.date.desc(), StockEntry.id.desc())

    if product_id:
        q = q.filter(StockEntry.product_id == product_id)

    rows = q.all()
    data = []

    for r in rows:
        data.append({
            "id": r.id,
            "product_id": r.product_id,
            "product_name": r.product.name if r.product else "",
            "date": r.date.strftime("%Y-%m-%d"),
            "received_cs": r.received_cs,
            "invoice_no": r.invoice_no,
            "remarks": r.remarks
        })

    return jsonify(data), 200


# --------------------------------------
# CURRENT STOCK FOR SINGLE PRODUCT
# --------------------------------------
@stock_bp.route("/product/<int:product_id>/current", methods=["GET"])
def stock_product_current(product_id):

    p = Product.query.get(product_id)
    if not p:
        return jsonify({"error": "Product not found"}), 404

    received_cs = db.session.query(
        func.coalesce(func.sum(StockEntry.received_cs), 0)
    ).filter(StockEntry.product_id == product_id).scalar()

    sold_pcs = db.session.query(
        func.coalesce(func.sum(InvoiceItem.pcs), 0)
    ).filter(InvoiceItem.product_id == product_id).scalar()

    pack = float(p.pack or 1)
    if pack == 0:
        pack = 1

    sold_cs = sold_pcs / pack
    current_stock = received_cs - sold_cs

    return jsonify({
        "product_id": p.id,
        "product_name": p.name,
        "received_cs": round(received_cs, 3),
        "sold_pcs": sold_pcs,
        "sold_cs": round(sold_cs, 3),
        "current_stock_cs": round(current_stock, 3),
        "pack": pack
    }), 200
