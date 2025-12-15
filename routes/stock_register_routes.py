from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from core.database import db
from models.stock import StockEntry
from models.invoice_items import InvoiceItem
from datetime import date
from openpyxl import Workbook
from flask import send_file
import io



stock_register_bp = Blueprint(
    "stock_register",
    __name__,
    url_prefix="/stock-register"
)


@stock_register_bp.route("/yearly-export", methods=["GET"])
@jwt_required()
def yearly_stock_register_export():
    product_id = request.args.get("product_id")
    year = request.args.get("year")

    if not product_id or not year:
        return {"error": "product_id and year required"}, 400

    product_id = int(product_id)
    year = int(year)

    # --------------------------------
    # Opening stock before Jan 1
    # --------------------------------
    year_start = date(year, 1, 1)

    opening_received = db.session.query(
        db.func.coalesce(db.func.sum(StockEntry.received_cs), 0)
    ).filter(
        StockEntry.product_id == product_id,
        StockEntry.received_date < year_start
    ).scalar()

    opening_sold = db.session.query(
        db.func.coalesce(db.func.sum(InvoiceItem.cs), 0)
    ).filter(
        InvoiceItem.product_id == product_id,
        InvoiceItem.created_at < year_start
    ).scalar()

    running_balance = float(opening_received) - float(opening_sold)

    # --------------------------------
    # Create Excel Workbook
    # --------------------------------
    wb = Workbook()
    ws = wb.active
    ws.title = "Stock Register"

    # Header
    ws.append([
        "Month",
        "Opening Qty (CS)",
        "Received Qty (CS)",
        "Out Qty (CS)",
        "Balance Qty (CS)"
    ])

    # Data rows
    for month in range(1, 13):

        received = db.session.query(
            db.func.coalesce(db.func.sum(StockEntry.received_cs), 0)
        ).filter(
            StockEntry.product_id == product_id,
            db.extract("year", StockEntry.received_date) == year,
            db.extract("month", StockEntry.received_date) == month
        ).scalar()

        sold = db.session.query(
            db.func.coalesce(db.func.sum(InvoiceItem.cs), 0)
        ).filter(
            InvoiceItem.product_id == product_id,
            db.extract("year", InvoiceItem.created_at) == year,
            db.extract("month", InvoiceItem.created_at) == month
        ).scalar()

        received = float(received)
        sold = float(sold)

        closing = running_balance + received - sold

        ws.append([
            f"{year}-{month:02d}",
            round(running_balance, 2),
            round(received, 2),
            round(sold, 2),
            round(closing, 2)
        ])

        running_balance = closing

    # --------------------------------
    # Send file
    # --------------------------------
    file_stream = io.BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    return send_file(
        file_stream,
        as_attachment=True,
        download_name=f"Stock_Register_{year}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
