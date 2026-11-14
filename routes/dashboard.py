from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models.sign import Sign
from models.announcement import Announcement
from models.settings import SiteSettings

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@login_required
def index():
    settings = SiteSettings.get_settings()
    lang_filter = request.args.get('lang', '')
    if lang_filter:
        all_signs = Sign.query.filter_by(language=lang_filter).order_by(Sign.id.desc()).all()
    else:
        all_signs = Sign.query.order_by(Sign.id.desc()).all()
    languages = [r[0] for r in Sign.query.with_entities(Sign.language).distinct().all() if r[0]]
    announcements = Announcement.query.filter_by(is_active=True).order_by(Announcement.id.desc()).all()
    return render_template('user/dashboard.html', user=current_user, all_signs=all_signs, lang_filter=lang_filter, languages=languages, announcements=announcements, settings=settings)
