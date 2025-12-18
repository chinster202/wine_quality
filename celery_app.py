from celery import Celery
import fastapi_test

celery_app = Celery(
    'celery_app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)
celery_app.autodiscover_tasks(['tasks'])
celery_app.conf.timezone = 'UTC'

celery_app.conf.beat_schedule = {
    'run-fastapi-test-every-1-minute': {
        'task': 'tasks.get_predictions_task',
        'schedule': 60.0,  # every 1 minute
    },
}