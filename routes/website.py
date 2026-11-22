from flask import Blueprint, render_template
from models.gallery import GalleryImage
from models import db

website_bp = Blueprint("website", __name__)

@website_bp.get("/")
def home():
    images = GalleryImage.query.order_by(GalleryImage.sort_order.asc()).all()
    return render_template("index.html", images=images)
