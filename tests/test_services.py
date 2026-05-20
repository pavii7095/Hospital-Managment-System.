#!/usr/bin/env python3
"""
Service Tests
Unit tests for business logic services
"""

import unittest
from datetime import datetime, date, timedelta
from app import create_app, db
from app.models import Patient, Doctor, Appointment
from app.services import PatientService, DoctorService, AppointmentService

class ServiceTestCase(unittest.TestCase):
    """Base test case for services"""
    
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

class PatientServiceTest(ServiceTestCase):
    """Test PatientService"""
    
    def test_create_patient(self):
        """Test creating a patient via service"""
        patient = PatientService.create_patient(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            date_of_birth=date(1990, 1, 1)
        )
        
        self.assertIsNotNone(patient)
        self.assertEqual(patient.email, 'john@example.com')
    
    def test_get_patient(self):
        """Test retrieving a patient"""
        patient = PatientService.create_patient(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            phone='9876543210',
            date_of_birth=date(1995, 5, 15)
        )
        
        retrieved = PatientService.get_patient(patient.id)
        self.assertEqual(retrieved.email, 'jane@example.com')

class DoctorServiceTest(ServiceTestCase):
    """Test DoctorService"""
    
    def test_create_doctor(self):
        """Test creating a doctor via service"""
        doctor = DoctorService.create_doctor(
            name='Dr. Smith',
            specialization='Cardiology',
            email='smith@hospital.com'
        )
        
        self.assertIsNotNone(doctor)
        self.assertEqual(doctor.specialization, 'Cardiology')
    
    def test_get_doctors_by_specialization(self):
        """Test retrieving doctors by specialization"""
        DoctorService.create_doctor(
            name='Dr. Smith',
            specialization='Cardiology',
            email='smith@hospital.com'
        )
        
        doctors = DoctorService.get_doctors_by_specialization('Cardiology')
        self.assertEqual(len(doctors), 1)

class AppointmentServiceTest(ServiceTestCase):
    """Test AppointmentService"""
    
    def test_create_appointment(self):
        """Test creating an appointment via service"""
        patient = PatientService.create_patient(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            date_of_birth=date(1990, 1, 1)
        )
        
        doctor = DoctorService.create_doctor(
            name='Dr. Smith',
            specialization='Cardiology',
            email='smith@hospital.com'
        )
        
        appointment_date = datetime.utcnow() + timedelta(days=7)
        appointment = AppointmentService.create_appointment(
            patient_id=patient.id,
            doctor_id=doctor.id,
            appointment_date=appointment_date,
            reason='Regular checkup'
        )
        
        self.assertIsNotNone(appointment)
        self.assertEqual(appointment.patient_id, patient.id)

if __name__ == '__main__':
    unittest.main()
