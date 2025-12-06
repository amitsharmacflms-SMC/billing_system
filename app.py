from flask import Flask, render_template
from core.database import db, migrate
from config import Config

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # import routes
    from routes.auth_routes import auth_bp
    from routes.invoice_routes import invoice_bp
    from routes.product_routes import product_bp
    from routes.distributor_routes import distributor_bp
    from routes.einvoice_routes import einv_bp
    from routes.ewaybill_routes import eway_bp
    from routes.supplier_routes import supplier_bp   # <-- NEW

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(distributor_bp)
    app.register_blueprint(einv_bp)
    app.register_blueprint(eway_bp)
    app.register_blueprint(supplier_bp)              # <-- NEW

    return app

app = create_app()


# ---------------------------------------
# 🚀 REQUIRED FOR RAILWAY DEPLOYMENT
# ---------------------------------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
