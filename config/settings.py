from pathlib import Path
import environ

# BASE_DIR 설정
BASE_DIR = Path(__file__).resolve().parent.parent

# 환경 변수 설정
env = environ.Env()
environ.Env.read_env()  # .env 파일 읽기

SECRET_KEY="django-insecure-2(i)nvc1fn%1r71*4l@ca_6!tr7lpk(l23@(v)$8v230(sk8!4"

# DEBUG 모드
DEBUG = True

# ALLOWED_HOSTS 설정
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "yourdomain.com"]

# CORS 설정
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # 프론트엔드의 주소
    "http://localhost:8000",  # 백엔드의 주소
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-requested-with",
    "x-csrftoken",  # CSRF 토큰 지원
    "accept",
    "origin",
]
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

# INSTALLED_APPS 설정
INSTALLED_APPS = [
    # 기본 Django 앱
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 프로젝트 앱
    'apps.toro_auth',  # 사용자 인증 관련 앱

    # 서드파티 앱
    'rest_framework',  # Django REST Framework
    'drf_yasg',         # Swagger 문서
    'corsheaders',      # CORS 지원
]

# MIDDLEWARE 설정
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS 미들웨어
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ROOT_URLCONF 설정
ROOT_URLCONF = 'config.urls'

# TEMPLATES 설정
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

# WSGI 설정
WSGI_APPLICATION = 'config.wsgi.application'

# DATABASE 설정
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'toro_db',
        'USER': 'toro_admin',  # 공백 제거
        'PASSWORD': 'toro_pwd123!',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

# PASSWORD VALIDATORS 설정
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

# 지역화 및 시간대 설정
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# STATIC 설정
STATIC_URL = 'static/'

# 기본 필드 타입 설정
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF 설정
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# EMAIL 설정
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_HOST_USER = env("EMAIL")
    EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD")
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
