#!/usr/bin/env python3
"""
Web Routes
Provides web interface routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services import PatientService, DoctorService, AppointmentService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('web', __name__)

@bp.route('/')
def index():
    """Home page"""
    return redirect(url_for('web.dashboard'))

@bp.route('/dashboard')
def dashboard():
    """Dashboard page"""
    try:
        appointments = AppointmentService.get_upcoming_appointments()
        patients_count = len(PatientService.get_all_patients())
        doctors_count = len(DoctorService.get_all_doctors())
        
        return render_template('dashboard.html',
                             appointments=appointments,
                             patients_count=patients_count,
                             doctors_count=doctors_count)
    except Exception as e:
        logger.error(f"Error loading dashboard: {str(e)}")
        return 'Error loading dashboard', 500

@bp.route('/patients')
def patients():
    """Patients list page"""
    try:
        patients_list = PatientService.get_all_patients()
        return render_template('patients.html', patients=patients_list)
    except Exception as e:
        logger.error(f"Error loading patients: {str(e)}")
        return 'Error loading patients', 500

@bp.route('/doctors')
def doctors():
    """Doctors list page"""
    try:
        doctors_list = DoctorService.get_all_doctors()
        return render_template('doctors.html', doctors=doctors_list)
    except Exception as e:
        logger.error(f"Error loading doctors: {str(e)}")
        return 'Error loading doctors', 500

@bp.route('/appointments')
def appointments():
    """Appointments list page"""
    try:
        appointments_list = AppointmentService.get_upcoming_appointments()
        return render_template('appointments.html', appointments=appointments_list)
    except Exception as e:
        logger.error(f"Error loading appointments: {str(e)}")
        return 'Error loading appointments', 500
