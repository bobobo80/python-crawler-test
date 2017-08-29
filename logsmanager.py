"""
logs 生产者,负责发布logs任务
"""
from tasks.logs import crawl_log
from db.mongoclient import MongoClient

place_id = 10065

if __name__ == '__main__':
    pass
    # 获取未下载的logs
    mdb = MongoClient()
    logs = mdb.get('log-{}'.format(place_id),
                   {'html': {'$exists': False}})
    for log in logs:
        crawl_log.delay(place_id, log['_id'])

