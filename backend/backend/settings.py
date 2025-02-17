import os
from pathlib import Path

# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1Qz3wHkJA5EyXwQxPSZpLD_e8zQ8-JGliRyWEHdknj1FKyFzl0UFV7oS2vnrZycSJnE'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Set to False in production

ALLOWED_HOSTS = []  # Add your domain or IP when deploying

# APPLICATIONS INSTALLED
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    "debug_toolbar",
    
    # Add your custom apps here
    'caseconnect',  # Replace with your actual app name
    'corsheaders',  # For handling CORS
]

# MIDDLEWARE (Ensure everything is present)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',  #for CORS
    'django.middleware.common.CommonMiddleware',
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]
CORS_ALLOW_ALL_ORIGINS = True


INTERNAL_IPS = [
    "127.0.0.1",
]

# ROOT URL CONFIGURATION
ROOT_URLCONF = 'backend.urls'  # Change 'backend' if your project folder is named differently

# TEMPLATES CONFIGURATION
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Add a templates directory if needed
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI CONFIGURATION
WSGI_APPLICATION = 'backend.wsgi.application'  # Change 'backend' if your project folder is different

# DATABASE CONFIGURATION (PostgreSQL example, change if using SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'case_connect',  # Replace with your PostgreSQL database name
        'USER': 'postgres',  # Replace with your PostgreSQL username
        'PASSWORD': 'aditya@123',  # Replace with your PostgreSQL password
        'HOST': 'localhost',  # Change if using a remote DB
        'PORT': '5432',  # Default PostgreSQL port
    }
}

# PASSWORD VALIDATION (Default settings)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNATIONALIZATION SETTINGS
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC FILES (Ensure STATIC_URL is defined)
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",  # This ensures Django knows where to look for static files
]

# MEDIA FILES (For user-uploaded files, if needed)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# DEFAULT AUTO FIELD (Avoids warnings in Django 3.2+)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Allow frontend to communicate with backend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5500",
    "http://localhost:8000",  # Update this with your frontend URL
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}





LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'django_security.log',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_KEY="1Qz3wHkJA5EyXwQxPSZpLD_e8zQ8-JGliRyWEHdknj1FKyFzl0UFV7oS2vnrZycSJnE"

DB_PASSWORD = os.getenv("DB_PASSWORD")
