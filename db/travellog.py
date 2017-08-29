"""
游记的操作类
"""
from db.mongoclient import MongoClient


class Tlog(object):
    """
    自定义游记类，暂时就是参数信息
    """
    def __init__(self, url, place_id):
        self.url = url
        self.error = None
        self.place_id = place_id
        self.status = 0
        # 由url解析id
        try:
            log_id = url.split('/i/')[1]
            # 去掉.html
            log_id = log_id.split('.')[0]
            self.log_id = int(log_id)
        except IndexError:
            self.error = 'Url format is wrong.'
        except ValueError:
            self.error = 'Log id format is wrong.'
        self.status = 1

    def save(self):
        """
        将当前状态的log信息存入数据库
        """
        if not self.error:
            mdb = MongoClient()
            if self.status == 1:
                # url信息存入
                mdb.insert_or_update('log-{}'.format(self.place_id),
                                     {'_id': self.log_id},
                                     {'_id': self.log_id,
                                      'url': self.url}
                                     )




