from . import db
from datetime import datetime

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    utr = db.Column(db.String(100))
    screenshot_url = db.Column(db.String(500))
    status = db.Column(db.String(30), default="Pending verification")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
