from core.database import db
from datetime import datetime

class InvoiceItem(db.Model):
    __tablename__ = "invoice_items"
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    hsn = db.Column(db.String(50))
    pcs = db.Column(db.Integer, default=0)
    cs = db.Column(db.Integer, default=0)
    rate = db.Column(db.Numeric(12,2))
    disc_percent = db.Column(db.Numeric(5,2), default=0.00)
    taxable = db.Column(db.Numeric(14,2), default=0.00)
    gst_percent = db.Column(db.Numeric(5,2), default=0.00)
    gst_amount = db.Column(db.Numeric(12,2), default=0.00)
    total = db.Column(db.Numeric(14,2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship("Product", foreign_keys=[product_id])
