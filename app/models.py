from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    stage = db.Column(db.String(50), nullable=False)  # This field should be non-nullable if required
    phone_number = db.Column(db.String(15), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Assignment(db.Model):
    __tablename__ = 'assignments'  # Table name should be plural for consistency
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.Enum('bio', 'geo', name='subject_enum'), nullable=False)
    stage = db.Column(db.Enum('first-grade', 'second-grade', 'third-grade', name='stage_enum'), nullable=False)  # Added stage field
    file_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='assignments')

class Exam(db.Model):
    __tablename__ = 'exams'  # Table name should be plural for consistency
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.Enum('bio', 'geo', name='subject_enum'), nullable=False)
    stage = db.Column(db.Enum('first-grade', 'second-grade', 'third-grade', name='stage_enum'), nullable=False)  # Added stage field
    file_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='exams')

class Video(db.Model):
    __tablename__ = 'videos'  # Table name should be plural for consistency
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.Enum('bio', 'geo', name='subject_enum'), nullable=False)
    stage = db.Column(db.Enum('first-grade', 'second-grade', 'third-grade', name='stage_enum'), nullable=False)  # Added stage field
    file_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    views = db.Column(db.Integer, default=0)
    max_views = db.Column(db.Integer, default=3)

    user = db.relationship('User', backref='videos')

class Course(db.Model):  # Renamed to Course
    __tablename__ = 'courses'  # Table name should be plural for consistency
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.Enum('bio', 'geo', name='subject_enum'), nullable=False)
    stage = db.Column(db.Enum('first-grade', 'second-grade', 'third-grade', name='stage_enum'), nullable=False)  # Added stage field
    file_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='courses')
