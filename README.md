# Mini_Store Django Project

## Features

- Product Catalog
- Shopping Cart
- Order Management
- Product Reviews
- REST APIs
- Celery Background Tasks
- Redis Broker
- Low Stock Alerts
- Request Timing Middleware
- Automated Tests

## Tech Stack

- Django
- Django REST Framework
- Celery
- Redis
- SQLite

## Run Project

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

## Run Celery

celery -A mini_store worker --pool=solo -l info

## Run Celery Beat

celery -A mini_store beat -l info
