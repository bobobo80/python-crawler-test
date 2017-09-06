from .mongoclient import MongoClient

c_prefix = 'logs-' # collection前缀

class LinksModel(object):
    """
    links的数据库相关操作
    """
    @staticmethod
    def get_place_count(place_id):
        """
        获取某地已有的含url的数量
        """
        mdb = MongoClient()
        return mdb.db[c_prefix+str(place_id)].find().count()
