import redis
import config


class CeleryModel(object):
    def __init__(self):
        self.__conn = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.CELERY_REDIS_DB)

    def get_queue_task_count(self, queue_name):
        """
        获取队列的任务书
        :param queue_name:
        :return:
        """
        return self.__conn.llen(queue_name)

    def is_queue_busy(self):
        if self.get_queue_task_count('celery') > 5:
            print('queue busy')
            return True
        return False
