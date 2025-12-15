from core.database import db
from datetime import datetime

class StockEntry(db.Model):
    __tablename__ = "stock_entries"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False,
        index=True
    )

    received_cs = db.Column(db.Float, nullable=False)

    bill_no = db.Column(db.String(50))
    bill_date = db.Column(db.Date)

    # 🔥 THIS WAS MISSING / WRONG
    received_date = db.Column(db.Date, nullable=False)

    remarks = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship("Product", backref="stock_entries")
