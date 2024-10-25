from celery import Celery
from kombu import Queue
celery_app = Celery(
    "worker",
    broker="redis://redis_broker:6379/0",  # Redis broker URL (use the service name `redis_broker`)
    backend="redis://redis_broker:6379/0"  # For storing results, if needed
)

celery_app.conf.task_queues = (
    Queue('high_priority', routing_key='player_queue'),
)

celery_app.conf.update(
    result_expires=3600,
    task_track_started=True,
    broker_connection_retry_on_startup=True,
    task_time_limit=1,
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    task_routes={
        "player.tasks.*": {"queue": "player_queue"},
    }
)
