from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Predefined admin credentials
ALLOWED_ADMINS = {
    'Ankith': '123',
    'mya': 'pass1'
}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # Add relationship to diary entries
    diary_entries = db.relationship('DiaryEntry', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<DiaryEntry {self.title}>'