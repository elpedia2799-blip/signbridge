import os
import time
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from database.db import db
from models.sign import Sign
from models.user import User
from models.lesson import Lesson
from models.announcement import Announcement
from models.settings import SiteSettings

admin = Blueprint('admin', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Hidden Full-Control Admin Panel (Direct URL /admin/, no password, no public links)
@admin.route('/')
def index():
    signs = Sign.query.order_by(Sign.id.desc()).all()
    users = User.query.order_by(User.id.desc()).all()
    lessons = Lesson.query.order_by(Lesson.order_index.asc(), Lesson.id.desc()).all()
    announcements = Announcement.query.order_by(Announcement.id.desc()).all()
    settings = SiteSettings.get_settings()
    return render_template(
        'admin/dashboard.html',
        signs=signs,
        users=users,
        lessons=lessons,
        announcements=announcements,
        settings=settings
    )

# --- 1. SIGN LANGUAGES & GESTURES FULL CONTROL ---
@admin.route('/signs/add', methods=['POST'])
def add_sign():
    word = request.form.get('word', '').strip()
    language = request.form.get('language', '').strip()
    custom_language = request.form.get('custom_language', '').strip()
    category = request.form.get('category', '').strip()
    description = request.form.get('description', '').strip()
    landmarks_json = request.form.get('landmarks_json', '').strip()
    file = request.files.get('media_file')

    final_language = custom_language if custom_language else (language or 'ASL (American Sign Language)')

    if not word:
        flash('Please enter a sign word or phrase.', 'danger')
        return redirect(url_for('admin.index'))

    media_filename = None
    if file and file.filename != '':
        if allowed_file(file.filename):
            timestamp = int(time.time())
            filename = secure_filename(f"admin_{timestamp}_{word}_{file.filename}")
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            media_filename = filename
        else:
            flash('Invalid file type. Allowed: png, jpg, jpeg, gif, mp4, webm.', 'danger')
            return redirect(url_for('admin.index'))

    new_sign = Sign(
        word=word,
        language=final_language,
        category=category or 'General',
        description=description,
        media_url=media_filename,
        landmarks_json=landmarks_json if landmarks_json else None,
        uploaded_by='Admin'
    )
    db.session.add(new_sign)
    db.session.commit()
    flash(f'Sign "{word}" ({final_language}) published across all user accounts!', 'success')
    return redirect(url_for('admin.index'))

@admin.route('/signs/edit/<int:sign_id>', methods=['POST'])
def edit_sign(sign_id):
    sign = Sign.query.get_or_404(sign_id)
    sign.word = request.form.get('word', sign.word).strip()
    sign.language = request.form.get('language', sign.language).strip()
    sign.category = request.form.get('category', sign.category).strip()
    sign.description = request.form.get('description', sign.description).strip()
    db.session.commit()
    flash(f'Updated sign "{sign.word}".', 'success')
    return redirect(url_for('admin.index'))

@admin.route('/signs/delete/<int:sign_id>', methods=['POST'])
def delete_sign(sign_id):
    sign = Sign.query.get_or_404(sign_id)
    if sign.media_url:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], sign.media_url)
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(sign)
    db.session.commit()
    flash(f'Deleted sign "{sign.word}".', 'info')
    return redirect(url_for('admin.index'))

@admin.route('/signs/clear_all', methods=['POST'])
def clear_all_signs():
    signs = Sign.query.all()
    for sign in signs:
        if sign.media_url:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], sign.media_url)
            if os.path.exists(file_path):
                os.remove(file_path)
        db.session.delete(sign)
    db.session.commit()
    flash('All signs cleared from the database.', 'warning')
    return redirect(url_for('admin.index'))

# --- 2. USER ACCOUNTS FULL CONTROL ---
@admin.route('/users/create', methods=['POST'])
def create_user():
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    if not username or not email or not password:
        flash('All fields are required to create a user.', 'danger')
        return redirect(url_for('admin.index'))
    if User.query.filter((User.email == email) | (User.username == username)).first():
        flash('Username or email already exists.', 'warning')
        return redirect(url_for('admin.index'))
    user = User(username=username, email=email, is_active_account=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    flash(f'Created user account "{username}".', 'success')
    return redirect(url_for('admin.index'))

@admin.route('/users/toggle/<int:user_id>', methods=['POST'])
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active_account = not user.is_active_account
    db.session.commit()
    status = "activated" if user.is_active_account else "suspended"
    flash(f'User "{user.username}" has been {status}.', 'info')
    return redirect(url_for('admin.index'))

@admin.route('/users/reset_password/<int:user_id>', methods=['POST'])
def reset_user_password(user_id):
    user = User.query.get_or_404(user_id)
    new_pw = request.form.get('new_password', '').strip()
    if new_pw:
        user.set_password(new_pw)
        db.session.commit()
        flash(f'Password updated for "{user.username}".', 'success')
    return redirect(url_for('admin.index'))

@admin.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'Deleted user "{user.username}".', 'danger')
    return redirect(url_for('admin.index'))

# --- 3. LEARNING LESSONS FULL CONTROL ---
@admin.route('/lessons/add', methods=['POST'])
def add_lesson():
    title = request.form.get('title', '').strip()
    language = request.form.get('language', 'ASL (American Sign Language)').strip()
    level = request.form.get('level', 'Beginner').strip()
    content = request.form.get('content', '').strip()
    order_index = int(request.form.get('order_index', 0) or 0)
    if title and content:
        lesson = Lesson(title=title, language=language, level=level, content=content, order_index=order_index)
        db.session.add(lesson)
        db.session.commit()
        flash(f'Lesson "{title}" published to Learning Centre!', 'success')
    return redirect(url_for('admin.index'))

@admin.route('/lessons/delete/<int:lesson_id>', methods=['POST'])
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    db.session.delete(lesson)
    db.session.commit()
    flash(f'Deleted lesson "{lesson.title}".', 'info')
    return redirect(url_for('admin.index'))

# --- 4. BROADCAST ANNOUNCEMENTS FULL CONTROL ---
@admin.route('/announcements/add', methods=['POST'])
def add_announcement():
    title = request.form.get('title', '').strip()
    message = request.form.get('message', '').strip()
    if title and message:
        ann = Announcement(title=title, message=message, is_active=True)
        db.session.add(ann)
        db.session.commit()
        flash('Announcement broadcasted across all user accounts!', 'success')
    return redirect(url_for('admin.index'))

@admin.route('/announcements/delete/<int:ann_id>', methods=['POST'])
def delete_announcement(ann_id):
    ann = Announcement.query.get_or_404(ann_id)
    db.session.delete(ann)
    db.session.commit()
    flash('Announcement removed.', 'info')
    return redirect(url_for('admin.index'))

# --- 5. SITE SETTINGS FULL CONTROL ---
@admin.route('/settings/update', methods=['POST'])
def update_settings():
    settings = SiteSettings.get_settings()
    settings.site_name = request.form.get('site_name', 'SignBridge').strip()
    settings.hero_title = request.form.get('hero_title', settings.hero_title).strip()
    settings.hero_subtitle = request.form.get('hero_subtitle', settings.hero_subtitle).strip()
    settings.allow_registration = 'allow_registration' in request.form
    db.session.commit()
    flash('Platform settings updated globally!', 'success')
    return redirect(url_for('admin.index'))
