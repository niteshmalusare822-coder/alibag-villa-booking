from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db
from models.booking import Booking
from models.payment import Payment

payment_bp = Blueprint("payment", __name__)

@payment_bp.route("/<int:booking_id>", methods=["GET", "POST"])
def submit_payment(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            if amount <= 0: raise ValueError()
        except (ValueError, KeyError):
            flash("Enter a valid amount.", "error")
            return render_template("payment.html", booking=booking)
        payment = Payment(booking_id=booking.id, amount=amount, utr=request.form.get("utr","").strip())
        db.session.add(payment)
        db.session.commit()
        flash("Payment details submitted. Admin will verify the payment.", "success")
        return redirect(url_for("booking.confirmation", booking_id=booking.id))
    return render_template("payment.html", booking=booking)
