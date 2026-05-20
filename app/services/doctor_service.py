#!/usr/bin/env python3
"""
Doctor Service
Handles doctor-related business logic
"""

from app import db
from app.models import Doctor
import logging

logger = logging.getLogger(__name__)

class DoctorService:
    """Service for managing doctors"""
    
    @staticmethod
    def create_doctor(name, specialization, email, phone=None, license_number=None):
        """Create a new doctor
        
        Args:
            name (str): Doctor's full name
            specialization (str): Medical specialization
            email (str): Doctor's email
            phone (str): Doctor's phone number
            license_number (str): Medical license number
        
        Returns:
            Doctor or None: Created doctor or None if failed
        """
        try:
            # Check if doctor already exists
            existing = Doctor.query.filter_by(email=email).first()
            if existing:
                logger.warning(f"Doctor with email {email} already exists")
                return existing
            
            doctor = Doctor(
                name=name,
                specialization=specialization,
                email=email,
                phone=phone,
                license_number=license_number
            )
            
            db.session.add(doctor)
            db.session.commit()
            
            logger.info(f"Doctor created: {doctor.id} - {doctor.name}")
            return doctor
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating doctor: {str(e)}")
            return None
    
    @staticmethod
    def get_doctor(doctor_id):
        """Get doctor by ID
        
        Args:
            doctor_id (int): Doctor ID
        
        Returns:
            Doctor or None: Doctor object or None if not found
        """
        return Doctor.query.get(doctor_id)
    
    @staticmethod
    def get_doctors_by_specialization(specialization):
        """Get doctors by specialization
        
        Args:
            specialization (str): Medical specialization
        
        Returns:
            list: List of doctors with the specialization
        """
        return Doctor.query.filter_by(specialization=specialization).all()
    
    @staticmethod
    def update_doctor(doctor_id, **kwargs):
        """Update doctor information
        
        Args:
            doctor_id (int): Doctor ID
            **kwargs: Fields to update
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            doctor = Doctor.query.get(doctor_id)
            
            if not doctor:
                logger.error(f"Doctor {doctor_id} not found")
                return False
            
            for key, value in kwargs.items():
                if hasattr(doctor, key):
                    setattr(doctor, key, value)
            
            db.session.commit()
            logger.info(f"Doctor {doctor_id} updated")
            return True
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating doctor: {str(e)}")
            return False
    
    @staticmethod
    def get_all_doctors():
        """Get all doctors
        
        Returns:
            list: List of all doctors
        """
        return Doctor.query.all()
    
    @staticmethod
    def get_available_doctors():
        """Get all available doctors
        
        Returns:
            list: List of available doctors
        """
        return Doctor.query.filter_by(available=True).all()
    
    @staticmethod
    def delete_doctor(doctor_id):
        """Delete a doctor
        
        Args:
            doctor_id (int): Doctor ID
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            doctor = Doctor.query.get(doctor_id)
            
            if not doctor:
                logger.error(f"Doctor {doctor_id} not found")
                return False
            
            db.session.delete(doctor)
            db.session.commit()
            
            logger.info(f"Doctor {doctor_id} deleted")
            return True
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting doctor: {str(e)}")
            return False
