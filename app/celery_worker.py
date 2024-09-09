from celery import Celery

celery_app = Celery('tasks', broker='redis://172.30.125.249:6379/0')
