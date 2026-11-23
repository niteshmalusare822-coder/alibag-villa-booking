from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import db, Room


def seed_rooms():
    if Room.query.count():
        return
    for i in range(1, 6):
        db.session.add(Room(name=f"Room {i}", capacity=2, price=3000, description="AC room for a couple"))
    db.session.add(Room(name="Room 6", capacity=8, price=6000, description="Large AC room for a group, up to 8 guests"))
    db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    if not app.config["SECRET_KEY"]:
        raise RuntimeError("SECRET_KEY must be set when PRODUCTION=1")
    CSRFProtect(app)
    db.init_app(app)

    from routes.guest import guest_bp
    from routes.admin import admin_bp
    app.register_blueprint(guest_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.context_processor
    def villa():
        c = app.config
        return {"villa_name": c["VILLA_NAME"], "villa_location": c["VILLA_LOCATION"], "villa_phone": c["VILLA_PHONE"], "contacts": c["CONTACTS"]}

    with app.app_context():
        db.create_all()
        seed_rooms()
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
