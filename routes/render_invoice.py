from flask import Blueprint, render_template, abort
from models.invoices import Invoice
from core.database import db

render_bp = Blueprint("render", __name__)

@render_bp.route("/invoice/<int:invoice_id>")
def render_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        abort(404)
    # Invoice has relationships to items, supplier, buyer, shipto
    return render_template("invoice.html",
                           invoice=invoice,
                           supplier=invoice.supplier,
                           buyer=invoice.buyer,
                           shipto=invoice.shipto,
                           items=invoice.items)
