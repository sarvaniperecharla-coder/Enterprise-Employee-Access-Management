# Enterprise Employee Access & Leave Management System

A backend-based employee management system built using Django REST Framework.  
This application helps organizations manage employees, departments, leave requests, approvals, notifications, and role-based access control.

---

# Features

## Authentication
- User registration
- JWT-based login authentication
- Access and refresh tokens
- Secure API authorization

## Employee Management
- Create employee profiles
- Update employee details
- View employee information
- Search and filter employees

## Department Management
- Create and manage departments
- Assign employees to departments
- View department details

## Leave Management
- Apply leave requests
- View leave history
- Approve or reject leave requests
- Track leave balance

## Dashboard
- Employee dashboard
- Manager dashboard
- Leave summary
- Notification tracking

---

# Tech Stack

## Backend
- Python
- Django
- Django REST Framework

## Authentication
- JWT Authentication
- Simple JWT

## Database
- MySQL

## API Documentation
- Swagger UI
- drf-spectacular

## Tools
- Git
- GitHub
- MySQL Workbench

---

# Project Structure


Enterprise-Employee-Access-Management
│
├── employee-service
│ │
│ ├── accounts
│ │ └── Authentication and user registration
│ │
│ ├── employees
│ │ └── Employee management APIs
│ │
│ ├── departments
│ │ └── Department management APIs
│ │
│ ├── leaves
│ │ └── Leave request and approval APIs
│ │
│ ├── dashboard
│ │ └── Employee and manager dashboards
│ │
│ ├── notifications
│ │ └── Notification management
│ │
│ └── manage.py
│
├── database
│
├── docker
│
├── docs
│
├── frontend
│
├── requirements
│
└── .gitignore

---

# Installation and Setup

## Clone Repository


git clone https://github.com/sarvaniperecharla-coder/Enterprise-Employee-Access-Management.git


## Navigate to Project


cd Enterprise-Employee-Access-Management


## Create Virtual Environment


python -m venv venv


## Activate Virtual Environment

Windows:


venv\Scripts\activate


---

# Install Dependencies


pip install -r requirements/django.txt


---

# Database Configuration

This project uses MySQL.

Create a database in MySQL:


CREATE DATABASE employee_access_db;


Update MySQL configuration in:


employee-service/employee_service/settings.py


Example:


DATABASES = {
"default": {
"ENGINE": "django.db.backends.mysql",
"NAME": "employee_access_db",
"USER": "your_mysql_username",
"PASSWORD": "your_mysql_password",
"HOST": "localhost",
"PORT": "3306",
}
}


---

# Run Migrations

Navigate to employee-service:


cd employee-service


Run:


python manage.py makemigrations

python manage.py migrate


---

# Create Admin User


python manage.py createsuperuser


---

# Run Development Server


python manage.py runserver


Application runs at:


http://127.0.0.1:8000/


---

# API Documentation

Swagger UI:


http://127.0.0.1:8000/api/docs/


---

# API Modules

The project includes:

- Authentication API
- Employee API
- Department API
- Leave API
- Dashboard API
- Notification API

---

# API Testing Flow

1. Register employee account using employee ID
2. Login using username and password
3. Generate JWT access token
4. Authorize Swagger using Bearer token
5. Access employee and department APIs
6. Apply leave request
7. Approve or reject leave as manager
8. Check dashboard and notifications

---

# User Roles

## Admin
- Full system access
- Manage employees and departments

## HR
- Manage employee information

## Manager
- View team leave requests
- Approve or reject leave requests

## Employee
- Apply for leaves
- View leave status
- Check leave balance

---

# Future Improvements

- React frontend integration
- Docker deployment
- Cloud deployment
- Email notifications
- Automated testing

---

# Author

Sarvani Perecharla
