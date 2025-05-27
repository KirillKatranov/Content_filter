# celery_app.py

import sys
from celery import Celery
import os
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

broker = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery = Celery("Content_filter", broker=broker, backend=broker)
celery.conf.timezone = "Europe/Moscow"
print("Текущая рабочая директория:", os.getcwd())
celery.autodiscover_tasks(["tasks"])  # <== папка с задачами

from celery.schedules import crontab

celery.conf.beat_schedule = {
    "send-every-30-min": {
        "task": "tasks.task.send_filtered_news",  # <== путь до задачи
        "schedule": crontab(minute="*/30"),
    }
}