from core.database import db
from datetime import datetime

class Invoice(db.Model):
    __tablename__ = "invoice"

    id = db.Column(db.Integer, primary_key=True)
    invoice_no = db.Column(db.String(50))
    invoice_date = db.Column(db.Date)

    super_stockist_id = db.Column(db.Integer, db.ForeignKey("super_stockist.id"))
    distributor_id = db.Column(db.Integer, db.ForeignKey("distributor.id"))

    pcs_total = db.Column(db.Integer)
    cs_total = db.Column(db.Integer)
    taxable = db.Column(db.Numeric(14,2))
    cgst = db.Column(db.Numeric(14,2))
    sgst = db.Column(db.Numeric(14,2))
    grand_total = db.Column(db.Numeric(14,2))

    irn = db.Column(db.Text)
    ack_no = db.Column(db.Text)
    ack_date = db.Column(db.DateTime)
    signed_json = db.Column(db.JSON)
    signed_qr = db.Column(db.Text)
    eway_no = db.Column(db.Text)
    eway_valid_from = db.Column(db.DateTime)
    eway_valid_to = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class InvoiceItem(db.Model):
    __tablename__ = "invoice_item"

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoice.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))

    qty_pcs = db.Column(db.Integer)
    qty_cs = db.Column(db.Integer)
    rate = db.Column(db.Numeric(12,2))
    discount = db.Column(db.Numeric(5,2))
    taxable = db.Column(db.Numeric(12,2))
    gst_percent = db.Column(db.Numeric(5,2))
    total = db.Column(db.Numeric(12,2))
