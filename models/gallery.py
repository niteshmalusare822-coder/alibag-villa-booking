from . import db

class GalleryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.String(250))
    is_cover = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
