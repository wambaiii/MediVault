from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

# Required by Flask-Login to load a user from the database
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ── USERS TABLE ──────────────────────────────────────────────
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    full_name     = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role          = db.Column(db.Enum('admin', 'doctor', 'nurse', 'patient'), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    is_active     = db.Column(db.Boolean, default=True)

    # Relationships
    records_uploaded = db.relationship('MedicalRecord', backref='uploaded_by_user', lazy=True)

    def __repr__(self):
        return f'<User {self.email} - {self.role}>'


# ── PATIENTS TABLE ────────────────────────────────────────────
class Patient(db.Model):
    __tablename__ = 'patients'

    id            = db.Column(db.Integer, primary_key=True)
    full_name     = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender        = db.Column(db.Enum('male', 'female', 'other'), nullable=False)
    phone         = db.Column(db.String(20))
    email         = db.Column(db.String(120))
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    records = db.relationship('MedicalRecord', backref='patient', lazy=True)

    def __repr__(self):
        return f'<Patient {self.full_name}>'


# ── MEDICAL RECORDS TABLE ─────────────────────────────────────
class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'

    id                = db.Column(db.Integer, primary_key=True)
    patient_id        = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    uploaded_by       = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_name         = db.Column(db.String(255), nullable=False)   # Original filename
    stored_file_name  = db.Column(db.String(255), nullable=False)   # Encrypted filename on disk
    file_type         = db.Column(db.String(50))
    record_type       = db.Column(db.Enum('lab_result', 'prescription', 'diagnosis', 'imaging', 'other'), nullable=False)
    description       = db.Column(db.Text)
    iv                = db.Column(db.String(255), nullable=False)    # AES encryption IV
    uploaded_at       = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<MedicalRecord {self.file_name} - Patient {self.patient_id}>'


# ── AUDIT LOG TABLE ───────────────────────────────────────────
class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action      = db.Column(db.String(255), nullable=False)   # e.g. "uploaded file", "viewed record"
    target      = db.Column(db.String(255))                   # e.g. filename or patient name
    timestamp   = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address  = db.Column(db.String(50))

    def __repr__(self):
        return f'<AuditLog {self.action} by User {self.user_id}>'