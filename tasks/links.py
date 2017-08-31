from .workers import app
from web_get.webget import WebRequest, TimeoutException, ResponseException
from db.taskmodel import TaskData
from mfw_parser.links_parser import parser_link

@app.task(bind=True)
def crawl_place_links(self, place_id, page_number):
    """
    爬取某地点的游记链接
    :param place_id:
    :return:
    """
    # 游记的ajax api
    url = 'http://www.mafengwo.cn/gonglve/ajax.php?act=get_travellist'
    # 链接的前缀
    prefix_url = 'http://www.mafengwo.cn'

    # 初始list
    log_list = []

    payload = {
        'mddid': place_id,
        'pageid': 'mdd_index',
        'sort': 1,
        'cost': 0,
        'days': 0,
        'month': 0,
        'tagid': 0,
        'page': page_number
    }

    try:
        result = WebRequest().post(url, payload)
        if result:
            parser_link(result.json(), place_id)
    except (TimeoutException, ResponseException) as exc:
        raise self.retry(countdown=10, exc=exc, max_retries=5)


@app.task()
def schedule_download_links(pid=None, pnumber=None):
    """
    随机获取获取链接的place
    """
    if pid:
        place_id = pid
    else:
        place_id = int(TaskData().get_link_place_id())
    if pnumber:
        pages = pnumber
    else:
        pages = 10
    for p in range(1, pages):
        app.send_task('tasks.links.crawl_place_links', args=(place_id, p))

