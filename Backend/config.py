import os
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv


load_dotenv(
    os.environ.get("PPA_ENV_FILE") or str(Path(__file__).resolve().parents[3] / ".env"),
    override=False,
)



class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///placement_db.db"
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/1")
    RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")

    BEAT_SCHEDULE = {
        "daily-reminders": {
            "task": "tasks.send_daily_reminders",
            "schedule": crontab(hour=9, minute=0),
            "options": {"queue": "celery"},
        },
        "monthly-activity-report": {
            "task": "tasks.send_monthly_activity_report",
            "schedule": crontab(day_of_month=1, hour=9, minute=0),
            "options": {"queue": "celery"},
        },
    }

    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    CACHE_DEFAULT_TIMEOUT = 60

    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = os.environ.get("MAIL_PORT", 587)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", True)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
