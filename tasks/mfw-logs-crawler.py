"""
马蜂窝游记爬取工具
根据地点页面爬取的游记链接，爬取具体游记页面内容
"""

import multiprocessing

import config
from db import mongoclient
from db.travellog import Tlog

crawl_number = 3000


def exe_log_crawl(tlog,):
    """
    执行游记的抓取
    :param tlog:
    :return:
    """
    # 连接mongodb，读取链接信息
    # db = mdb.MfwDB(config.PLACE_ID)

    print('start', tlog.log_id)
    # tlog.download_content(proxies_list[random.randrange(len(proxies_list))])
    tlog.download_content()
    # if not tlog.error:
    #     db.insert_new_log(tlog.to_dict())
    # else:
    #     print(tlog.error)


def get_log_to_crawl():
    """
    根据抓取数量，返回对应的需要抓取的tlog对象
    :return:
    """
    # 连接mongodb，读取链接信息
    db = mongoclient.MfwDB(config.PLACE_ID)
    return db.get_uncrawl_logs(crawl_number)


if __name__ == '__main__':
    # 读取代理池
    # with open('proxies.json', 'r') as f:
    #     proxies_list = json.load(f)

    # 创建进程池
    pool = multiprocessing.Pool(processes=8)

    # just test_juptyer
    for log in get_log_to_crawl():
        tlog = Tlog(log['url'], config.PLACE_ID)
        pool.apply_async(exe_log_crawl, (tlog, ))
        # exe_log_crawl(tlog, proxies_list)

    print('start multiprocess')
    pool.close()
    pool.join()
    print('all processes end')



