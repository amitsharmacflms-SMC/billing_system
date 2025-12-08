from flask import Blueprint, request, jsonify
from core.database import db
from models.stock import StockEntry
from models.products import Product
# NOTE: import correct invoice item model name used in your codebase
from models.invoices import Invoice, InvoiceItemModel
from datetime import datetime
from sqlalchemy import func

stock_bp = Blueprint("stock", __name__, url_prefix="/stock")


# -------------------------
# Helper: parse date (YYYY-MM-DD)
# -------------------------
def _parse_date(d):
    if not d:
        return datetime.utcnow().date()
    if isinstance(d, datetime):
        return d.date()
    try:
        return datetime.strptime(d, "%Y-%m-%d").date()
    except Exception:
        # try other common formats
        try:
            return datetime.strptime(d, "%d-%m-%Y").date()
        except Exception:
            raise ValueError("Invalid date format, expected YYYY-MM-DD")


# -------------------------
# Add Stock Entry (Stock IN)
# POST /stock/add
# body: { product_id, date (YYYY-MM-DD optional), received_cs, invoice_no (optional), remarks (optional) }
# -------------------------
@stock_bp.route("/add", methods=["POST"])
def add_stock():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "JSON payload required"}), 400

    product_id = data.get("product_id")
    if product_id is None:
        return jsonify({"error": "product_id is required"}), 400

    try:
        product = Product.query.get(int(product_id))
    except Exception:
        return jsonify({"error": "invalid product_id"}), 400

    if not product:
        return jsonify({"error": "product not found"}), 404

    try:
        received_cs = float(data.get("received_cs", 0))
    except Exception:
        return jsonify({"error": "received_cs must be a number"}), 400

    if received_cs == 0:
        return jsonify({"error": "received_cs should be non-zero"}), 400

    try:
        date = _parse_date(data.get("date"))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    invoice_no = data.get("invoice_no")
    remarks = data.get("remarks")

    entry = StockEntry(
        product_id=product.id,
        date=date,
        received_cs=received_cs,
        invoice_no=invoice_no,
        remarks=remarks
    )

    db.session.add(entry)
    db.session.commit()

    return jsonify({
        "message": "Stock entry added",
        "entry_id": entry.id,
        "product_id": product.id,
        "product_name": product.name,
        "received_cs": entry.received_cs,
        "date": entry.date.isoformat()
    }), 201


# -------------------------
# Stock Summary for ALL PRODUCTS
# GET /stock/summary
# returns list: product_id, product_name, received_cs, sold_cs, current_stock_cs
# -------------------------
@stock_bp.route("/summary", methods=["GET"])
def stock_summary():
    products = Product.query.order_by(Product.name).all()
    result = []

    for p in products:
        # Sum of received CS for product
        received = db.session.query(func.coalesce(func.sum(StockEntry.received_cs), 0.0)) \
            .filter(StockEntry.product_id == p.id).scalar() or 0.0

        # Sum of sold PCS from invoice items (use InvoiceItemModel.qty or your model's qty field)
        sold_pcs = db.session.query(func.coalesce(func.sum(InvoiceItemModel.qty), 0)) \
            .filter(InvoiceItemModel.product_id == p.id).scalar() or 0

        # Convert sold pcs -> CS using pack (pcs per case). If pack is zero/None use 1 to avoid div by zero.
        try:
            pack = float(p.pack) if p.pack else 1.0
            if pack == 0:
                pack = 1.0
        except Exception:
            pack = 1.0

        sold_cs = float(sold_pcs) / pack
        current_stock = float(received) - float(sold_cs)

        result.append({
            "product_id": p.id,
            "product_name": p.name,
            "received_cs": round(float(received), 4),
            "sold_pcs": float(sold_pcs),
            "sold_cs": round(float(sold_cs), 4),
            "current_stock_cs": round(float(current_stock), 4),
            "pack": pack
        })

    return jsonify(result), 200


# -------------------------
# List Stock Entries (ledger)
# GET /stock/entries
# optional query params: product_id, limit, offset
# -------------------------
@stock_bp.route("/entries", methods=["GET"])
def stock_entries():
    product_id = request.args.get("product_id", type=int)
    limit = request.args.get("limit", default=200, type=int)
    offset = request.args.get("offset", default=0, type=int)

    q = StockEntry.query.order_by(StockEntry.date.desc(), StockEntry.id.desc())
    if product_id:
        q = q.filter(StockEntry.product_id == product_id)

    total = q.count()
    rows = q.offset(offset).limit(limit).all()

    items = []
    for r in rows:
        items.append({
            "id": r.id,
            "product_id": r.product_id,
            "product_name": getattr(r.product, "name", None),
            "date": r.date.isoformat() if hasattr(r.date, "isoformat") else str(r.date),
            "received_cs": float(r.received_cs),
            "invoice_no": r.invoice_no,
            "remarks": r.remarks
        })

    return jsonify({"total": total, "count": len(items), "rows": items}), 200


# -------------------------
# Current stock for a single product
# GET /stock/product/<int:product_id>/current
# -------------------------
@stock_bp.route("/product/<int:product_id>/current", methods=["GET"])
def product_current(product_id):
    p = Product.query.get(product_id)
    if not p:
        return jsonify({"error": "product not found"}), 404

    received = db.session.query(func.coalesce(func.sum(StockEntry.received_cs), 0.0)) \
        .filter(StockEntry.product_id == p.id).scalar() or 0.0

    sold_pcs = db.session.query(func.coalesce(func.sum(InvoiceItemModel.qty), 0)) \
        .filter(InvoiceItemModel.product_id == p.id).scalar() or 0

    try:
        pack = float(p.pack) if p.pack else 1.0
        if pack == 0:
            pack = 1.0
    except Exception:
        pack = 1.0

    sold_cs = float(sold_pcs) / pack
    current_stock = float(received) - float(sold_cs)

    return jsonify({
        "product_id": p.id,
        "product_name": p.name,
        "received_cs": round(float(received), 4),
        "sold_pcs": float(sold_pcs),
        "sold_cs": round(float(sold_cs), 4),
        "current_stock_cs": round(float(current_stock), 4),
        "pack": pack
    }), 200
