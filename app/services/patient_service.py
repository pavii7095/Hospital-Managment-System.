#!/usr/bin/env python3
"""
Patient Service
Handles patient-related business logic
"""

from app import db
from app.models import Patient
import logging

logger = logging.getLogger(__name__)

class PatientService:
    """Service for managing patients"""
    
    @staticmethod
    def create_patient(first_name, last_name, email, phone, date_of_birth, gender=None, address=None):
        """Create a new patient
        
        Args:
            first_name (str): Patient's first name
            last_name (str): Patient's last name
            email (str): Patient's email
            phone (str): Patient's phone number
            date_of_birth (date): Patient's date of birth
            gender (str): Patient's gender
            address (str): Patient's address
        
        Returns:
            Patient or None: Created patient or None if failed
        """
        try:
            # Check if patient already exists
            existing = Patient.query.filter_by(email=email).first()
            if existing:
                logger.warning(f"Patient with email {email} already exists")
                return existing
            
            patient = Patient(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                date_of_birth=date_of_birth,
                gender=gender,
                address=address
            )
            
            db.session.add(patient)
            db.session.commit()
            
            logger.info(f"Patient created: {patient.id} - {patient.get_full_name()}")
            return patient
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating patient: {str(e)}")
            return None
    
    @staticmethod
    def get_patient(patient_id):
        """Get patient by ID
        
        Args:
            patient_id (int): Patient ID
        
        Returns:
            Patient or None: Patient object or None if not found
        """
        return Patient.query.get(patient_id)
    
    @staticmethod
    def get_patient_by_email(email):
        """Get patient by email
        
        Args:
            email (str): Patient email
        
        Returns:
            Patient or None: Patient object or None if not found
        """
        return Patient.query.filter_by(email=email).first()
    
    @staticmethod
    def update_patient(patient_id, **kwargs):
        """Update patient information
        
        Args:
            patient_id (int): Patient ID
            **kwargs: Fields to update
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            patient = Patient.query.get(patient_id)
            
            if not patient:
                logger.error(f"Patient {patient_id} not found")
                return False
            
            for key, value in kwargs.items():
                if hasattr(patient, key):
                    setattr(patient, key, value)
            
            db.session.commit()
            logger.info(f"Patient {patient_id} updated")
            return True
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating patient: {str(e)}")
            return False
    
    @staticmethod
    def get_all_patients():
        """Get all patients
        
        Returns:
            list: List of all patients
        """
        return Patient.query.all()
    
    @staticmethod
    def delete_patient(patient_id):
        """Delete a patient
        
        Args:
            patient_id (int): Patient ID
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            patient = Patient.query.get(patient_id)
            
            if not patient:
                logger.error(f"Patient {patient_id} not found")
                return False
            
            db.session.delete(patient)
            db.session.commit()
            
            logger.info(f"Patient {patient_id} deleted")
            return True
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting patient: {str(e)}")
            return False
