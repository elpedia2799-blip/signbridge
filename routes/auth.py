from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from database.db import db
from models.user import User
from models.settings import SiteSettings

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    settings = SiteSettings.get_settings()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if not user.is_active_account:
                flash('Your account has been suspended by an administrator.', 'danger')
                return redirect(url_for('auth.login'))
            login_user(user)
            return redirect(url_for('dashboard.index'))
        flash('Invalid email or password', 'danger')
    return render_template('auth/login.html', settings=settings)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    settings = SiteSettings.get_settings()
    if not settings.allow_registration:
        flash('New user registration is currently disabled by the administrator.', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'warning')
            return redirect(url_for('auth.register'))
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', settings=settings)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
