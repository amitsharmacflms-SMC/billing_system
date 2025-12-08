from flask import Blueprint, request, jsonify
from core.database import db
from models.stock import StockEntry
from models.products import Product
from models.invoices import Invoice, InvoiceItemModel
from datetime import datetime

stock_bp = Blueprint("stock", __name__, url_prefix="/stock")

# -------------------------
# ADD STOCK ENTRY (Stock IN)
# -------------------------
@stock_bp.route("/add", methods=["POST"])
def add_stock():
    data = request.get_json()

    entry = StockEntry(
        product_id = data["product_id"],
        date = datetime.strptime(data["date"], "%Y-%m-%d"),
        received_cs = float(data["received_cs"]),
        invoice_no = data.get("invoice_no"),
        remarks = data.get("remarks")
    )

    db.session.add(entry)
    db.session.commit()

    return jsonify({"message": "Stock added successfully"}), 200


# -------------------------
# GET CURRENT STOCK FOR ALL PRODUCTS
# -------------------------
@stock_bp.route("/summary", methods=["GET"])
def stock_summary():

    products = Product.query.all()
    result = []

    for p in products:

        # Total Received in CS
        received = db.session.query(
            db.func.sum(StockEntry.received_cs)
        ).filter_by(product_id=p.id).scalar() or 0

        # Total Sold in CS (calculated from invoice items)
        sold_pcs = db.session.query(
    db.func.sum(InvoiceItemModel.qty)
).filter_by(product_id=p.id).scalar() or 0


        # pack size (PCS per case)
        pack = p.pack or 1
        sold_cs = sold_pcs / pack

        current_stock = received - sold_cs

        result.append({
            "product_id": p.id,
            "product_name": p.name,
            "received_cs": round(received, 2),
            "sold_cs": round(sold_cs, 2),
            "current_stock_cs": round(current_stock, 2)
        })

    return jsonify(result)
