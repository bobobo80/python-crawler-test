"""
使用requests包装的页面请求
"""
import requests

from .headers import Headers
from proxy import proxy


class TimeoutException(Exception):
    """
    连接超时异常
    """
    pass


class ResponseException(Exception):
    """
    响应异常
    """
    pass


class WebRequest(object):
    """
    包装requests
    """
    def __init__(self):
        self.headers = Headers().get()
        self.proxies = proxy.get_proxy()

    def get(self, url):
        """
        页面请求
        """
        try:
            resp = requests.get(url, headers=self.headers,
                                proxies={'http': 'http://{}'.format(self.proxies)}, timeout=10)
            return self.check_response(resp)
        except Exception as e:
            self.network_error(e)

    def post(self, url, payload):
        """
        页面post
        """
        try:
            resp = requests.post(url, data=payload, headers=self.headers,
                                 proxies={'http': 'http://{}'.format(self.proxies)},
                                 timeout=10)
            return self.check_response(resp)
        except Exception as e:
            self.network_error(e)

    def network_error(self, e):
        proxy.delete_proxy(self.proxies)
        print('error: {}'.format(e))
        raise TimeoutException('timeout')

    def check_response(self, resp):
        """
        检查响应
        :param resp:
        :return:
        """
        if resp.status_code == 200:
            return resp
        else:
            raise ResponseException('response status error: {}'.format(resp.status_code))
