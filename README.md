# Hospital-Managment-System.
"Local hospital management system with appointments and email notifications"

## 📋 Overview
A comprehensive local hospital management system built with Python that streamlines hospital operations by managing patient appointments and automating email notifications.

## ✨ Features
- **Appointment Management**: Schedule and manage patient appointments
- **Email Notifications**: Automatic email notifications for appointment confirmations and reminders
- **Patient Management**: Manage patient information and records
- **Doctor Scheduling**: Track and manage doctor availability
- **Notification System**: Automated alerts for appointments and updates

## 🛠️ Tech Stack
- **Language**: Python
- **Backend**: Python-based application
- **Database**: Local database support
- **Notifications**: Email integration for automated notifications

## 📦 Installation

### Prerequisites
- Python 3.x installed on your system
- pip (Python package manager)

### Setup Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/pavii7095/Hospital-Managment-System..git
   cd Hospital-Managment-System.
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Create a `.env` file with your email and database configurations
   - Add necessary credentials for email notifications

4. Initialize the database:
   ```bash
   python setup.py
   ```

## 🚀 Usage

### Running the Application
```bash
python main.py
```

### Key Operations
- Schedule new appointments
- View existing appointments
- Send email notifications
- Manage patient records
- Track doctor schedules

## 📧 Email Configuration
Configure your email settings in the environment variables:
- Email service (Gmail, Outlook, etc.)
- SMTP credentials
- Sender email address

## 📁 Project Structure
```
Hospital-Managment-System/
├── main.py
├── requirements.txt
├── setup.py
├── config/
├── models/
├── services/
└── README.md
```

## 🤝 Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests with improvements.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### Email Not Sending
- Verify SMTP credentials in .env file
- Check email service settings allow less secure app access
- Ensure internet connection is active

### Database Issues
- Ensure database file has proper permissions
- Verify database initialization completed successfully

## 📞 Support
For issues, questions, or suggestions, please open an issue on the GitHub repository.

---
**Last Updated**: 2026-05-20
