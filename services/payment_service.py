"""Manual UPI verification starter. Never mark payment verified based on screenshot alone.""" 
def verify_payment_manually(payment, verified_by):
    payment.status = "Verified"
    payment.verified_by = verified_by
