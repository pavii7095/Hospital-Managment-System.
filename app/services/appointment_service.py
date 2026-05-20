#!/usr/bin/env python3
"""
Appointment Service
Handles appointment-related business logic
"""

from app import db
from app.models import Appointment, Patient, Doctor
from app.services.email_service import EmailService
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
email_service = EmailService()

class AppointmentService:
    """Service for managing appointments"""
    
    @staticmethod
    def create_appointment(patient_id, doctor_id, appointment_date, reason=None):
        """Create a new appointment
        
        Args:
            patient_id (int): ID of the patient
            doctor_id (int): ID of the doctor
            appointment_date (datetime): Date and time of appointment
            reason (str): Reason for appointment
        
        Returns:
            Appointment or None: Created appointment or None if failed
        """
        try:
            # Validate patient and doctor exist
            patient = Patient.query.get(patient_id)
            doctor = Doctor.query.get(doctor_id)
            
            if not patient or not doctor:
                logger.error(f"Patient {patient_id} or Doctor {doctor_id} not found")
                return None
            
            # Check for conflicts
            if AppointmentService.has_conflict(doctor_id, appointment_date):
                logger.error(f"Time conflict for doctor {doctor_id} at {appointment_date}")
                return None
            
            # Create appointment
            appointment = Appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_date=appointment_date,
                reason=reason,
                status='scheduled'
            )
            
            db.session.add(appointment)
            db.session.commit()
            
            # Send confirmation email
            email_service.send_appointment_confirmation(
                patient.email,
                patient.get_full_name(),
                doctor.name,
                appointment_date
            )
            
            logger.info(f"Appointment created: {appointment.id}")
            return appointment
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating appointment: {str(e)}")
            return None
    
    @staticmethod
    def has_conflict(doctor_id, appointment_date, duration_minutes=30):
        """Check if doctor has conflicting appointment
        
        Args:
            doctor_id (int): ID of the doctor
            appointment_date (datetime): Proposed appointment date
            duration_minutes (int): Appointment duration in minutes
        
        Returns:
            bool: True if conflict exists, False otherwise
        """
        appointment_end = appointment_date + timedelta(minutes=duration_minutes)
        
        conflict = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status != 'cancelled',
            Appointment.appointment_date < appointment_end,
            (Appointment.appointment_date + timedelta(minutes=duration_minutes)) > appointment_date
        ).first()
        
        return conflict is not None
    
    @staticmethod
    def cancel_appointment(appointment_id):
        """Cancel an appointment
        
        Args:
            appointment_id (int): ID of the appointment to cancel
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            appointment = Appointment.query.get(appointment_id)
            
            if not appointment:
                logger.error(f"Appointment {appointment_id} not found")
                return False
            
            patient = appointment.patient
            doctor = appointment.doctor
            
            appointment.status = 'cancelled'
            db.session.commit()
            
            # Send cancellation email
            email_service.send_cancellation_notification(
                patient.email,
                patient.get_full_name(),
                doctor.name,
                appointment.appointment_date
            )
            
            logger.info(f"Appointment {appointment_id} cancelled")
            return True
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error cancelling appointment: {str(e)}")
            return False
    
    @staticmethod
    def send_reminders():
        """Send appointment reminders for upcoming appointments (24 hours)"""
        try:
            now = datetime.utcnow()
            tomorrow = now + timedelta(hours=24)
            
            appointments = Appointment.query.filter(
                Appointment.appointment_date >= now,
                Appointment.appointment_date <= tomorrow,
                Appointment.status == 'scheduled',
                Appointment.reminder_sent == False
            ).all()
            
            for appointment in appointments:
                email_service.send_appointment_reminder(
                    appointment.patient.email,
                    appointment.patient.get_full_name(),
                    appointment.doctor.name,
                    appointment.appointment_date
                )
                appointment.reminder_sent = True
                db.session.commit()
            
            logger.info(f"Sent {len(appointments)} appointment reminders")
        
        except Exception as e:
            logger.error(f"Error sending reminders: {str(e)}")
    
    @staticmethod
    def get_upcoming_appointments(patient_id=None, doctor_id=None):
        """Get upcoming appointments
        
        Args:
            patient_id (int): Filter by patient ID
            doctor_id (int): Filter by doctor ID
        
        Returns:
            list: List of upcoming appointments
        """
        query = Appointment.query.filter(
            Appointment.appointment_date > datetime.utcnow(),
            Appointment.status != 'cancelled'
        )
        
        if patient_id:
            query = query.filter(Appointment.patient_id == patient_id)
        
        if doctor_id:
            query = query.filter(Appointment.doctor_id == doctor_id)
        
        return query.order_by(Appointment.appointment_date).all()
