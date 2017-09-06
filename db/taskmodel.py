"""
任务用的数据操作
"""
from .redisclient import RedisClient


class TaskData(object):
    def __init__(self):
        self._conn = RedisClient()
        self.raw_places = 'mfw_place_ids'
        self.crawl_places = 'mfw_place_ids'
        self.parser_places = 'mfw_place_ids'
        self.finish_places = 'mfw_place_ids'

    def get_link_place_id(self):
        return self._conn.db.srandmember(self.raw_places)

    def get_crawl_place_id(self):
        """
        随机获取待爬取的place_id
        """
        return self._conn.db.srandmember(self.crawl_places)

    def get_parser_place_id(self):
        return self._conn.db.srandmember(self.parser_places)


