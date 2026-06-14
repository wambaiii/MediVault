from flask import render_template
from flask_login import login_required, current_user
from app.records import records

@records.route('/dashboard')
@login_required
def dashboard():
    print(f"DEBUG: User {current_user} reached dashboard")
    return render_template('dashboard.html')