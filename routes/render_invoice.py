from flask import Blueprint, render_template, abort, Response
from models.invoices import Invoice
from models.invoice_items import InvoiceItem
from weasyprint import HTML

render_invoice_bp = Blueprint("render_invoice", __name__)

def build_invoice_data(invoice):
    items = InvoiceItem.query.filter_by(invoice_id=invoice.id).all()
    return {
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

@render_invoice_bp.route("/invoice/<int:invoice_id>")
def view_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return render_template("invoice.html", invoice=build_invoice_data(invoice))

@render_invoice_bp.route("/invoice/<int:invoice_id>/pdf")
def invoice_pdf(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    html = render_template("invoice.html", invoice=build_invoice_data(invoice))
    pdf = HTML(string=html).write_pdf()
    return Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=Invoice_{invoice.invoice_number}.pdf"}
    )
