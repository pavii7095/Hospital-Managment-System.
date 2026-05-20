#!/usr/bin/env python3
"""
API Routes
Provides REST API endpoints for the hospital management system
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models import Patient, Doctor, Appointment
from app.services import PatientService, DoctorService, AppointmentService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Patient Routes
@bp.route('/patients', methods=['GET'])
def get_patients():
    """Get all patients"""
    try:
        patients = PatientService.get_all_patients()
        return jsonify([patient.to_dict() for patient in patients]), 200
    except Exception as e:
        logger.error(f"Error fetching patients: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get patient by ID"""
    try:
        patient = PatientService.get_patient(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        return jsonify(patient.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching patient: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/patients', methods=['POST'])
def create_patient():
    """Create a new patient"""
    try:
        data = request.get_json()
        
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        
        patient = PatientService.create_patient(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            date_of_birth=date_of_birth,
            gender=data.get('gender'),
            address=data.get('address')
        )
        
        if not patient:
            return jsonify({'error': 'Failed to create patient'}), 400
        
        return jsonify(patient.to_dict()), 201
    except Exception as e:
        logger.error(f"Error creating patient: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update patient information"""
    try:
        data = request.get_json()
        
        if PatientService.update_patient(patient_id, **data):
            patient = PatientService.get_patient(patient_id)
            return jsonify(patient.to_dict()), 200
        else:
            return jsonify({'error': 'Patient not found'}), 404
    except Exception as e:
        logger.error(f"Error updating patient: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Delete a patient"""
    try:
        if PatientService.delete_patient(patient_id):
            return jsonify({'message': 'Patient deleted successfully'}), 200
        else:
            return jsonify({'error': 'Patient not found'}), 404
    except Exception as e:
        logger.error(f"Error deleting patient: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Doctor Routes
@bp.route('/doctors', methods=['GET'])
def get_doctors():
    """Get all doctors"""
    try:
        doctors = DoctorService.get_all_doctors()
        return jsonify([doctor.to_dict() for doctor in doctors]), 200
    except Exception as e:
        logger.error(f"Error fetching doctors: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    """Get doctor by ID"""
    try:
        doctor = DoctorService.get_doctor(doctor_id)
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        return jsonify(doctor.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching doctor: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/doctors/specialization/<specialization>', methods=['GET'])
def get_doctors_by_specialization(specialization):
    """Get doctors by specialization"""
    try:
        doctors = DoctorService.get_doctors_by_specialization(specialization)
        return jsonify([doctor.to_dict() for doctor in doctors]), 200
    except Exception as e:
        logger.error(f"Error fetching doctors: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/doctors', methods=['POST'])
def create_doctor():
    """Create a new doctor"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'specialization', 'email']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        doctor = DoctorService.create_doctor(
            name=data['name'],
            specialization=data['specialization'],
            email=data['email'],
            phone=data.get('phone'),
            license_number=data.get('license_number')
        )
        
        if not doctor:
            return jsonify({'error': 'Failed to create doctor'}), 400
        
        return jsonify(doctor.to_dict()), 201
    except Exception as e:
        logger.error(f"Error creating doctor: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/doctors/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    """Update doctor information"""
    try:
        data = request.get_json()
        
        if DoctorService.update_doctor(doctor_id, **data):
            doctor = DoctorService.get_doctor(doctor_id)
            return jsonify(doctor.to_dict()), 200
        else:
            return jsonify({'error': 'Doctor not found'}), 404
    except Exception as e:
        logger.error(f"Error updating doctor: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    """Delete a doctor"""
    try:
        if DoctorService.delete_doctor(doctor_id):
            return jsonify({'message': 'Doctor deleted successfully'}), 200
        else:
            return jsonify({'error': 'Doctor not found'}), 404
    except Exception as e:
        logger.error(f"Error deleting doctor: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Appointment Routes
@bp.route('/appointments', methods=['GET'])
def get_appointments():
    """Get upcoming appointments"""
    try:
        patient_id = request.args.get('patient_id', type=int)
        doctor_id = request.args.get('doctor_id', type=int)
        
        appointments = AppointmentService.get_upcoming_appointments(patient_id, doctor_id)
        return jsonify([appointment.to_dict() for appointment in appointments]), 200
    except Exception as e:
        logger.error(f"Error fetching appointments: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/appointments', methods=['POST'])
def create_appointment():
    """Create a new appointment"""
    try:
        data = request.get_json()
        
        required_fields = ['patient_id', 'doctor_id', 'appointment_date']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        appointment_date = datetime.fromisoformat(data['appointment_date'])
        
        appointment = AppointmentService.create_appointment(
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            appointment_date=appointment_date,
            reason=data.get('reason')
        )
        
        if not appointment:
            return jsonify({'error': 'Failed to create appointment'}), 400
        
        return jsonify(appointment.to_dict()), 201
    except Exception as e:
        logger.error(f"Error creating appointment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
def cancel_appointment(appointment_id):
    """Cancel an appointment"""
    try:
        if AppointmentService.cancel_appointment(appointment_id):
            return jsonify({'message': 'Appointment cancelled successfully'}), 200
        else:
            return jsonify({'error': 'Appointment not found'}), 404
    except Exception as e:
        logger.error(f"Error cancelling appointment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Hospital Management System is running'}), 200
