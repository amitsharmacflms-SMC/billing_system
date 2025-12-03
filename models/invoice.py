from core.database import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Invoice(db.Model):
    __tablename__ = "invoices"
    id = db.Column(db.Integer, primary_key=True)
    invoice_no = db.Column(db.String(100), unique=True, nullable=False, index=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("distributors.id"), nullable=False)
    shipto_id = db.Column(db.Integer, db.ForeignKey("distributors.id"), nullable=True)
    transport = db.Column(db.String(200))
    vehicle_no = db.Column(db.String(100))
    place_of_supply = db.Column(db.String(100))
    total_pcs = db.Column(db.Integer, default=0)
    total_cs = db.Column(db.Integer, default=0)
    taxable_value = db.Column(db.Numeric(14,2), default=0.00)
    total_gst = db.Column(db.Numeric(12,2), default=0.00)
    grand_total = db.Column(db.Numeric(14,2), default=0.00)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship("InvoiceItem", backref="invoice", cascade="all, delete-orphan")

    # convenience link
    supplier = db.relationship("Supplier", foreign_keys=[supplier_id])
    buyer = db.relationship("Distributor", foreign_keys=[buyer_id])
    shipto = db.relationship("Distributor", foreign_keys=[shipto_id])
