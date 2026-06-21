# Mini_Store Django Project
A Django-based e-commerce application implementing product catalog management, shopping cart functionality, order processing, mock payment integration, REST APIs, and asynchronous email notifications using Celery and Redis.

## Features

## Product Catalog

      - Categories with parent-child hierarchy
      - Product management
      - Product variants (size, color, SKU)
      - Product images
      - Product reviews and ratings
Shopping Cart

      -Session-based cart
      -Add products to cart
      -Update quantities
      -Remove products
      -Cart total calculation
Order Management

      -Checkout process
      -Order history
      -Order details page
      -Order cancellation
      -Stock validation
Payment

      Mock Stripe payment implementation
      Test card support:
        4242 4242 4242 4242
      Payment success/failure handling
Email Notifications

      -HTML order confirmation emails
      -Celery background tasks
      -Redis message broker
REST APIs

      -Product API
      -Review API
      -Order API
Admin Features

      -Product management
      -Category management
      -Review management
      -Order management
      -Product activation/deactivation
      
Product Reviews
REST APIs
Celery Background Tasks
Redis Broker
Low Stock Alerts
Request Timing Middleware
Automated Tests

## Tech Stack

- Python 3.12
- Django 4.2
- Django
- Django REST Framework
- Celery
- Redis
- Pillow
- SQLite

## Installation

Clone Repository
    git clone <repository-url> 
    cd mini_store
Create Virtual Environment
    python -m venv venv
Activate Virtual Environment
    Windows:   venv\Scripts\activate
    Linux/macOS:    source venv/bin/activate

Install Dependencies
    pip install -r requirements.txt
Apply Migrations
    python manage.py migrate
Create Superuser
    python manage.py createsuperuser
Environment Variables
    Create a .env file from .env.example.

## Redis Setup
    Ubuntu / WSL
      Start Redis:
          sudo service redis-server start
      Verify:
          redis-cli ping
      Expected:
          PONG
## Run Project

    Start Django Server
        python manage.py runserver
    Start Celery Worker
        Open a new terminal:
          celery -A mini_store worker -l info --pool=solo
    Start Celery Beat
        Open another terminal:
          celery -A mini_store beat -l info

## Running Tests

  Execute:
      python manage.py test
  Current result:
      Ran 16 tests
      OK

## Mock Payment

  This project uses a mock payment implementation to simulate Stripe test mode.
    Use the following card number: 4242 4242 4242 4242
    Payment succeeds when the valid test card is entered.
    Invalid card numbers trigger a payment failure page and prevent order creation.

## Celery Tasks

      Order Confirmation Email
      Triggered after successful payment.
      Features:
          HTML email format
          Order summary
          Background execution using Celery
          Low Stock Alert
      Scheduled using Celery Beat.
      Monitors product variant inventory levels.

## API Endpoints

      Products : /api/products/
      Product Detail : /api/products/<slug>/
      Reviews : /api/reviews/
      Orders :  /api/orders/
      Cancel Order :  /api/orders/<id>/cancel/

## Screenshots

    Screenshots demonstrating:
      Login Page
      Home Page
      Product List
      Shopping Cart
      Checkout
      Payment
      Order History
      Order Details
      Admin Panel
    are included in the screenshots folder.

## Future Improvements
    Real Stripe Integration
    PostgreSQL Database
    Docker Deployment
    Seller Dashboard
    Product Search & Filtering

## Author
    Nayana Prakash
