from app import create_app, db
from app.models import User, Patient, MedicalRecord, AuditLog

app = create_app()
app.secret_key = 'medivault-super-secret-key-2024-strathmore'

@app.route('/test-session')
def test_session():
    from flask import session
    from flask_login import current_user
    session['test'] = 'hello'
    return f"Session={session}, Authenticated={current_user.is_authenticated}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")
        print(f"✅ Secret key: {app.secret_key}")

    app.run(debug=True, use_reloader=False)