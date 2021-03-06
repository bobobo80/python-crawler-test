"""
游记的操作类
"""
import os
from db.mongoclient import MongoClient


c_prefix = 'logs-' # collection前缀
max_tasks_number = 200

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
        status 1 url存入
               2 html存入本地
               3 解析完成
        """
        if not self.error:
            mdb = MongoClient()
            if self.status == 1:
                # url信息存入
                mdb.insert_or_update('{}{}'.format(c_prefix, self.place_id),
                                     {'_id': self.log_id},
                                     {'_id': self.log_id,
                                      'url': self.url}
                                     )
            elif self.status == 2:
                mdb.update('{}{}'.format(c_prefix, self.place_id),
                           {'_id': self.log_id},
                           {'html': self.html})
            elif self.status == 3:
                mdb.update('{}{}'.format(c_prefix, self.place_id),
                           {'_id': self.log_id},
                           {'title': self.title,
                            'start_time': self.start_time,
                            'days': self.days,
                            'text_content': self.text_content,
                            'total_words': self.total_words,
                            'total_pictures': self.total_pictures,
                            'help_persons': self.help_persons,
                            'keywords': self.keywords,
                            'sentiments': self.sentiments
                            })

    def set_html(self, html):
        """
        设置html，设置状态
        """
        self.html = html
        self.status = 2 # 页面HTML下载完成状态
        self.save()

    def save_html_file(self, html):
        """
        存储html文件到本地
        place_id目录下，直接存
        """
        if (html is not None or html != '') and not self.error:
            # 判断目录是否存在
            if not os.path.isdir('./html_downloads'):
                os.mkdir('./html_downloads')
            if not os.path.isdir('./html_downloads/{}'.format(self.place_id)):
                os.mkdir('./html_downloads/{}'.format(self.place_id))
            with open('./html_downloads/{}/{}.html'.format(self.place_id, self.log_id), 'w') as f:
                f.write(html)
                print('存储成功：', self.url)
            self.status = 2 # 页面HTML下载完成状态
            self.save()

    @staticmethod
    def get_parser_logs(place_id):
        """
        获取place下未解析的logs
        """
        mdb = MongoClient()
        m_results = mdb.get('{}{}'.format(c_prefix, place_id),
                           {'html': {'$exists': True},
                            'title': {'$exists': False}
                           })
        if m_results.count() > max_tasks_number:
            m_results = m_results[:max_tasks_number]
        for item in m_results:
            yield place_id, item['url'], item['html']

    @staticmethod
    def get_download_logs(place_id):
        """
        获取place下未下载的logs
        """
        mdb = MongoClient()
        m_results = mdb.get('{}{}'.format(c_prefix, place_id),
                            {'html': {'$exists': False}})
        if m_results.count() > max_tasks_number:
            m_results = m_results[:max_tasks_number]
        for item in m_results:
            yield place_id, item['_id']





