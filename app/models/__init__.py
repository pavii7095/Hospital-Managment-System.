#!/usr/bin/env python3
"""
Database Models
Defines Patient, Doctor, and Appointment models
"""

from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.appointment import Appointment

__all__ = ['Patient', 'Doctor', 'Appointment']
