from flask import Flask, render_template
from core.database import db, migrate
from config import Config
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    # ------------------------------
    # INIT JWT  (REQUIRED)
    # ------------------------------
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
    from routes.stock_routes import stock_bp
    from routes.user_routes import user_bp
    from routes.supplier_mapping_routes import map_bp

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
    app.register_blueprint(stock_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(map_bp)

    # ------------------------------
    # HTML Routes
    # ------------------------------
    @app.route("/")
    def login_page():
        return render_template("login.html")

    @app.route("/menu")
    def menu_page():
        return render_template("menu.html")

    @app.route("/test-login")
    def test_login_page():
        return render_template("test_login.html")

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
