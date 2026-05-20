#!/usr/bin/env python3
"""
Patient Model
Represents a patient in the hospital management system
"""

from app import db
from datetime import datetime

class Patient(db.Model):
    """Patient model for storing patient information"""
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    medical_history = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Patient {self.first_name} {self.last_name}>'
    
    def get_full_name(self):
        """Return patient's full name"""
        return f'{self.first_name} {self.last_name}'
    
    def to_dict(self):
        """Convert patient to dictionary"""
        return {
            'id': self.id,
            'full_name': self.get_full_name(),
            'email': self.email,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth.isoformat(),
            'gender': self.gender,
            'address': self.address,
            'created_at': self.created_at.isoformat()
        }
