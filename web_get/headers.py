"""
使用fake user agent获取UserAgent, 设置headers
"""
import random
import fake_useragent
from db.redisclient import RedisClient


class Headers(object):
    """
    供web request获取headers
    """
    def __init__(self):
        """
        从redis中获取保存的ua值，如果没有，则新下载
        """
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
        }
        rc = RedisClient()
        self.ua_dict = rc.get_all('useragents')
        while not self.ua_dict:
            Headers.set_ua_from_fua()
            self.ua_dict = rc.get_all('useragents')

    # def __getattr__(self, item):
    #     """
    #     用于直接获取某个ua
    #     :param item:
    #     :return: 如果有对应浏览器agent，返回。没有则返回默认的chrome agent
    #     """
    #     if item in self.ua_dict:
    #         return self.ua_dict[item]
    #     else:
    #         return random.choice(self.ua_dict.values())

    def get(self):
        self.headers['User-Agent'] = random.choice(list(self.ua_dict.values()))
        return self.headers

    @staticmethod
    def set_ua_from_fua():
        """
        从fake user agent获取ua信息
        """
        ua = fake_useragent.UserAgent()
        ua_dict = {
            'chrome': ua.chrome,
            'ie': ua.ie,
            'opera': ua.opera,
            'firefox': ua.firefox,
            'safari': ua.safari,
        }
        rc = RedisClient()
        rc.put('useragents', ua_dict)


if __name__ == '__main__':
    pass
