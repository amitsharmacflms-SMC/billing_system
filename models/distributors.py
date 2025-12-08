from core.database import db
from datetime import datetime

class Distributor(db.Model):
    __tablename__ = "distributors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    gstin = db.Column(db.String(50))
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=True)

    supplier = db.relationship("Supplier", backref="distributors", foreign_keys=[supplier_id])
