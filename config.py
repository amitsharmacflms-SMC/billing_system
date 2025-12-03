import os

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "supersecret")
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
