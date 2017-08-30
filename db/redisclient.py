"""
redis
"""

import redis
import config


class RedisClient(object):
    """
    redis client
    """
    def __init__(self):
        self.db = redis.Redis(host=config.REDIS_HOST,
                              port=config.REDIS_PORT,
                              db=config.REDIS_DB,
                              decode_responses=True)

    def put(self, key_name, fv_dict):
        """
        hmset
        """
        try:
            self.db.hmset(key_name, fv_dict)
        except Exception as e:
            print(e)

    def get(self, key_name, field):
        """
        hget
        """
        try:
            return self.db.hget(key_name, field)
        except Exception as e:
            print(e)

    def get_all(self, key_name):
        """
        hgetall
        """
        try:
            return self.db.hgetall(key_name)
        except Exception as e:
            print(e)

