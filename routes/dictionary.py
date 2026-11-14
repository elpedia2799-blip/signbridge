from flask import Blueprint, render_template, request, send_from_directory, current_app
from models.sign import Sign
from models.settings import SiteSettings

dictionary = Blueprint('dictionary', __name__)

@dictionary.route('/')
def index():
    settings = SiteSettings.get_settings()
    query = request.args.get('q', '')
    lang_filter = request.args.get('lang', '')

    signs_query = Sign.query
    if query:
        signs_query = signs_query.filter(Sign.word.ilike(f'%{query}%'))
    if lang_filter:
        signs_query = signs_query.filter(Sign.language == lang_filter)

    signs = signs_query.order_by(Sign.id.desc()).all()
    languages = [r[0] for r in Sign.query.with_entities(Sign.language).distinct().all() if r[0]]
    return render_template('dictionary/index.html', signs=signs, query=query, lang_filter=lang_filter, languages=languages, settings=settings)

@dictionary.route('/media/<path:filename>')
def serve_media(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
