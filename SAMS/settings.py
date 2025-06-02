import os
from pathlib import Path
import dj_database_url # Add this import for production database settings (if you use PostgreSQL on Render)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key_for_dev') # Use environment variable for production

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True' # Use environment variable for DEBUG

ALLOWED_HOSTS = ['sams-wef5.onrender.com', '127.0.0.1', 'localhost'] # Add your Render domain and any other allowed hosts

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'members',
    # Add WhiteNoise to INSTALLED_APPS
    'whitenoise.runserver_nostatic', # Only if you want WhiteNoise to handle static files in development (optional but useful)
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Add WhiteNoiseMiddleware directly after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SAMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates',
                 BASE_DIR / 'core/templates'
                 ],
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

WSGI_APPLICATION = 'SAMS.wsgi.application'

# COMPRESS_PRECOMPILERS = ( # This might be conflicting with WhiteNoise or not needed if you compile CSS locally
#     ('text/x-scss', 'django_libsass.SassCompiler'),
# )


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# For Render PostgreSQL (if you switch from SQLite)
# DATABASE_URL = os.environ.get('DATABASE_URL')
# if DATABASE_URL:
#     DATABASES['default'] = dj_database_url.parse(DATABASE_URL)


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # This is correct

# Configure WhiteNoise to compress and cache static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# If you have static files outside of your app's 'static' folders (e.g., a top-level 'static' folder)
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "members.CustomUser"

# SECURITY SETTINGS (Crucial for production)
# These should generally be True in production, but you might need to adjust based on your specific Render setup.
# Render typically handles HTTPS, so SECURE_PROXY_SSL_HEADER and SECURE_SSL_REDIRECT might be managed by them.

CORS_REPLACE_HTTPS_REFERER = True # Generally True in production
HOST_SCHEME = "https://" # Use HTTPS in production
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # Render might automatically set this up
SECURE_SSL_REDIRECT = True # Redirect HTTP to HTTPS in production
SESSION_COOKIE_SECURE = True # Ensure session cookies are sent over HTTPS
CSRF_COOKIE_SECURE = True # Ensure CSRF cookies are sent over HTTPS
SECURE_HSTS_SECONDS = 31536000 # 1 year - enables HTTP Strict Transport Security
SECURE_HSTS_INCLUDE_SUBDOMAINS = True # Apply HSTS to subdomains
SECURE_FRAME_DENY = True # Prevents clickjacking (can be False if you need iframes from your domain)
