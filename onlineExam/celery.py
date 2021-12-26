import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineExam.settings')
app = Celery('onlineExam', broker='redis://localhost:6379/1', backend='redis://localhost:6379')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
