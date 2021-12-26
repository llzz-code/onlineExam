from onlineExam.celery import app
from celery import shared_task
import time

@shared_task
def waste_time():
    time.sleep(3)
    return 'waste_time finshed'
