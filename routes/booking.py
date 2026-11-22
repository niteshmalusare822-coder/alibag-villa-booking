from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from models import db
from models.booking import Booking

booking_bp = Blueprint("booking", __name__)

@booking_bp.route("/", methods=["GET", "POST"])
def create_booking():
    if request.method == "POST":
        try:
            check_in = datetime.strptime(request.form["check_in"], "%Y-%m-%d").date()
            check_out = datetime.strptime(request.form["check_out"], "%Y-%m-%d").date()
            guests = int(request.form.get("guests", "1"))
            if check_out <= check_in or guests < 1 or guests > 30:
                raise ValueError("Invalid date range or guest count")
        except (ValueError, KeyError):
            flash("Please enter valid dates and guest count.", "error")
            return render_template("booking.html")
        booking = Booking(
            full_name=request.form["full_name"].strip(),
            phone=request.form["phone"].strip(),
            email=request.form.get("email", "").strip(),
            check_in=check_in, check_out=check_out, guests=guests,
            notes=request.form.get("notes", "").strip()
        )
        db.session.add(booking)
        db.session.commit()
        return redirect(url_for("booking.confirmation", booking_id=booking.id))
    return render_template("booking.html")

@booking_bp.get("/confirmation/<int:booking_id>")
def confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template("confirmation.html", booking=booking)
