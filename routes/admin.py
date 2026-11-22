from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from functools import wraps
from models.booking import Booking
from models.payment import Payment

admin_bp = Blueprint("admin", __name__)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.login"))
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username","")
        password = request.form.get("password","")
        configured_user = current_app.config.get("ADMIN_USERNAME")
        configured_password = current_app.config.get("ADMIN_PASSWORD")
        if configured_password and user == configured_user and password == configured_password:
            session.clear()
            session["admin_logged_in"] = True
            return redirect(url_for("admin.dashboard"))
        flash("Login failed.", "error")
    return render_template("admin/login.html")

@admin_bp.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin.login"))

@admin_bp.get("/")
@admin_required
def dashboard():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    return render_template("admin/dashboard.html", bookings=bookings, payments=payments)

@admin_bp.post("/booking/<int:booking_id>/status")
@admin_required
def update_status(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    status = request.form.get("status")
    if status in {"Pending", "Confirmed", "Cancelled"}:
        booking.status = status
        from models import db
        db.session.commit()
    return redirect(url_for("admin.dashboard"))
