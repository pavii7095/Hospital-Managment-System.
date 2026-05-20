#!/usr/bin/env python3
"""
Database Setup Script
Initializes the database with required tables and default data
"""

import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import Patient, Doctor, Appointment

load_dotenv()

def init_database():
    """Initialize the database with tables"""
    app = create_app()
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database initialized successfully!")
        
        # Add sample data
        sample_doctors = [
            Doctor(name='Dr. John Smith', specialization='Cardiology', email='dr.smith@hospital.com'),
            Doctor(name='Dr. Sarah Johnson', specialization='Orthopedics', email='dr.johnson@hospital.com'),
            Doctor(name='Dr. Mike Wilson', specialization='Neurology', email='dr.wilson@hospital.com'),
        ]
        
        for doctor in sample_doctors:
            if not Doctor.query.filter_by(email=doctor.email).first():
                db.session.add(doctor)
        
        db.session.commit()
        print("Sample doctors added successfully!")

if __name__ == '__main__':
    init_database()
