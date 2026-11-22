from flask import Flask
from config import Config
from models import db
from routes.website import website_bp
from routes.booking import booking_bp
from routes.payment import payment_bp
from routes.admin import admin_bp
from routes.gallery import gallery_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(website_bp)
    app.register_blueprint(booking_bp, url_prefix="/booking")
    app.register_blueprint(payment_bp, url_prefix="/payment")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(gallery_bp, url_prefix="/gallery")

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
