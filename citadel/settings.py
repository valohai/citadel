import hashlib
import os

from environ import Env
from jwt.utils import force_bytes

env = Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = env.bool("DEBUG", default=False)
SECRET_KEY = env.str("SECRET_KEY", default=("x" if DEBUG else Env.NOTSET))
JWT_KEY = env.str("JWT_KEY", default=hashlib.sha256(force_bytes(SECRET_KEY)).hexdigest())
ALLOWED_HOSTS = ["*"]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
VAR_ROOT = env.str("VAR_ROOT", default=os.path.join(BASE_DIR, "var"))
os.makedirs(VAR_ROOT, exist_ok=True)
STATIC_URL = "/static/"
STATIC_ROOT = env.str("STATIC_ROOT", default=os.path.join(VAR_ROOT, "static"))
MEDIA_URL = "/media/"
MEDIA_ROOT = env.str("MEDIA_ROOT", default=os.path.join(VAR_ROOT, "media"))
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_NAME = "citadel_session"
X_FRAME_OPTIONS = "SAMEORIGIN"
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "citadel",
    "cicore",
    "cifront",
    "civote",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "citadel.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "citadel.wsgi.application"

DATABASES = {
    "default": env.db_url(default="sqlite:///%s" % os.path.join(VAR_ROOT, "citadel.sqlite3")),
}

AUTH_PASSWORD_VALIDATORS = []
