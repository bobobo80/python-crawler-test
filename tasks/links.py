from .workers import app
from web_get.webget import WebRequest

from mfw_parser.links_parser import parser_link

@app.task()
def crawl_place_links(place_id, page_number):
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

    result = WebRequest().post(url, payload)
    if result:
        return parser_link(result.json(), place_id)
    else:
        return False

