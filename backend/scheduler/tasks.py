from scheduler import celery_app
from utils import refresh_healthcheck_timestamp


@celery_app.task(queue="celerybeat")
def celerybeat_healthcheck():
    """Healthcheck task for Celerybeat monitoring purposes."""
    refresh_healthcheck_timestamp()
