#!/usr/bin/env python3
"""
Email Service
Handles all email notifications and communications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

load_dotenv()

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending emails for appointments and notifications"""
    
    def __init__(self):
        """Initialize email service with SMTP configuration"""
        self.sender_email = os.getenv('EMAIL_SENDER')
        self.sender_password = os.getenv('EMAIL_PASSWORD')
        self.smtp_server = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('EMAIL_SMTP_PORT', 587))
    
    def send_email(self, recipient_email, subject, body, html=False):
        """Send an email
        
        Args:
            recipient_email (str): Email address of recipient
            subject (str): Email subject
            body (str): Email body content
            html (bool): Whether body is HTML content
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = recipient_email
            
            # Attach body
            if html:
                part = MIMEText(body, 'html')
            else:
                part = MIMEText(body, 'plain')
            message.attach(part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            logger.info(f"Email sent to {recipient_email}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
            return False
    
    def send_appointment_confirmation(self, patient_email, patient_name, doctor_name, appointment_date):
        """Send appointment confirmation email
        
        Args:
            patient_email (str): Patient email address
            patient_name (str): Patient full name
            doctor_name (str): Doctor name
            appointment_date (datetime): Appointment date and time
        """
        subject = "Appointment Confirmation - Hospital Management System"
        
        html_body = f"""
        <html>
            <body>
                <h2>Appointment Confirmation</h2>
                <p>Dear {patient_name},</p>
                <p>Your appointment has been confirmed with the following details:</p>
                <ul>
                    <li><strong>Doctor:</strong> {doctor_name}</li>
                    <li><strong>Date & Time:</strong> {appointment_date.strftime('%Y-%m-%d %H:%M')}</li>
                </ul>
                <p>Please arrive 10 minutes before your scheduled appointment time.</p>
                <p>If you need to cancel or reschedule, please contact us as soon as possible.</p>
                <p>Best regards,<br>Hospital Management System</p>
            </body>
        </html>
        """
        
        return self.send_email(patient_email, subject, html_body, html=True)
    
    def send_appointment_reminder(self, patient_email, patient_name, doctor_name, appointment_date):
        """Send appointment reminder email
        
        Args:
            patient_email (str): Patient email address
            patient_name (str): Patient full name
            doctor_name (str): Doctor name
            appointment_date (datetime): Appointment date and time
        """
        subject = "Appointment Reminder - Hospital Management System"
        
        html_body = f"""
        <html>
            <body>
                <h2>Appointment Reminder</h2>
                <p>Dear {patient_name},</p>
                <p>This is a friendly reminder about your upcoming appointment:</p>
                <ul>
                    <li><strong>Doctor:</strong> {doctor_name}</li>
                    <li><strong>Date & Time:</strong> {appointment_date.strftime('%Y-%m-%d %H:%M')}</li>
                </ul>
                <p>Please make sure to arrive on time.</p>
                <p>If you cannot attend, please cancel or reschedule your appointment.</p>
                <p>Best regards,<br>Hospital Management System</p>
            </body>
        </html>
        """
        
        return self.send_email(patient_email, subject, html_body, html=True)
    
    def send_cancellation_notification(self, patient_email, patient_name, doctor_name, appointment_date):
        """Send appointment cancellation notification
        
        Args:
            patient_email (str): Patient email address
            patient_name (str): Patient full name
            doctor_name (str): Doctor name
            appointment_date (datetime): Appointment date and time
        """
        subject = "Appointment Cancelled - Hospital Management System"
        
        html_body = f"""
        <html>
            <body>
                <h2>Appointment Cancelled</h2>
                <p>Dear {patient_name},</p>
                <p>Your appointment has been cancelled:</p>
                <ul>
                    <li><strong>Doctor:</strong> {doctor_name}</li>
                    <li><strong>Date & Time:</strong> {appointment_date.strftime('%Y-%m-%d %H:%M')}</li>
                </ul>
                <p>To schedule a new appointment, please contact us.</p>
                <p>Best regards,<br>Hospital Management System</p>
            </body>
        </html>
        """
        
        return self.send_email(patient_email, subject, html_body, html=True)
