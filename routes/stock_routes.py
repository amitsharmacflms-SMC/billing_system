@stock_bp.route("/stock-summary", methods=["GET"])
@jwt_required()
def stock_summary():

    rows = []

    products = Product.query.order_by(Product.name).all()

    for p in products:

        opening_qty = 0   # LOCKED AS PER REQUIREMENT

        received_qty = db.session.query(
            func.coalesce(func.sum(StockEntry.received_cs), 0)
        ).filter(
            StockEntry.product_id == p.id
        ).scalar()

        out_qty = db.session.query(
            func.coalesce(func.sum(InvoiceItem.cs), 0)
        ).filter(
            InvoiceItem.product_id == p.id
        ).scalar()

        balance_qty = opening_qty + received_qty - out_qty

        rows.append({
            "product": p.name,
            "opening_qty": float(opening_qty),
            "received_qty": float(received_qty),
            "out_qty": float(out_qty),
            "balance_qty": float(balance_qty)
        })

    return jsonify(rows)
