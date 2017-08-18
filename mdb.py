"""
mongodb连接，查询，写入的操作类
"""

import pymongo


class MfwDB(object):
    def __init__(self, place_id):
        """
        初始化mongodb的连接等
        """
        self.client = pymongo.MongoClient()
        self.db = self.client.mfw_crawler
        self.place_id = place_id
        self.logs_col = self.db['logs-'+str(place_id)]
        # print('初始化mongodb连接')

    def insert_link(self, insert_dict):
        """
        插入新的游记地址
        如果已含有id，则不添加
        """
        # 查询id
        if not self.logs_col.find_one({'id': insert_dict['id']}):
            self.logs_col.insert_one(insert_dict)
            print('插入新link记录')

    def insert_new_log(self, insert_dict):
        """
        插入新doc
        :param insert_dict: 要插入的dict类型的对象
        :return:
        """
        if isinstance(insert_dict, dict):
            # result = self.logs_col.insert_one(insert_dict)
            result = self.logs_col.update_one({'id': insert_dict['id']}, {'$set': insert_dict})
            print('插入新游记log记录')

    def get_uncrawl_logs(self, number):
        """
        获取未被爬取的log url
        :param number: 所需数量
        :return:
        """
        return self.logs_col.find({'html': { '$exists': False }}, limit=number)
