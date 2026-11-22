import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-this")
    db_url = os.getenv("DATABASE_URL", "sqlite:///villa.db")
    SQLALCHEMY_DATABASE_URI = db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "P@ssw0rd")
