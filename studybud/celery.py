import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybud.settings')  # Cambia 'studybud' por el nombre de tu proyecto si es diferente

app = Celery('studybud')  # Cambia 'studybud' por el nombre de tu proyecto si es diferente

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()