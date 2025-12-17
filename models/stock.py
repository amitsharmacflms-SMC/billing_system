from core.database import db
from datetime import date

class StockEntry(db.Model):
    __tablename__ = "stock_entries"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False, index=True)

    bill_no = db.Column(db.String(100), nullable=False)
    bill_date = db.Column(db.Date, nullable=False)
    received_date = db.Column(db.Date, nullable=False)

    received_cs = db.Column(db.Float, nullable=False)
    remarks = db.Column(db.String(255))
