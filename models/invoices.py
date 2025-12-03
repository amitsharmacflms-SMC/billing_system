from core.database import db
from datetime import datetime


class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)

    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)

    distributor_id = db.Column(db.Integer, db.ForeignKey("distributors.id"), nullable=False)
    distributor = db.relationship("Distributor", backref="invoices")

    total_amount = db.Column(db.Float, default=0.0)
    total_tax = db.Column(db.Float, default=0.0)
    grand_total = db.Column(db.Float, default=0.0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
