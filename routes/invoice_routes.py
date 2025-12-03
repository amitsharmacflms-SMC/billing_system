from flask import Blueprint, request, jsonify
from core.database import db
from models.invoices import Invoice, InvoiceItem
from models.distributors import Distributor
from models.products import Product
import datetime

invoice_bp = Blueprint("invoice", __name__, url_prefix="/invoice")


# ---------------------------------------------------
# CREATE INVOICE
# ---------------------------------------------------
@invoice_bp.route("/create", methods=["POST"])
def create_invoice():
    try:
        data = request.get_json()

        distributor_id = data.get("distributor_id")
        items_data = data.get("items", [])
        invoice_no = data.get("invoice_no")
        invoice_date = data.get("invoice_date", datetime.date.today().isoformat())

        if not distributor_id or not items_data:
            return jsonify({"error": "Missing distributor or invoice items"}), 400

        distributor = Distributor.query.get(distributor_id)
        if not distributor:
            return jsonify({"error": "Distributor not found"}), 404

        invoice = Invoice(
            distributor_id=distributor_id,
            invoice_no=invoice_no,
            invoice_date=invoice_date
        )

        db.session.add(invoice)
        db.session.flush()  # get invoice.id before committing

        grand_total = 0

        for item in items_data:
            product_id = item.get("product_id")
            qty_pcs = item.get("qty_pcs", 0)
            qty_cs = item.get("qty_cs", 0)
            rate = item.get("rate", 0)
            discount = item.get("discount", 0)
            gst = item.get("gst", 0)

            # calculate taxable amount
            taxable = rate - (rate * (discount / 100))
            total = taxable + (taxable * (gst / 100))

            grand_total += total

            invoice_item = InvoiceItem(
                invoice_id=invoice.id,
                product_id=product_id,
                qty_pcs=qty_pcs,
                qty_cs=qty_cs,
                rate=rate,
                discount=discount,
                taxable=taxable,
                gst=gst,
                total=total
            )

            db.session.add(invoice_item)

        invoice.grand_total = grand_total
        db.session.commit()

        return jsonify({
            "message": "Invoice created",
            "invoice_id": invoice.id,
            "grand_total": grand_total
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------
# GET INVOICE DETAILS
# ---------------------------------------------------
@invoice_bp.route("/<int:invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404

    items = InvoiceItem.query.filter_by(invoice_id=invoice_id).all()
    item_list = []

    for i in items:
        product = Product.query.get(i.product_id)
        item_list.append({
            "product": product.name if product else "Unknown",
            "qty_pcs": i.qty_pcs,
            "qty_cs": i.qty_cs,
            "rate": i.rate,
            "discount": i.discount,
            "taxable": i.taxable,
            "gst": i.gst,
            "total": i.total
        })

    return jsonify({
        "invoice_no": invoice.invoice_no,
        "date": invoice.invoice_date,
        "distributor_id": invoice.distributor_id,
        "grand_total": invoice.grand_total,
        "items": item_list
    })


# ---------------------------------------------------
# EXPORT JSON FOR E-INVOICE
# ---------------------------------------------------
@invoice_bp.route("/export-json/<int:invoice_id>", methods=["GET"])
def export_invoice_json(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404

    items = InvoiceItem.query.filter_by(invoice_id=invoice_id).all()

    json_data = {
        "InvoiceNo": invoice.invoice_no,
        "InvoiceDate": invoice.invoice_date,
        "SellerGSTIN": "19AGXPA6418M1ZQ",
        "BuyerGSTIN": "",
        "Items": []
    }

    for item in items:
        product = Product.query.get(item.product_id)
        json_data["Items"].append({
            "Description": product.name if product else "",
            "HSN": product.hsn if product else "",
            "QtyPCS": item.qty_pcs,
            "QtyCS": item.qty_cs,
            "Rate": item.rate,
            "Taxable": item.taxable,
            "GST": item.gst,
            "Total": item.total
        })

    return jsonify(json_data)
