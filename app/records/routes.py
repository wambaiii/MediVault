from flask import render_template, redirect, url_for
from flask_login import current_user,login_required
from app.records import records

@records.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')