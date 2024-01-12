import json
from .base import *

BASE_DIR = Path(__file__).resolve().parent.parent

CSRF_TRUSTED_ORIGINS = [
    "http://0.0.0.0:8000",
    "http://127.0.0.1:8000",
]
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_NAME", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

SITE_ID = int(os.environ.get("SITE_ID", 1))
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

ALLOWED_HOSTS = ["127.0.0.1", os.environ.get("HOST_URL", "127.0.0.1")]
DEBUG = os.environ.get("DJANGO_DEBUG", False)
SECRET_KEY = os.environ.get("SECRET_KEY")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")
CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:5173", "http://localhost:5173"]
