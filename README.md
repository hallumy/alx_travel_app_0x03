# Alx Travel App Setup Guide

## Objective

This guide outlines the steps to set up a Django project for the "Alx Travel App" with the necessary dependencies, configure the database, and add Swagger for API documentation.

---

## Instructions

### 1. **Create a Django Project**

#### Set up the Django Project
Create a new Django project named `alx_travel_app`.

    django-admin startproject alx_travel_app

Create an App within the Project

Inside the alx_travel_app project, create an app named listings:

    cd alx_travel_app
    python manage.py startapp listings

Install Necessary Packages

Install the required dependencies using pip.

    pip install django djangorestframework django-cors-headers celery rabbitmq drf-yasg

Make sure that you're in a virtual environment (optional but recommended).

### 2. **Configure Settings**

#### Configure for REST Framework and CORS Headers

Open settings.py and add 'rest_framework' and 'corsheaders' to the INSTALLED_APPS:

    INSTALLED_APPS = [
        'rest_framework',
        'corsheaders',
        'listings', 
    ]

Add CORS middleware to the MIDDLEWARE list in settings.py:

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
    ]


Set up the Database Configuration for MySQL

Install mysqlclient for connecting to a MySQL database:

    pip install mysqlclient

Use the django-environ package to handle database credentials securely. Install django-environ:

    pip install django-environ

In settings.py, add the following lines at the top to load environment variables:

    import environ

    # Initialize environment variables
    env = environ.Env()
    environ.Env.read_env()  

    # Database configuration
    DATABASES = {
        'default': env.db(),
    }


3. Add Swagger Documentation
Install drf-yasg

Install the drf-yasg package for Swagger API documentation:

    pip install drf-yasg

Configure Swagger for Auto Documentation

Open urls.py and add the following configuration to enable Swagger documentation:

    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from django.urls import path

    # Set up Swagger schema view
    schema_view = get_schema_view(
        openapi.Info(
            title="Alx Travel API",
            default_version='v1',
            description="API documentation for the Alx Travel Project",
            contact=openapi.Contact(email="contact@alxtravel.com"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    ]

This will make the Swagger UI available at http://localhost:8000/swagger/ once you run the server.
