"""
使用requests包装的页面请求
"""
import requests

from .headers import Headers
from proxy import proxy


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
            if resp.status_code == 200:
                return resp
        except Exception as e:
            self.delete_proxy()
            print(e)

    def post(self, url, payload):
        """
        页面post
        """
        try:
            resp = requests.post(url, data=payload, headers=self.headers,
                                 proxies={'http': 'http://{}'.format(self.proxies)},
                                 timeout=10)
            if resp.status_code == 200:
                return resp
        except Exception as e:
            self.delete_proxy()
            print(e)

    def delete_proxy(self):
        proxy.delete_proxy(self.proxies)
