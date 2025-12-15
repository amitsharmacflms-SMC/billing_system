from core.database import db

class StockEntry(db.Model):
    __tablename__ = "stock_entries"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    received_cs = db.Column(db.Float, nullable=False)

    bill_no = db.Column(db.String(50))
    bill_date = db.Column(db.Date)

    received_date = db.Column(db.Date, nullable=False)  # ✅ CORRECT
    remarks = db.Column(db.String(200))

    created_at = db.Column(db.DateTime)

    product = db.relationship("Product", backref="stock_entries")
