from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, AuditLog
from app.encryption import hash_password, verify_password
from app.auth import auth

# ── REGISTER ──────────────────────────────────────────────────
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('records.dashboard'))

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email     = request.form.get('email')
        password  = request.form.get('password')
        role      = request.form.get('role')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(
            full_name     = full_name,
            email         = email,
            password_hash = hash_password(password),
            role          = role
        )
        db.session.add(new_user)
        db.session.commit()

        log = AuditLog(
            user_id    = new_user.id,
            action     = 'User registered',
            target     = email,
            ip_address = request.remote_addr
        )
        db.session.add(log)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# ── LOGIN ─────────────────────────────────────────────────────
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('records.dashboard'))

    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not verify_password(password, user.password_hash):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))

        # Save audit log BEFORE login_user
        log = AuditLog(
            user_id    = user.id,
            action     = 'User logged in',
            target     = email,
            ip_address = request.remote_addr
        )
        db.session.add(log)
        db.session.commit()

        # Login AFTER db operations
        login_user(user, remember=True)

        flash(f'Welcome back, {user.full_name}!', 'success')
        return redirect(url_for('records.dashboard'))

    return render_template('login.html')


# ── LOGOUT ────────────────────────────────────────────────────
@auth.route('/logout')
@login_required
def logout():
    log = AuditLog(
        user_id    = current_user.id,
        action     = 'User logged out',
        target     = current_user.email,
        ip_address = request.remote_addr
    )
    db.session.add(log)
    db.session.commit()

    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))