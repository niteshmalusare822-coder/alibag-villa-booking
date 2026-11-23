import os
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)

# ✅ Bad Request एरर येऊ नये म्हणून CSRF बंद केले
app.config['WTF_CSRF_ENABLED'] = False 

db = SQLAlchemy(app)

# ================= GUEST SECTION =================
CONTACTS = [
    {"name": "Rupesh", "phone": "+919167870303"},
    {"name": "Shivali", "phone": "+919082462036"},
    {"name": "Savli", "phone": "+918454037731"}
]

VILLA_INFO = {
    "name": "Spring Field Villa",
    "tagline": "Escape the City... Feel the Vacation Vibes!",
    "address": "Gut No. 214, Plot No. 854, Chondhi, Alibaug, Maharashtra 402208",
    "hero_image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200&q=80",
    "highlights": ["Spacious & Beautiful Villa", "Private Swimming Pool", "Lush Green Lawn", "Relaxing Sit-out Area", "Perfect for Family & Friends", "Peaceful & Serene Location"],
    "nearby": [
        {"place": "Mandwa Jetty", "dist": "12 km", "time": "25-30 Min"},
        {"place": "Fish Market (Chondhi)", "dist": "0.5 km", "time": "2 Min"},
        {"place": "Alibaug City", "dist": "9 km", "time": "20 Min"},
        {"place": "Kihim Beach", "dist": "2.2 km", "time": "5-7 Min"},
        {"place": "Baigarh Beach", "dist": "5.5 km", "time": "12-15 Min"}
    ],
    "route": {"distance": "100 - 115 km", "time": "2.5 - 3.5 Hours", "path": "Mumbai -> Atal Setu -> Chirle -> Pen -> Chondhi -> Villa"},
    "contacts": CONTACTS
}

class BookingEnquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=True)
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
        try:
            new_enquiry = BookingEnquiry(
                name=request.form.get('name', ''),
                phone=request.form.get('phone', ''),
                email=request.form.get('email', ''),
                check_in=request.form.get('check_in', ''),
                check_out=request.form.get('check_out', ''),
                guests=int(request.form.get('guests', 1))
            )
            db.session.add(new_enquiry)
            db.session.commit()
            flash('तुमची बुकिंग विनंती यशस्वीरित्या नोंदवली गेली आहे!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('बुकिंग नोंदवताना त्रुटी आली. कृपया सर्व फील्ड्स भरा.', 'error')
            return redirect(url_for('booking'))
    return render_template('booking.html', villa=VILLA_INFO)

# ================= ADMIN SECTION =================
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == app.config['ADMIN_USERNAME'] and request.form['password'] == app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash('चुकीचे Username किंवा Password!', 'error')
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    bookings = BookingEnquiry.query.order_by(BookingEnquiry.id.desc()).all()
    return render_template('admin/dashboard.html', bookings=bookings)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
