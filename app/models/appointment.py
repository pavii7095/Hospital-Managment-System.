#!/usr/bin/env python3
"""
Appointment Model
Represents a patient appointment with a doctor
"""

from app import db
from datetime import datetime
from enum import Enum

class AppointmentStatus(Enum):
    """Appointment status enum"""
    SCHEDULED = 'scheduled'
    CONFIRMED = 'confirmed'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    NO_SHOW = 'no_show'

class Appointment(db.Model):
    """Appointment model for scheduling patient appointments"""
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False, index=True)
    appointment_date = db.Column(db.DateTime, nullable=False, index=True)
    status = db.Column(db.String(20), default=AppointmentStatus.SCHEDULED.value)
    reason = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    reminder_sent = db.Column(db.Boolean, default=False)
    confirmation_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Appointment {self.id} - {self.patient_id} with {self.doctor_id}>'
    
    def to_dict(self):
        """Convert appointment to dictionary"""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.get_full_name(),
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name,
            'appointment_date': self.appointment_date.isoformat(),
            'status': self.status,
            'reason': self.reason,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }
    
    def is_upcoming(self):
        """Check if appointment is upcoming"""
        return self.appointment_date > datetime.utcnow() and self.status != AppointmentStatus.CANCELLED.value
