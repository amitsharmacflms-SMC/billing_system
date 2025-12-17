from flask import Flask, render_template
from core.database import db, migrate
from config import Config
from flask_jwt_extended import JWTManager
from flask import jsonify

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    # ------------------------------
    # INIT JWT
    # ------------------------------
    jwt = JWTManager(app)

    # ------------------------------
    # DB + MIGRATIONS
    # ------------------------------
    db.init_app(app)
    migrate.init_app(app, db)

    # ------------------------------
    # IMPORT BLUEPRINTS
    # ------------------------------
    from routes.auth_routes import auth_bp
    from routes.invoice_routes import invoice_bp
    from routes.product_routes import product_bp
    from routes.distributor_routes import distributor_bp
    from routes.einvoice_routes import einv_bp
    from routes.ewaybill_routes import eway_bp
    from routes.supplier_routes import supplier_bp
    from routes.stock_routes import stock_bp
    from routes.user_routes import user_bp
    from routes.supplier_mapping_routes import map_bp
    from routes.render_invoice import render_invoice_bp


    # ------------------------------
    # REGISTER BLUEPRINTS
    # ------------------------------
    app.register_blueprint(auth_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(distributor_bp)
    app.register_blueprint(einv_bp)
    app.register_blueprint(eway_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(map_bp)
    app.register_blueprint(render_invoice_bp)


    # ------------------------------
    # FRONT-END ROUTES (HTML PAGES)
    # ------------------------------
    @app.route("/")
    def login_page():
        return render_template("login.html")

    @app.route("/menu")
    def menu_page():
        return render_template("menu.html")

    # RECEIVED STOCK
    @app.route("/received-stock")
    def received_stock_page():
        return render_template("received_stock.html")

    # STOCK REGISTER
    @app.route("/stock-register-page")
    def stock_register_page():
        return render_template("stock_register.html")

    # CREATE INVOICE PAGE
    @app.route("/invoice/create")
    def invoice_create_page():
        return render_template("create_invoice.html")


    # SEARCH INVOICE PAGE
    @app.route("/invoice/search")
    def invoice_search_page():
        return render_template("invoice_search.html")

    # REPORTS PAGE
    @app.route("/reports")
    def reports_page():
        return render_template("reports.html")

    @reports_bp.route("/gst-summary")
    def gst_summary():
    rows = db.session.execute("""
        SELECT DATE_TRUNC('month', date) AS month,
               SUM(total_amount) taxable,
               SUM(total_tax) gst
        FROM invoices
        GROUP BY month
        ORDER BY month
    """)
        return jsonify([dict(r) for r in rows])

    @app.route("/reports/gst-summary")
    def gst_summary():
    rows = db.session.execute("""
        SELECT DATE_TRUNC('month', date) AS month,
               SUM(total_amount) AS taxable,
               SUM(total_tax) AS gst
        FROM invoices
        GROUP BY month
        ORDER BY month
    """).fetchall()

        return jsonify([
        {
            "month": str(r.month),
            "taxable": float(r.taxable),
            "gst": float(r.gst)
        }
        for r in rows
    ])






    # USER MANAGEMENT
    @app.route("/users/manage")
    def users_manage_page():
        return render_template("user_management.html")

    # PRODUCT MANAGEMENT
    @app.route("/products/manage")
    def products_manage_page():
        return render_template("product_update.html")

    # SUPPLIER MANAGEMENT
    @app.route("/suppliers/manage")
    def suppliers_manage_page():
        return render_template("suppliers_update.html")

    # DISTRIBUTOR MANAGEMENT
    @app.route("/distributors/manage")
    def distributors_manage_page():
        return render_template("distributors_update.html")

    print(app.url_map)

    return app


# --------------------------------------------------
# CREATE APP INSTANCE
# --------------------------------------------------
app = create_app()

# --------------------------------------------------
# RAILWAY DEPLOYMENT SERVER
# --------------------------------------------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
