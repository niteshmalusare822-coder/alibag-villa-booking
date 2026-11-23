import os
from dotenv import load_dotenv

load_dotenv()
PRODUCTION = os.getenv("PRODUCTION") == "1"

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or ("" if PRODUCTION else "dev-only-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///villa.db"
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = PRODUCTION
    
    # ✅ येथे Admin Username आणि Password सेट केला आहे
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")  # ✅ रिकाम्या ऐवजी "admin123" ठेवला
    
    VILLA_NAME = "Springfield Villa"
    VILLA_LOCATION = os.getenv("VILLA_LOCATION", "Alibag")
    VILLA_PHONE = os.getenv("VILLA_PHONE", "")
    UPI_ID = os.getenv("UPI_ID", "")
    
    CONTACTS = [
        {"name": os.getenv("CONTACT_1_NAME", "Rupesh"), "phone": os.getenv("CONTACT_1_PHONE", "919167870303")},
        {"name": os.getenv("CONTACT_2_NAME", "Shivali"), "phone": os.getenv("CONTACT_2_PHONE", "919082462036")},
        {"name": os.getenv("CONTACT_3_NAME", "Savli"), "phone": os.getenv("CONTACT_3_PHONE", "918454037731")},
    ]
