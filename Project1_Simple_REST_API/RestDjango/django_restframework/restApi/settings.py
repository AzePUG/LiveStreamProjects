"""
Django settings for restApi project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from django.conf import settings
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/


'''
Securty key designed for PasswordResetView tokens,  usage of cryptographic signing, unless a different key is provided. There are many things in a Django app which require a cryptographic signature, and the ‘SECRET_KEY’ setting is the key used for those.
'''
# Django automatically hides settings if they contain any of the following words:
# API
# TOKEN 
# KEY
# SECRET
# PASS
# SIGNATURE 

SECRET_KEY = os.getenv("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
'''
Django addresses this through the get_host() method of django.http.HttpRequest. This method validates the requested host header against the hosts listed in the ALLOWED_HOSTS settings. If the host does not match then a SuspiciousOperation exception will be thrown.
'''
ALLOWED_HOSTS = ["*"]


# Application definition
'''
django uses INSTALLED_APPS as a list of all of the places to look for models, 
management commands, tests, and other utilities.
'''
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "api.apps.MyAppConfig",
    "rest_framework",

    
]
# rest_framework_simplejwt.token_blacklist  
# for more about black list: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/blacklist_app.html

#JWT stand for JSON Web Token and it is an authentication strategy used by client/server applications where the client is a Web application using JavaScript and some frontend framework like Angular, React or VueJS.The JWT is acquired by exchanging an username + password for an access token and an refresh token.
SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True, #When set to True, if a refresh token is submitted to the TokenRefreshView, a new refresh token will be returned along with the new access token. 
    'BLACKLIST_AFTER_ROTATION': True, #refresh tokens submitted to the TokenRefreshView to be added to the blacklist 

    'ALGORITHM': 'HS256', #TWO types either HMAC  or RSA for HMAC 'HS256', 'HS384', 'HS512: SIGNING_KEY setting will be used as both the signing key and the verifying key.  asymmetric RSA RS256', 'RS384', 'RS512' SIGNING_KEY setting must be set to a string that contains an RSA private key. Likewise, the VERIFYING_KEY
    'SIGNING_KEY': settings.SECRET_KEY, #content of generated tokens.
    'VERIFYING_KEY': None, #The verifying key which is used to verify the content of generated tokens
    'AUDIENCE': None, #The audience claim to be included in generated tokens and/or validated in decoded tokens
    'ISSUER': None, #ssuer claim to be included in generated tokens 

    'AUTH_HEADER_TYPES': ('Bearer',), #Authorization: Bearer <token> ('Bearer', 'JWT')
    'USER_ID_FIELD': 'id', #The database field from the user model that will be included in generated tokens to identify users.
    'USER_ID_CLAIM': 'user_id', #value of 'user_id' would mean generated tokens include a “user_id” claim that contains the user’s identifier.

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type', #The claim name that is used to store a token’s type

    'JTI_CLAIM': 'jti', #The claim name that is used to store a token’s unique identifier.
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  #which specifies how long access tokens are valid
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1), # how long refresh tokens are valid.
}


#rest framework config
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

'''
At its core, Django takes an HTTP request (sent to the Web server) and turns it into an HTTP response (sent from the server back to the browser).
This is usually done via Views and Templates. Middleware provides a way to consistently process the requests or the responses on a global level without having to customize every view. It can either work on the requests or on the response objects depending on where in the lifecycle it operates. 
Order of middlewares is important.
A middleware only need to extend from class object.
'''
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'restApi.urls'

'''
django ships built-in backends
'''
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', 
        #BACKEND is a dotted Python path to a template engine class implementing Django’s template backend API. The built-in backends are django.template.backends.django.DjangoTemplates and django.template.backends.jinja2.Jinja2.
    #The template backend to use. The built-in template backends are:

# 'django.template.backends.django.DjangoTemplates'
# 'django.template.backends.jinja2.Jinja2'

        'DIRS': [os.path.join(BASE_DIR,"templates")], 
        #DIRS defines a list of directories where the engine should look for template source files, in search order.

        'APP_DIRS': True, 
        #APP_DIRS tells whether the engine should look for templates inside installed applications. Each backend defines a conventional name for the subdirectory inside applications where its templates should be stored.
 
        #Extra parameters to pass to the template backend. Available parameters vary depending on the template backend. See DjangoTemplates and Jinja2 for the options of the built-in backends.
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

'''
Any server you set up has to know where the WSGI file is. If you're using an external server it will look in its own settings. If you're using Django's development server, it will check Django's settings. So the circularity you noticed is a consequence of the fact that the Django application can be started in a number of different ways.

'''
WSGI_APPLICATION = 'restApi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
'''
Django officially supports the following databases:
PostgreSQL
MariaDB
MySQL
Oracle
SQLite
'''
if DEBUG:
    
    DATABASES = {
        
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }}

#PROD DB
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASS'),
            'HOST': os.environ.get('HOST'),
            'PORT': '5432',
        }
    }



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
'''
Users often attempts poor passwords. To ignore this problem, Django offers pluggable password validation
'''
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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'


LOG_LEVEL = 'ERROR' if DEBUG else 'DEBUG'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': not DEBUG,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:=> %(message)s',
        },
        'focused': {
            'format': '\n----------------------\n%(asctime)s [%(levelname)s] %(name)s:=> %(message)s \n----------------------',
        },
    },
}
