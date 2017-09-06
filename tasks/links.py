from .workers import app
from web_get.webget import WebRequest, TimeoutException, ResponseException
from db.taskmodel import TaskData
from db.linksmodel import LinksModel
from mfw_parser.links_parser import parser_link
# from .taskdecorator import check_queue_busy
from db.celerymodel import CeleryModel

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
    except Exception as e:
        # 游记页数不够情况，忽略
        pass


@app.task()
def schedule_download_links(pid=None, pnumber=None):
    """
    随机获取获取链接的place
    """
    if CeleryModel().is_queue_busy():
        return
    if pid:
        place_id = pid
    else:
        place_id = int(TaskData().get_link_place_id())
    if pnumber:
        pages = pnumber
    else:
        pages = 10
    # 根据已有链接数量，再下载新的，获取该地已有links，计算页数开始范围
    links_count = LinksModel.get_place_count(place_id)
    # 首页
    app.send_task('tasks.links.crawl_place_links', args=(place_id, 1))
    # 后续页
    exists_page = links_count // 10
    if exists_page == 0:
        # 抓所有links
        for p in range(2, pages+1):
            app.send_task('tasks.links.crawl_place_links', args=(place_id, p))
    elif exists_page > 0 and exists_page < 299:
        # 抓后续
        for p in range(exists_page, exists_page+pages):
            app.send_task('tasks.links.crawl_place_links', args=(place_id, p))

