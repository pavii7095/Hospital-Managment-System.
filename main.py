#!/usr/bin/env python3
"""
Hospital Management System - Main Application Entry Point
Handles appointments, patient management, and email notifications
"""

import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import Patient, Doctor, Appointment

load_dotenv()

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Patient': Patient, 'Doctor': Doctor, 'Appointment': Appointment}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    debug_mode = os.getenv('FLASK_DEBUG', False)
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
