import task
import os
from celery import Celery

from dotenv import load_dotenv

load_dotenv()

celery_app = Celery('tcp_server_app')

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

celery_app.conf.update(
    # broker_url='amqp://guest:guest@localhost:5672//',  # RabbitMQ bağlantı URL'si
    # Redis bağlantı URL'si
    # result_backend='redis://redis:6379/0',
    broker_url=CELERY_BROKER_URL,
    result_backend=CELERY_RESULT_BACKEND,
    accept_content=['json'],
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    worker_concurrency=4,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
    task_time_limit=300,
    task_soft_time_limit=240,
    broker_connection_retry_on_startup=True,
)

celery_app.autodiscover_tasks(['task'])
