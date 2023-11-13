from datetime import timedelta

from backend import celery_app


@celery_app.task(run_every=(timedelta(seconds=5)), name='hello')
def hello():
    print("Hello there")
