import pymongo


class MfwDB(object):
    def __init__(self, place_id):
        """
        初始化mongodb的连接等
        """
        self.client = pymongo.MongoClient()
        self.db = self.client.mfw_crawler
        self.collection = self.db['logs-'+str(place_id)]

    def insert_new_post(self, insert_dict):
        """
        插入新doc
        :param insert_dict: 要插入的dict类型的对象
        :return:
        """
        if isinstance(insert_dict, dict):
            result = self.collection.insert_one(insert_dict)
