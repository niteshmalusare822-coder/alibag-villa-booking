import os
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
app.config['WTF_CSRF_ENABLED'] = False
db = SQLAlchemy(app)

# ================= BUSINESS CONFIG =================
PRICE_PER_PERSON = 3000          # ₹3000 / person / day (meals included)
ROOM_CAPACITY = 8                # 1 room = max 8 persons
TOTAL_ROOMS = 6                  # 6 rooms total

MEAL_PLAN = [
    {"time": "08:00 AM", "meal": "Morning Tea + Nashta", "icon": "☕"},
    {"time": "01:00 PM", "meal": "Lunch (Thali)", "icon": "🍛"},
    {"time": "05:00 PM", "meal": "Evening Tea + Snacks", "icon": "🫖"},
    {"time": "08:30 PM", "meal": "Dinner", "icon": "🍲"},
    {"time": "07:30 AM", "meal": "Check-out Morning Nashta", "icon": "🥞"},
]

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
    "total_rooms": TOTAL_ROOMS,
    "room_capacity": ROOM_CAPACITY,
    "price_per_person": PRICE_PER_PERSON,
    "check_in_time": "12:00 PM",
    "check_out_time": "11:00 AM",
    "meal_plan": MEAL_PLAN,
    "highlights": ["Spacious & Beautiful Villa", "Private Swimming Pool", "Lush Green Lawn",
                   "Relaxing Sit-out Area", "Perfect for Family & Friends", "Peaceful & Serene Location"],
    "nearby": [
        {"place": "Mandwa Jetty", "dist": "12 km", "time": "25-30 Min"},
        {"place": "Fish Market (Chondhi)", "dist": "0.5 km", "time": "2 Min"},
        {"place": "Alibaug City", "dist": "9 km", "time": "20 Min"},
        {"place": "Kihim Beach", "dist": "2.2 km", "time": "5-7 Min"},
        {"place": "Baigarh Beach", "dist": "5.5 km", "time": "12-15 Min"}
    ],
    "route": {"distance": "100 - 115 km", "time": "2.5 - 3.5 Hours",
              "path": "Mumbai -> Atal Setu -> Chirle -> Pen -> Chondhi -> Villa"},
    "contacts": CONTACTS
}

# ================= DATABASE MODELS =================
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, default=ROOM_CAPACITY)
    is_active = db.Column(db.Boolean, default=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    check_in = db.Column(db.String(20), nullable=False)
    check_out = db.Column(db.String(20), nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    nights = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Seed 6 rooms on first run
def seed_rooms():
    if Room.query.count() == 0:
        for i in range(1, TOTAL_ROOMS + 1):
            db.session.add(Room(name=f"Room {i}", capacity=ROOM_CAPACITY, is_active=True))
        db.session.commit()

# ================= AVAILABILITY LOGIC =================
def get_booked_rooms_for_date(d):
    """Return set of room_ids booked on date d"""
    d_str = d.isoformat() if isinstance(d, date) else d
    booked = set()
    for b in Booking.query.filter(Booking.status != 'Cancelled').all():
        try:
            ci = date.fromisoformat(b.check_in)
            co = date.fromisoformat(b.check_out)
            if ci <= date.fromisoformat(d_str) < co:
                booked.add(b.room_id)
        except Exception:
            pass
    return booked

def get_available_rooms_on_date(d):
    booked = get_booked_rooms_for_date(d)
    all_rooms = Room.query.filter_by(is_active=True).all()
    return [r for r in all_rooms if r.id not in booked]

def get_nights(ci_str, co_str):
    try:
        ci = date.fromisoformat(ci_str)
        co = date.fromisoformat(co_str)
        return max((co - ci).days, 0)
    except Exception:
        return 0

# ================= PUBLIC ROUTES =================
@app.route('/')
def index():
    today = date.today()
    # 14-day availability preview
    preview = []
    for i in range(14):
        d = today + timedelta(days=i)
        avail = len(get_available_rooms_on_date(d))
        preview.append({"date": d.isoformat(), "label": d.strftime("%d %b"), "available": avail})
    return render_template('index.html', villa=VILLA_INFO, preview=preview)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        ci = request.form.get('check_in', '')
        co = request.form.get('check_out', '')
        guests = int(request.form.get('guests', 1))
        nights = get_nights(ci, co)

        if nights <= 0:
            flash('Check-out date check-in पेक्षा मोठी असणे आवश्यक आहे.', 'error')
            return redirect(url_for('booking'))

        # Find a room that can accommodate guests for ALL nights
        chosen_room = None
        d = date.fromisoformat(ci)
        while d < date.fromisoformat(co):
            avail = get_available_rooms_on_date(d)
            avail = [r for r in avail if r.capacity >= guests]
            if not avail:
                break
            if chosen_room is None:
                chosen_room = avail[0]
            else:
                chosen_room = next((r for r in avail if r.id == chosen_room.id), None)
            d += timedelta(days=1)

        if chosen_room is None:
            flash(f'😔 Sorry! {guests} लोकांसाठी {ci} ते {co} पर्यंत कोणतीही room available नाही.', 'error')
            return redirect(url_for('booking'))

        total = guests * PRICE_PER_PERSON * nights
        new_b = Booking(
            room_id=chosen_room.id, name=request.form.get('name', ''),
            phone=request.form.get('phone', ''), email=request.form.get('email', ''),
            check_in=ci, check_out=co, guests=guests, nights=nights, total_price=total
        )
        db.session.add(new_b)
        db.session.commit()
        flash(f'✅ Booking #{new_b.id} confirmed! Room: {chosen_room.name} | Total: ₹{total:,}', 'success')
        return redirect(url_for('index'))

    # GET: show availability calendar
    today = date.today()
    cal = []
    for i in range(30):
        d = today + timedelta(days=i)
        avail = len(get_available_rooms_on_date(d))
        cal.append({"date": d.isoformat(), "label": d.strftime("%d %b"),
                    "available": avail, "status": "free" if avail > 0 else "full"})
    return render_template('booking.html', villa=VILLA_INFO, calendar=cal)

# API for live availability check
@app.route('/api/availability')
def api_availability():
    ci = request.args.get('check_in')
    co = request.args.get('check_out')
    guests = int(request.args.get('guests', 1))
    if not ci or not co:
        return jsonify({"error": "dates required"}), 400
    nights = get_nights(ci, co)
    total = guests * PRICE_PER_PERSON * nights
    return jsonify({
        "nights": nights, "guests": guests,
        "total_price": total, "per_person_per_day": PRICE_PER_PERSON,
        "available_rooms": [r.name for r in get_available_rooms_on_date(date.fromisoformat(ci))]
    })

# ================= ADMIN ROUTES =================
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
    bookings = Booking.query.order_by(Booking.id.desc()).all()
    rooms = Room.query.all()
    today = date.today()

    # Room-wise status
    room_status = []
    for r in rooms:
        booked_today = any(b.room_id == r.id and b.status != 'Cancelled'
                           and date.fromisoformat(b.check_in) <= today < date.fromisoformat(b.check_out)
                           for b in bookings)
        room_status.append({"room": r, "booked_today": booked_today})

    # 30-day calendar
    calendar = []
    for i in range(30):
        d = today + timedelta(days=i)
        avail = len(get_available_rooms_on_date(d))
        calendar.append({"date": d.isoformat(), "label": d.strftime("%d %b"),
                         "available": avail, "booked": TOTAL_ROOMS - avail})

    total_revenue = sum(b.total_price for b in bookings if b.status == 'Confirmed')
    pending = sum(1 for b in bookings if b.status == 'Pending')

    return render_template('admin/dashboard.html',
                           bookings=bookings, room_status=room_status,
                           calendar=calendar, villa=VILLA_INFO,
                           total_revenue=total_revenue, pending=pending,
                           total_bookings=len(bookings))

@app.route('/admin/booking/<int:bid>/status', methods=['POST'])
@admin_required
def update_status(bid):
    b = Booking.query.get_or_404(bid)
    s = request.form.get('status', 'Pending')
    if s in ('Pending', 'Confirmed', 'Cancelled'):
        b.status = s
        db.session.commit()
        flash(f'Booking #{bid} → {s}', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/rooms')
@admin_required
def admin_rooms():
    rooms = Room.query.all()
    return render_template('admin/rooms.html', rooms=rooms, villa=VILLA_INFO)

@app.route('/admin/room/<int:rid>/toggle', methods=['POST'])
@admin_required
def toggle_room(rid):
    r = Room.query.get_or_404(rid)
    r.is_active = not r.is_active
    db.session.commit()
    return redirect(url_for('admin_rooms'))

# ================= INIT =================
with app.app_context():
    db.create_all()
    seed_rooms()

if __name__ == "__main__":
    app.run(debug=True)
