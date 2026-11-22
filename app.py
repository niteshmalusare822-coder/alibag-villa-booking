import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# 📞 3 संपर्क व्यक्ती (Render Environment Variables मधून येतील)
CONTACTS = [
    {"name": "Rupesh", "phone": "+919167870303"},
    {"name": "Shivali", "phone": "+919082462036"},
    {"name": "Savli", "phone": "+918454037731"}
]

VILLA_INFO = {
    "name": "Springfield Villa",
    "tagline": "अलिबागच्या समुद्रकाठची तुमची स्वतःची शांत निवारा 🌊",
    "hero_image": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=1200&q=80",
    "price_per_night": 3000,
    "bedrooms": 3,
    "bathrooms": 3,
    "max_guests": 8,
    "amenities": ["Private Pool", "Sea View", "Free Wi-Fi", "Fully Equipped Kitchen", "AC Rooms", "Free Parking"],
    "contacts": CONTACTS
}

# Simple Booking Database Model
class BookingEnquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    check_in = db.Column(db.String(20), nullable=False)
    check_out = db.Column(db.String(20), nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Pending')

@app.route('/')
def index():
    return render_template('index.html', villa=VILLA_INFO)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        new_enquiry = BookingEnquiry(
            name=request.form['name'],
            phone=request.form['phone'],
            check_in=request.form['check_in'],
            check_out=request.form['check_out'],
            guests=request.form['guests']
        )
        db.session.add(new_enquiry)
        db.session.commit()
        flash('तुमची विनंती यशस्वीरित्या नोंदवली गेली आहे! आम्ही लवकरच संपर्क करू.', 'success')
        return redirect(url_for('index'))
    
    return render_template('booking.html', villa=VILLA_INFO)

# डेटाबेस टेबल ऑटोमॅटिक तयार करण्यासाठी
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
