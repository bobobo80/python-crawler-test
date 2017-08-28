"""
使用proxy_pool获取和删除代理
"""
import requests


PROXY_URL = 'http://127.0.0.1:5000/'


def get_proxy():
    """
    使用proxy_pool获取代理ip
    :return:
    """
    return requests.get(PROXY_URL+'get/').text


def delete_proxy(proxy):
    """
    删除无法使用proxy
    :param proxy:
    :return:
    """
    # proxy = proxy.split('http://')[1]
    requests.get(PROXY_URL+'delete/?proxy={}'.format(proxy))
    print('delete proxy: {}'.format(proxy))
