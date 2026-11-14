from flask import Blueprint, render_template
from models.lesson import Lesson
from models.settings import SiteSettings

learning = Blueprint('learning', __name__)

@learning.route('/')
def index():
    settings = SiteSettings.get_settings()
    lessons = Lesson.query.order_by(Lesson.order_index).all()
    return render_template('learning/index.html', lessons=lessons, settings=settings)
