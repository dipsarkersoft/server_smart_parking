

from pathlib import Path
import psycopg2
from dotenv import load_dotenv
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x_5k-pk3il_x=&3oq&#h@99!n)i!w$1izra=3t-(ifeon4_s)i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app","*"]






CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'x-csrftoken',
    'accept',
    'origin',
]

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'category',
    'profiles',
    'Parking',
]


CORS_ALLOWED_ORIGINS = [
    "https://front-parking.vercel.app",
    "http://localhost:5173",
]

CSRF_TRUSTED_ORIGINS = [
   "https://backend-parking-p4dd.onrender.com",
   "https://server-smart-parking.vercel.app/",
   "http://127.0.0.1:8000",
   "https://front-parking.vercel.app",
    "http://localhost:5173",
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  
    'django.middleware.common.CommonMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
       
         'rest_framework.authentication.BasicAuthentication',
         'rest_framework.authentication.TokenAuthentication',
       
    ],
    
    
}




ROOT_URLCONF = 'ParkingBackend.urls'
MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ParkingBackend.wsgi.app'



# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# import dj_database_url
# DATABASES = {
#     'default': dj_database_url.parse(
#         os.getenv("DB_URL_AIVEN"),
        
#         ssl_require=True
#     )
# }


DATABASES = {
    'default': {
        'ENGINE':"django.db.backends.postgresql",
        'NAME':"postgres",
        'USER':os.getenv("DB_USER"),
        'PASSWORD':os.getenv("DB_PASS"),
        'HOST':"aws-0-ap-south-1.pooler.supabase.com",
        'PORT':os.getenv("DB_PORT"),
        'OPTIONS': {
            'sslmode': 'require'  
        },
    }
}




# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_TZ = True

LANGUAGE_CODE = 'en-us'  
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True  
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT=BASE_DIR/'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
