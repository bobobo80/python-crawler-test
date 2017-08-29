"""
根据爬取的游记内容信息，分析其中的情感信息
"""
import jieba.analyse
from snownlp import SnowNLP

import config
from db import mongoclient


def cal_content_avg_sentiments(sentences):
    """
    根据给定的句子list，计算每句的sentiments，计算平均数返回
    :param sentences:
    :return: 平均数结果
    """
    list_sentiments = [SnowNLP(sentence).sentiments for sentence in sentences]
    if len(list_sentiments) == 0:
        return -1
    else:
        return sum(list_sentiments) / len(list_sentiments)


if __name__ == '__main__':
    db = mongoclient.MfwDB(config.PLACE_ID)

    # 查找有内容，但没有关键词的
    logs = db.logs_col.find({'text_content': { '$exists': True },
                             'keywords': {'$exists': False}}, limit=5000)
    for log in logs:
        print(log['title'])
        try:
            s = SnowNLP(log['text_content'])
            # print('Keywords:', s.keywords(10))
            sentiments = cal_content_avg_sentiments(s.sentences)
            # jieba
            keywords = jieba.analyse.extract_tags(log['text_content'])
            # 写入db
            db.insert_new_log({'id': log['id'],
                               'keywords': keywords,
                               'sentiments': sentiments})
        except Exception as e:
            # 暂不处理
            pass
