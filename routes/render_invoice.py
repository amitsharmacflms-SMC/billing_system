from flask import Blueprint, render_template, abort
from models.invoices import Invoice
from models.invoice_items import InvoiceItem

render_invoice_bp = Blueprint("render_invoice", __name__)

@render_invoice_bp.route("/invoice/<int:invoice_id>")
def view_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        abort(404)

    items = InvoiceItem.query.filter_by(invoice_id=invoice_id).all()

    invoice_data = {
        "invoice_number": invoice.invoice_number,
        "date": invoice.date,
        "supplier": invoice.distributor.supplier,
        "distributor": invoice.distributor,
        "items": items,
        "totals": {
            "taxable_total": invoice.total_amount,
            "gst_total": invoice.total_tax,
            "grand_total": invoice.grand_total
        }
    }

    return render_template("invoice.html", invoice=invoice_data)
