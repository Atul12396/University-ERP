# Final ERP/Final ERP/ERP/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERP.settings')

app = Celery('ERP')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Final ERP/Final ERP/ERP/celery.py

from celery import Celery
from celery.schedules import crontab

app = Celery('ERP')

app.conf.beat_schedule = {
    'send-payment-reminders-every-day': {
        'task': 'myapp.tasks.send_payment_reminders',
        'schedule': crontab(hour=0, minute=0),
    },
}
