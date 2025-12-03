import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    # ----------------------------------------------------------------------
    # Flask Settings
    # ----------------------------------------------------------------------
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_key")

    # ----------------------------------------------------------------------
    # SQLAlchemy (PostgreSQL via psycopg3)
    # ----------------------------------------------------------------------
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # ----------------------------------------------------------------------
    # NIC E-Invoice API
    # ----------------------------------------------------------------------
    EINV_CLIENT_ID = os.getenv("EINV_CLIENT_ID")
    EINV_CLIENT_SECRET = os.getenv("EINV_CLIENT_SECRET")
    EINV_GSTIN = os.getenv("EINV_GSTIN")
    EINV_BASE_URL = os.getenv("EINV_BASE_URL")

    # ----------------------------------------------------------------------
    # NIC E-Waybill API
    # ----------------------------------------------------------------------
    EWAY_CLIENT_ID = os.getenv("EWAY_CLIENT_ID")
    EWAY_CLIENT_SECRET = os.getenv("EWAY_CLIENT_SECRET")
    EWAY_GSTIN = os.getenv("EWAY_GSTIN")
    EWAY_BASE_URL = os.getenv("EWAY_BASE_URL")

    # ----------------------------------------------------------------------
    # CORS (Optional: Enable if frontend hosted separately)
    # ----------------------------------------------------------------------
    CORS_ORIGINS = "*"
