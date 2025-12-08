from flask import Flask, render_template
from core.database import db, migrate
from config import Config

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    from flask_jwt_extended import JWTManager
    jwt = JWTManager(app)


    # ------------------------------
    # Initialize DB + Migrations
    # ------------------------------
    db.init_app(app)
    migrate.init_app(app, db)

    # ------------------------------
    # Import Blueprints
    # ------------------------------
    from routes.auth_routes import auth_bp
    from routes.invoice_routes import invoice_bp
    from routes.product_routes import product_bp
    from routes.distributor_routes import distributor_bp
    from routes.einvoice_routes import einv_bp
    from routes.ewaybill_routes import eway_bp
    from routes.supplier_routes import supplier_bp
    from routes.render_invoice import render_bp
    from routes.stock_routes import stock_bp
    # ------------------------------
    # Register Blueprints
    # ------------------------------
    app.register_blueprint(auth_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(distributor_bp)
    app.register_blueprint(einv_bp)
    app.register_blueprint(eway_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(render_bp)
    app.register_blueprint(stock_bp)



    # ------------------------------
    # ROOT ROUTE
    # ------------------------------
    @app.route("/")
    def login_page():
    return render_template("login.html")


    @app.route("/test-login")
    def test_login_page():
    return render_template("test_login.html")


    # ------------------------------
    # MENU ROUTE
    # ------------------------------




    @app.route("/menu")
    def menu():
        return render_template("menu.html")

    @app.route("/received-stock")
    def received_stock():
        return render_template("received_stock.html")

    @app.route("/create-invoice")
    def create_invoice_page():
        return render_template("create_invoice.html")

    @app.route("/search-invoice")
    def search_invoice():
        return render_template("search_invoice.html")

    @app.route("/reports")
    def reports():
        return render_template("reports.html")

    @app.route("/product-update")
    def product_update():
        return render_template("product_update.html")

    @app.route("/suppliers-update")
    def suppliers_update():
        return render_template("suppliers_update.html")

    @app.route("/distributors-update")
    def distributors_update():
        return render_template("distributors_update.html")



    # ------------------------------
    # Health Check
    # ------------------------------
    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app


# --------------------------------------------------
# Create App Instance
# --------------------------------------------------
app = create_app()


# --------------------------------------------------
# REQUIRED FOR RAILWAY DEPLOYMENT
# --------------------------------------------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
