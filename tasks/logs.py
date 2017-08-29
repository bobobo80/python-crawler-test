"""
访问游记单页面，下载页面
"""
from .workers import app
from web_get.webget import WebRequest, TimeoutException, ResponseException
from db.travellog import Tlog


@app.task(bind=True)
def crawl_log(self, place_id, log_id):
    """
    爬取游记页面
    :param place_id:
    :return:
    """
    url = 'http://www.mafengwo.cn/i/{}.html'.format(log_id)

    try:
        html = WebRequest().get(url).content.decode('utf-8')
    except (TimeoutException, ResponseException) as exc:
        raise self.retry(countdown=10, exc=exc, max_retries=3)

    tlog = Tlog(url, place_id)
    tlog.set_html(html)
