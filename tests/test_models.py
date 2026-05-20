#!/usr/bin/env python3
"""
Model Tests
Unit tests for database models
"""

import unittest
from datetime import datetime, date
from app import create_app, db
from app.models import Patient, Doctor, Appointment

class ModelTestCase(unittest.TestCase):
    """Base test case for models"""
    
    def setUp(self):
        """Set up test database"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Clean up test database"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

class PatientModelTest(ModelTestCase):
    """Test Patient model"""
    
    def test_patient_creation(self):
        """Test creating a patient"""
        patient = Patient(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            date_of_birth=date(1990, 1, 1)
        )
        db.session.add(patient)
        db.session.commit()
        
        self.assertEqual(patient.get_full_name(), 'John Doe')
        self.assertEqual(patient.email, 'john@example.com')
    
    def test_patient_to_dict(self):
        """Test patient to_dict method"""
        patient = Patient(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            phone='9876543210',
            date_of_birth=date(1995, 5, 15)
        )
        db.session.add(patient)
        db.session.commit()
        
        patient_dict = patient.to_dict()
        self.assertEqual(patient_dict['email'], 'jane@example.com')
        self.assertEqual(patient_dict['full_name'], 'Jane Smith')

class DoctorModelTest(ModelTestCase):
    """Test Doctor model"""
    
    def test_doctor_creation(self):
        """Test creating a doctor"""
        doctor = Doctor(
            name='Dr. Smith',
            specialization='Cardiology',
            email='smith@hospital.com'
        )
        db.session.add(doctor)
        db.session.commit()
        
        self.assertEqual(doctor.name, 'Dr. Smith')
        self.assertEqual(doctor.specialization, 'Cardiology')

class AppointmentModelTest(ModelTestCase):
    """Test Appointment model"""
    
    def test_appointment_creation(self):
        """Test creating an appointment"""
        patient = Patient(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            date_of_birth=date(1990, 1, 1)
        )
        doctor = Doctor(
            name='Dr. Smith',
            specialization='Cardiology',
            email='smith@hospital.com'
        )
        
        db.session.add(patient)
        db.session.add(doctor)
        db.session.commit()
        
        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=doctor.id,
            appointment_date=datetime(2024, 12, 25, 10, 0, 0),
            reason='Regular checkup'
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        self.assertEqual(appointment.patient_id, patient.id)
        self.assertEqual(appointment.doctor_id, doctor.id)

if __name__ == '__main__':
    unittest.main()
