from app import create_app, db
from app.models import User, Patient, MedicalRecord, AuditLog

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates all tables in the database
        print("✅ Database tables created successfully!")
    
    app.run(debug=True)