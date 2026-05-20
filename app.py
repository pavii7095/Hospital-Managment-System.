from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///hospital.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', True)
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Host Configuration
HOST_URL = os.getenv('HOST_URL', 'http://localhost:5000')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

db = SQLAlchemy(app)
mail = Mail(app)

# Database Models
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    available_slots = db.Column(db.Integer, default=10)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'specialization': self.specialization,
            'email': self.email,
            'phone': self.phone,
            'available_slots': self.available_slots,
            'url': f"{HOST_URL}/api/doctors/{self.id}"
        }


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    medical_history = db.Column(db.Text)
    appointments = db.relationship('Appointment', backref='patient', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'age': self.age,
            'medical_history': self.medical_history,
            'url': f"{HOST_URL}/api/patients/{self.id}"
        }


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'appointment_date': self.appointment_date.isoformat(),
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'url': f"{HOST_URL}/api/appointments/{self.id}",
            'patient_url': f"{HOST_URL}/api/patients/{self.patient_id}",
            'doctor_url': f"{HOST_URL}/api/doctors/{self.doctor_id}"
        }


# Helper function to send emails
def send_appointment_email(patient_email, patient_name, doctor_name, appointment_date, appointment_type='confirmation'):
    try:
        if appointment_type == 'confirmation':
            subject = 'Appointment Confirmation'
            body = f"""
Dear {patient_name},

Your appointment has been successfully scheduled with Dr. {doctor_name} on {appointment_date.strftime('%Y-%m-%d %H:%M')}.

Please arrive 10 minutes early.

You can view your appointment details at: {HOST_URL}/api/appointments

Best regards,
Hospital Management System
"""
        else:
            subject = 'Appointment Cancellation'
            body = f"""
Dear {patient_name},

Your appointment with Dr. {doctor_name} on {appointment_date.strftime('%Y-%m-%d %H:%M')} has been cancelled.

Please contact us for further assistance.

For more details visit: {HOST_URL}/api/appointments

Best regards,
Hospital Management System
"""
        
        msg = Message(subject, recipients=[patient_email], body=body)
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


# Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'Hospital Management System API',
        'version': '1.0',
        'host': HOST_URL,
        'endpoints': {
            'doctors': f"{HOST_URL}/api/doctors",
            'patients': f"{HOST_URL}/api/patients",
            'appointments': f"{HOST_URL}/api/appointments",
            'statistics': f"{HOST_URL}/api/statistics"
        }
    })


# Doctor Routes
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify({
        'data': [doctor.to_dict() for doctor in doctors],
        'count': len(doctors),
        'host': HOST_URL,
        'endpoint': f"{HOST_URL}/api/doctors"
    })


@app.route('/api/doctors', methods=['POST'])
def create_doctor():
    data = request.json
    try:
        doctor = Doctor(
            name=data['name'],
            specialization=data['specialization'],
            email=data['email'],
            phone=data['phone']
        )
        db.session.add(doctor)
        db.session.commit()
        return jsonify({
            'data': doctor.to_dict(),
            'host': HOST_URL,
            'message': 'Doctor created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'host': HOST_URL}), 400


@app.route('/api/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return jsonify({
        'data': doctor.to_dict(),
        'host': HOST_URL
    })


@app.route('/api/doctors/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    data = request.json
    try:
        doctor.name = data.get('name', doctor.name)
        doctor.specialization = data.get('specialization', doctor.specialization)
        doctor.email = data.get('email', doctor.email)
        doctor.phone = data.get('phone', doctor.phone)
        doctor.available_slots = data.get('available_slots', doctor.available_slots)
        db.session.commit()
        return jsonify({
            'data': doctor.to_dict(),
            'host': HOST_URL,
            'message': 'Doctor updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'host': HOST_URL}), 400


@app.route('/api/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    try:
        db.session.delete(doctor)
        db.session.commit()
        return jsonify({
            'message': 'Doctor deleted successfully',
            'host': HOST_URL,
            'deleted_id': doctor_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'host': HOST_URL}), 400


# Patient Routes
@app.route('/api/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify({
        'data': [patient.to_dict() for patient in patients],
        'count': len(patients),
        'host': HOST_URL,
        'endpoint': f"{HOST_URL}/api/patients"
    })


@app.route('/api/patients', methods=['POST'])
def create_patient():
    data = request.json
    try:
        patient = Patient(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            age=data['age'],
            medical_history=data.get('medical_history', '')
        )
        db.session.add(patient)
        db.session.commit()
        return jsonify({
            'data': patient.to_dict(),
            'host': HOST_URL,
            'message': 'Patient created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'host': HOST_URL}), 400


@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return jsonify({
        'data': patient.to_dict(),
        'host': HOST_URL
    })


@app.route('/api/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.json
    try:
        patient.name = data.get('name', patient.name)
        patient.email = data.get('email', patient.email)
        patient.phone = data.get('phone', patient.phone)
        patient.age = data.get('age', patient.age)
        patient.medical_history = data.get('medical_history', patient.medical_history)
        db.session.commit()
        return jsonify({
            'data': patient.to_dict(),
            'host': HOST_URL,
            'message': 'Patient updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'host': HOST_URL}), 400


@app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    try:
        db.session.delete(patient)
        db.session.commit()
        return jsonify({
            'message': 'Patient deleted successfully',
            'host': HOST_URL,
            'deleted_id': patient_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'host': HOST_URL}), 400


# Appointment Routes
@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify({
        'data': [appointment.to_dict() for appointment in appointments],
        'count': len(appointments),
        'host': HOST_URL,
        'endpoint': f"{HOST_URL}/api/appointments"
    })


@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    try:
        patient = Patient.query.get_or_404(data['patient_id'])
        doctor = Doctor.query.get_or_404(data['doctor_id'])
        
        if doctor.available_slots <= 0:
            return jsonify({
                'error': 'No available slots for this doctor',
                'host': HOST_URL,
                'doctor_url': f"{HOST_URL}/api/doctors/{doctor.id}"
            }), 400
        
        appointment_date = datetime.fromisoformat(data['appointment_date'])
        
        appointment = Appointment(
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            appointment_date=appointment_date,
            notes=data.get('notes', '')
        )
        
        doctor.available_slots -= 1
        db.session.add(appointment)
        db.session.commit()
        
        # Send confirmation email
        send_appointment_email(
            patient.email,
            patient.name,
            doctor.name,
            appointment_date,
            'confirmation'
        )
        
        return jsonify({
            'data': appointment.to_dict(),
            'host': HOST_URL,
            'message': 'Appointment created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'host': HOST_URL}), 400


@app.route('/api/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    return jsonify({
        'data': appointment.to_dict(),
        'host': HOST_URL
    })


@app.route('/api/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    data = request.json
    try:
        old_status = appointment.status
        appointment.status = data.get('status', appointment.status)
        appointment.notes = data.get('notes', appointment.notes)
        
        if old_status != 'cancelled' and data.get('status') == 'cancelled':
            doctor = appointment.doctor
            doctor.available_slots += 1
            
            send_appointment_email(
                appointment.patient.email,
                appointment.patient.name,
                doctor.name,
                appointment.appointment_date,
                'cancellation'
            )
        
        db.session.commit()
        return jsonify({
            'data': appointment.to_dict(),
            'host': HOST_URL,
            'message': 'Appointment updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'host': HOST_URL}), 400


@app.route('/api/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    try:
        doctor = appointment.doctor
        if appointment.status != 'cancelled':
            doctor.available_slots += 1
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({
            'message': 'Appointment deleted successfully',
            'host': HOST_URL,
            'deleted_id': appointment_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e), 'host': HOST_URL}), 400


# Statistics and Reports
@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    total_appointments = Appointment.query.count()
    scheduled_appointments = Appointment.query.filter_by(status='scheduled').count()
    completed_appointments = Appointment.query.filter_by(status='completed').count()
    
    return jsonify({
        'data': {
            'total_patients': total_patients,
            'total_doctors': total_doctors,
            'total_appointments': total_appointments,
            'scheduled_appointments': scheduled_appointments,
            'completed_appointments': completed_appointments
        },
        'host': HOST_URL,
        'endpoint': f"{HOST_URL}/api/statistics"
    })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print(f"\n{'='*60}")
    print(f"Hospital Management System Starting...")
    print(f"{'='*60}")
    print(f"Host URL: {HOST_URL}")
    print(f"Server: {HOST}:{PORT}")
    print(f"Debug: True")
    print(f"{'='*60}\n")
    app.run(debug=True, host=HOST, port=PORT)
