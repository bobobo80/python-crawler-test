"""
马蜂窝游记爬取工具
根据地点页面爬取的游记链接，爬取具体游记页面内容
"""

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import random
import json
import multiprocessing

from tlog import Tlog
import config
import mdb


crawl_number = 500


def exe_log_crawl(tlog, proxies_list):
    """
    执行游记的抓取
    :param tlog:
    :return:
    """
    # 连接mongodb，读取链接信息
    db = mdb.MfwDB(config.PLACE_ID)
    # time.sleep(1)
    print('start', tlog.log_id)
    tlog.download_content(proxies_list[random.randrange(len(proxies_list))])
    if not tlog.error:
        db.insert_new_log(tlog.to_dict())
        # print('写入数据库', tlog.title)


def get_log_to_crawl():
    """
    根据抓取数量，返回对应的需要抓取的tlog对象
    :return:
    """
    # 连接mongodb，读取链接信息
    db = mdb.MfwDB(config.PLACE_ID)
    return db.get_uncrawl_logs(crawl_number)


if __name__ == '__main__':
    # 连接mongodb，读取链接信息
    db = mdb.MfwDB(config.PLACE_ID)

    # 读取代理池
    with open('proxies.json', 'r') as f:
        proxies_list = json.load(f)

    # 创建进程池
    pool = multiprocessing.Pool(processes=4)

    # just test
    for log in get_log_to_crawl():
        tlog = Tlog(log['url'])
        pool.apply_async(exe_log_crawl, (tlog, proxies_list))

    print('start multiprocess')
    pool.close()
    pool.join()
    print('all processes end')



