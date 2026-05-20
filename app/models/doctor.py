#!/usr/bin/env python3
"""
Doctor Model
Represents a doctor in the hospital management system
"""

from app import db
from datetime import datetime

class Doctor(db.Model):
    """Doctor model for storing doctor information and availability"""
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    specialization = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    license_number = db.Column(db.String(50), unique=True, nullable=True)
    available = db.Column(db.Boolean, default=True)
    availability_hours = db.Column(db.String(255), nullable=True)  # e.g., "9:00-17:00"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Doctor {self.name} - {self.specialization}>'
    
    def to_dict(self):
        """Convert doctor to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'specialization': self.specialization,
            'email': self.email,
            'phone': self.phone,
            'available': self.available,
            'availability_hours': self.availability_hours,
            'created_at': self.created_at.isoformat()
        }
