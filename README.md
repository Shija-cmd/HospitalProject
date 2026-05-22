# 🏥 Maga Hospital Management System (HMS)

A modern, intelligent, and workflow-driven Hospital Management System built with Django to streamline hospital operations, patient management, and clinical workflows.

Designed with real hospital workflow architecture, role-based access control, automation, and scalable healthcare engineering principles in mind.

---

# 🌐 Live System

🚀 Official Live System:  
https://shijajuma.website

For demo access, collaboration, or contributions, feel free to contact me.

---

# ✨ Core Features

## 👨‍⚕️ Multi-Department Workflow System

The HMS supports complete hospital outpatient workflow management across multiple departments:

- Reception Module
- Vitals Module
- Doctor Module
- Laboratory Module
- Procedure / Imaging Module
- Cashier Module
- Dispense / Pharmacy Module
- Administrative Dashboard

---

# 📋 Patient Management

- Patient registration system
- Unique patient ID generation
- Search and filter patients
- Visit history tracking
- Real-time workflow status updates
- Queue-based patient flow management

---

# 🩺 Intelligent Clinical Workflow

## Doctor Consultation
- Clinical history recording
- Diagnosis management
- Doctor review workflow
- Prescription management

## Laboratory Workflow
- Lab request processing
- Laboratory result management
- Doctor review integration

## Procedure / Imaging Workflow
- Procedure requests
- X-Ray / Ultrasound workflow
- Technician findings and notes
- Medical image uploads
- Procedure review by doctors

## Pharmacy & Dispensing
- Prescription dispensing
- Medication tracking
- Pharmacy workflow management

---

# 💰 Billing & Cashier Module

- Consultation billing
- Laboratory billing
- Procedure billing
- Medication billing
- Payment completion workflow
- Automated transition to dispensing queue

---

# 📄 PDF Medical Reports

Generate professional downloadable patient reports containing:

- Patient information
- Clinical diagnosis
- Laboratory findings
- Procedure findings
- Prescriptions
- Dispensed medications

---

# 🤖 AI-Powered Features

## 🧠 STDs Prediction AI Model

Integrated Machine Learning model for:

- STD risk prediction
- Clinical decision support
- Intelligent healthcare assistance

## 💬 AI Healthcare Chatbot

Interactive AI chatbot capable of:

- Responding to hospital FAQs
- Assisting visitors
- Enhancing user interaction
- Improving accessibility to healthcare information

---

# 📊 Dashboard & Analytics

- Total patients
- Waiting vitals queue
- Waiting doctor queue
- Waiting laboratory queue
- Waiting procedure queue
- Cashier queue
- Dispense queue
- Completed visits analytics

---

# 🔐 Authentication & Security

- Django authentication system
- Role-Based Access Control (RBAC)
- Group permissions
- Secure department restrictions
- CSRF protection
- Authentication-required workflows

---

# 🧪 Automated System Testing

The system includes Django automated unit testing for workflow stability and regression prevention.

Currently tested workflows include:

- Visit creation workflow
- Vitals → Doctor transition
- Procedure → Doctor Review workflow
- Cashier → Dispense workflow
- Doctor review queue validation

Testing framework powered by:

```bash
python manage.py test
```bash
git clone https://github.com/your-username/your-repo-name.git

🚀 Technologies Used
Python
Django
Bootstrap 5
HTML5
CSS3
JavaScript
SQLite / PostgreSQL
Machine Learning
xhtml2pdf
Pillow

⚙️ Installation
1️⃣ Clone Repository
git clone <your-repository-url>

2️⃣ Navigate Into Project
cd project-folder

3️⃣ Create Virtual Environment
python -m venv venv

Activate environment:

Windows
venv\Scripts\activate

Linux / macOS
source venv/bin/activate

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Start Development Server
python manage.py runserver

🧪 Run Automated Tests
python manage.py test

📌 Future Improvements
Full IPD (Inpatient Department) module
Bed and ward management
Nurse workflow system
Appointment reminders
Email/SMS notifications
Advanced analytics dashboard
REST API integration
Mobile application support

👨‍💻 Developer

Developed by Juma Shija

Backend Engineer | Django Developer | AI & Healthcare Systems Enthusiast

🌐 Website: https://shijajuma.website

⭐ Project Vision

This project aims to bridge healthcare operations and intelligent software engineering by providing scalable, workflow-oriented, and AI-enhanced hospital management solutions suitable for modern healthcare environments.
