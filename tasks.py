from celery_app import celery_app
from fastapi_test import main

@celery_app.task(name="tasks.get_predictions_task")
def get_predictions_task():
    main()