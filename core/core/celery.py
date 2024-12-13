from celery import Celery

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_connection_retry = True
app.conf.broker_connection_max_retries = 5
app.conf.broker_connection_retry_on_startup = True
