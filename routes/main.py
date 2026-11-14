from flask import Blueprint, render_template
from models.settings import SiteSettings
from models.announcement import Announcement

main = Blueprint('main', __name__)

@main.route('/')
def index():
    settings = SiteSettings.get_settings()
    announcements = Announcement.query.filter_by(is_active=True).order_by(Announcement.id.desc()).all()
    return render_template('index.html', settings=settings, announcements=announcements)
