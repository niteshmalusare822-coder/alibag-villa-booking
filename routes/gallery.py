from flask import Blueprint, render_template
from models.gallery import GalleryImage

gallery_bp = Blueprint("gallery", __name__)

@gallery_bp.get("/")
def view_gallery():
    images = GalleryImage.query.order_by(GalleryImage.sort_order.asc()).all()
    return render_template("gallery.html", images=images)
