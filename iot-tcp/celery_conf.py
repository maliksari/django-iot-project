
import os

from celery import Celery
from dotenv import load_dotenv

from task import save_location_to_db, logger

load_dotenv()


CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

celery_app = Celery('tasks')


celery_app.conf.update(
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


@celery_app.task(bind=True, max_retries=3)
def locations_task(self, device_id, latitude, longitude):
    try:
        save_location_to_db(device_id, latitude, longitude)
    except Exception as e:
        logger.error(f"Error saving location to database: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)
