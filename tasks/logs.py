"""
访问游记单页面，下载页面
"""
from .workers import app
from web_get.webget import WebRequest, TimeoutException, ResponseException
from db.travellog import Tlog
from db.taskmodel import TaskData
from mfw_parser import log_parser


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


@app.task()
def schedule_download_logs(input_pid=None):
    """
    随机获取待下载的place_id, 下载其中未下载的游记
    """
    if input_pid:
        place_id = input_pid
    else:
        place_id = int(TaskData().get_crawl_place_id())
    for pid, log_id in Tlog.get_download_logs(place_id):
        app.send_task('tasks.logs.crawl_log', args=(pid, log_id))


@app.task()
def schedule_parser_logs(input_pid=None):
    """
    随机获取待解析的place_id, 解析其中的logs
    """
    if input_pid:
        pid = input_pid
    else:
        pid = int(TaskData().get_parser_place_id())
    # 获取place下未解析的logs链接
    for pid, url, html in Tlog.get_parser_logs(pid):
        app.send_task('tasks.logs.parser_log', args=(pid, url, html))


@app.task(ignore_result=True)
def parser_log(place_id, url, html):
    """
    解析指定的log
    """
    log_parser.parser_log(place_id, url, html)

