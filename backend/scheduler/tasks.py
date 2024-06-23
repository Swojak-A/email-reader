from scheduler import celery_app
from utils import refresh_healthcheck_timestamp


@celery_app.task(
    bind=True,
    track_started=True,
    queue="celerybeat",
    name="celerybeat_healthcheck",
)
def celerybeat_healthcheck(self):
    """Healthcheck task for Celerybeat monitoring purposes."""
    refresh_healthcheck_timestamp()
