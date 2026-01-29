# 📦 Django Stock Management System

A web-based stock and inventory management system built with Django.

## 🚀 Features
- Product & Category management
- Stock in / stock out tracking
- Critical stock detection
- Admin dashboard with statistics
- Charts with Chart.js
- Role-based access control

## 🛠️ Technologies
- Python 3
- Django
- SQLite
- HTML / CSS
- Bootstrap
- Chart.js

## 📊 Dashboard
- Total products
- Total stock
- Stock movements
- Critical vs normal stock visualization

## ⚙️ Installation

```bash
git clone https://github.com/BusenurTerzi1/django-stock-management.git
cd django-stock-management
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
