from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://redis_broker:6379/0",  # Redis broker URL (use the service name `redis_broker`)
    backend="redis://redis_broker:6379/0"  # For storing results, if needed
)

celery_app.conf.update(
    task_routes={
        "database.connector.DatabaseConnector.query_get": {"queue": "db_read_queue"},
        "database.connector.DatabaseConnector.query_put": {"queue": "db_write_queue"}
    }
)
