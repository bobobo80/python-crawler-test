"""
celery workers 启动文件
"""
from celery import Celery
from kombu import Exchange, Queue

import config


tasks = ['tasks.links']

app = Celery('mfw_task', include=tasks, broker=config.CELERY_BROKER, backend=config.CELERY_BACKEND)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
    celerybeat_schedule={},
    celery_queues=(
        Queue('crawl_place_links', exchange=Exchange('crawl_place_links', type='direct'), routing_key='for_links'),
    ),
)
