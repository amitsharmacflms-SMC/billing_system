from core.database import db
from datetime import datetime

class StockEntry(db.Model):
    __tablename__ = "stock_entries"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    received_cs = db.Column(db.Float, nullable=False)
    invoice_no = db.Column(db.String(50))
    remarks = db.Column(db.String(200))

    product = db.relationship("Product", backref="stock_entries")
