# routes/render_invoice.py
from flask import Blueprint, render_template, abort, current_app, url_for, make_response
from core.database import db
from sqlalchemy import func
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

# Import your models (adjust names/paths if your project uses different module names)
from models.invoices import Invoice
from models.invoice_items import InvoiceItem
from models.distributors import Distributor
from models.products import Product
from models.suppliers import Supplier

render_bp = Blueprint("render_invoice", __name__, url_prefix="")

# ---- helpers ----
def to_decimal(x):
    return Decimal(str(x or 0)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def amount_in_words_rupees(amount):
    """
    Try to import num2words. If not available, fall back to a simple stub.
    """
    try:
        from num2words import num2words
        whole = int(amount)
        fraction = int(round((amount - whole) * 100))
        words = num2words(whole, lang="en_IN").replace(" and", ",")
        if fraction:
            words = f"{words} Rupees and {num2words(fraction, lang='en_IN')} Paise"
        else:
            words = f"{words} Rupees"
        return words.title()
    except Exception:
        # fallback
        return f"{amount:.2f} Rupees"

def compute_gst_summary(items, interstate=False):
    """
    items: list of dicts with keys: qty, rate, gst_percent, taxable_value, gst_amount
    interstate: bool - if interstate True, treat as IGST; else split CGST/SGST equally.
    Returns dict keyed by gst_percent -> {taxable, gst, cgst, sgst, igst}
    """
    summary = {}
    for it in items:
        g = Decimal(str(it.get("gst_percent") or 0)).quantize(Decimal("0.01"))
        key = str(g)  # use string key like "12.00"
        taxable = to_decimal(it.get("taxable_value") or 0)
        gst_amount = to_decimal(it.get("gst_amount") or 0)

        if key not in summary:
            summary[key] = {
                "gst_percent": g,
                "taxable_value": Decimal("0.00"),
                "gst_amount": Decimal("0.00"),
                "cgst": Decimal("0.00"),
                "sgst": Decimal("0.00"),
                "igst": Decimal("0.00"),
            }

        summary[key]["taxable_value"] += taxable
        summary[key]["gst_amount"] += gst_amount

    # Post-process split
    for k, v in summary.items():
        if interstate:
            v["igst"] = v["gst_amount"]
            v["cgst"] = v["sgst"] = Decimal("0.00")
        else:
            # split equally
            half = (v["gst_amount"] / 2).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            v["cgst"] = half
            v["sgst"] = half
            v["igst"] = Decimal("0.00")

    # Convert Decimal -> float for template friendliness
    for k, v in summary.items():
        for kk in ["taxable_value", "gst_amount", "cgst", "sgst", "igst"]:
            v[kk] = float(v[kk].quantize(Decimal("0.01")))
        v["gst_percent"] = float(v["gst_percent"])
    return summary


# ---- main route ----
@render_bp.route("/invoice/<int:invoice_id>", methods=["GET"])
def render_invoice(invoice_id):
    """
    Renders HTML invoice for invoice_id
    """
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        abort(404, "Invoice not found")

    # load related distributor (buyer)
    distributor = invoice.distributor  # relationship set in model
    # load supplier (your company). Many setups have a single supplier row; fallback to config-based seller info.
    supplier = None
    try:
        supplier = Supplier.query.first()
    except Exception:
        supplier = None

    # load invoice items
    items_q = InvoiceItem.query.filter_by(invoice_id=invoice.id).join(Product, isouter=True).all()
    items = []
    for it in items_q:
        # fields expected on InvoiceItem: id, invoice_id, product_id, description, qty, rate, gst_percent
        prod = None
        try:
            prod = Product.query.get(it.product_id) if it.product_id else None
        except Exception:
            prod = None

        qty = to_decimal(it.qty or 0)
        rate = to_decimal(it.rate or (getattr(prod, "rate", 0) if prod else 0))
        taxable_value = (qty * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        gst_percent = getattr(it, "gst_percent", None) or getattr(prod, "gst_percent", 0) or 0
        gst_amount = (taxable_value * Decimal(str(gst_percent)) / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        items.append({
            "id": it.id,
            "product_id": it.product_id,
            "sku": getattr(prod, "sku", "") if prod else "",
            "description": it.description or (getattr(prod, "name", "") if prod else ""),
            "qty": float(qty),
            "rate": float(rate),
            "taxable_value": float(taxable_value),
            "gst_percent": float(gst_percent),
            "gst_amount": float(gst_amount)
        })

    # determine intra/interstate supply for tax split
    # Simple heuristic: compare supplier state and distributor state_code (if available)
    supplier_state = None
    distributor_state = None
    try:
        if supplier:
            supplier_state = supplier.state or None
    except Exception:
        supplier_state = None
    try:
        distributor_state = getattr(distributor, "state", None) or getattr(distributor, "state_code", None)
    except Exception:
        distributor_state = None

    interstate = False
    if supplier_state and distributor_state:
        interstate = (supplier_state.strip().lower() != distributor_state.strip().lower())

    gst_summary = compute_gst_summary(items, interstate=interstate)

    # totals (recompute to be safe)
    total_taxable = sum([it["taxable_value"] for it in items])
    total_gst = sum([it["gst_amount"] for it in items])
    grand_total = to_decimal(total_taxable + total_gst)

    # seller / company info (fallback to app config)
    company = current_app.config.get("COMPANY", {
        "name": "Your Company Pvt Ltd",
        "address": "Address line 1\nCity - PIN",
        "gstin": "00AAAAA0000A0Z0",
        "phone": "",
        "email": "",
    })

    invoice_data = {
        "id": invoice.id,
        "invoice_number": invoice.invoice_number,
        "date": invoice.date.strftime("%d-%b-%Y") if getattr(invoice, "date", None) else datetime.utcnow().strftime("%d-%b-%Y"),
        "distributor": {
            "id": distributor.id if distributor else None,
            "name": distributor.name if distributor else "",
            "address": distributor.address if distributor else "",
            "gstin": getattr(distributor, "gstin", "") if distributor else "",
            "state": getattr(distributor, "state", "") if distributor else "",
            "state_code": getattr(distributor, "state_code", "") if distributor else ""
        },
        "supplier": {
            "name": company.get("name"),
            "address": company.get("address"),
            "gstin": company.get("gstin"),
            "phone": company.get("phone"),
            "email": company.get("email"),
        },
        "items": items,
        "totals": {
            "taxable_total": float(to_decimal(total_taxable)),
            "gst_total": float(to_decimal(total_gst)),
            "grand_total": float(grand_total)
        },
        "gst_summary": gst_summary,
        "amount_in_words": amount_in_words_rupees(float(grand_total))
    }

    return render_template("invoice_template.html", invoice=invoice_data)


# ---- PDF endpoint (optional; requires WeasyPrint) ----
@render_bp.route("/invoice/<int:invoice_id>/pdf", methods=["GET"])
def invoice_pdf(invoice_id):
    """
    Generates a PDF using WeasyPrint (recommended) or returns a helpful message if not installed.
    """
    # first render HTML via the same render route code (avoid double query duplication)
    resp = render_invoice(invoice_id)
    html = resp  # this is a rendered template string (Flask returns Response, but render_template returns Response when called inside doc)
    # If render_invoice returned a Response object, extract data
    if hasattr(html, "get_data"):
        html = html.get_data(as_text=True)

    try:
        from weasyprint import HTML, CSS
    except Exception:
        abort(500, "WeasyPrint is not installed. Install with: pip install weasyprint and required system deps.")

    html_obj = HTML(string=html, base_url=current_app.root_path)
    pdf = html_obj.write_pdf(stylesheets=None)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=invoice-{invoice_id}.pdf'
    return response
