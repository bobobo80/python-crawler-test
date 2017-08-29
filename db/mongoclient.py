"""
mongodb连接，查询，写入的操作类
"""

import pymongo
import config


class MongoClient(object):
    def __init__(self):
        """
        初始化mongodb的连接等
        """
        self.client = pymongo.MongoClient(config.MONGO_HOST, config.MONGO_PORT)
        self.db = self.client[config.MONGO_DBNAME]
        # self.logs_col = self.db['logs-'+str(place_id)]
        # print('初始化mongodb连接')

    def insert(self, col_name, insert_dict):
        """
        插入新内容
        :param col_name:
        :param insert_dict:
        :return:
        """
        try:
            self.db[col_name].insert(insert_dict)
            print('insert {} record'.format(col_name))
        except Exception as e:
            print(e)

    def update(self, col_name, key, update_dict):
        """
        :param col_name:
        :param key: {"_id": 12312}
        :param update_dict:  {'$set": {update_dict}}
        :return:
        """
        try:
            self.db[col_name].update_one(key, {'$set': update_dict})
            print('update {} record'.format(col_name))
        except Exception as e:
            print(e)

    def insert_or_update(self, col_name, key, update_dict):
        """
        if key exist, update, else insert
        """
        if self.get(col_name, key).count():
            self.update(col_name, key, update_dict)
        else:
            self.insert(col_name, update_dict)

    def get(self, col_name, search_key):
        """
        获取内容
        :param col_name:
        :param get_dict:
        :return:
        """
        try:
            return self.db[col_name].find(search_key)
        except Exception as e:
            print(e)


