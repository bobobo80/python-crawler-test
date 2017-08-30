"""
celery workers 启动文件
"""
from celery import Celery
from kombu import Exchange, Queue
from datetime import timedelta

import config


tasks = ['tasks.links', 'tasks.logs']

app = Celery('mfw_task', include=tasks, broker=config.CELERY_BROKER, backend=config.CELERY_BACKEND)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
    beat_schedule={
        'log_parser': {
            'task': 'tasks.logs.schedule_parser_logs',
            'schedule': 60,
        },
    },
    celery_queues=(
        Queue('links_queue', exchange=Exchange('links_queue', type='direct'), routing_key='for_links'),
        Queue('logs_queue', exchange=Exchange('logs_queue', type='direct'), routing_key='for_logs'),
    ),
)
