import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from tlog import Tlog
import config


def init_session():
    '''
    访问首页，初始化session
    return 初始化后的session
    '''
    session = requests.Session()
    # 设置fake-agent
    ua = UserAgent()
    headers = {
        'user-agent': ua.chrome
    }
    url = 'http://www.mafengwo.cn/travel-scenic-spot/mafengwo/' + str(config.PLACE_ID) + '.html'
    session.get(url, headers=headers)
    return session


def get_place_log_list(session):
    """
    通过游记ajax api，获取所有游记的链接
    return 游记链接地址list
    """
    # 游记的ajax api
    url = 'http://www.mafengwo.cn/gonglve/ajax.php?act=get_travellist'
    # 链接的前缀
    prefix_url = 'http://www.mafengwo.cn'

    # 初始list
    log_list = []

    # 设置参数
    page_number = 1

    payload = {
        'mddid': config.PLACE_ID,
        'pageid': 'mdd_index',
        'sort': 1,
        'cost': 0,
        'days': 0,
        'month': 0,
        'tagid': 0,
        'page': page_number
    }
    # 循环叠加page_number, 获取所有页的游记链接
    for p_number in range(1, 5):
        payload['page'] = p_number

        # post请求 TODO: try
        r = session.post(url, data=payload)

        # 解析结果，获取游记列表
        result = r.json()
        if result['msg'] == 'succ':
            log_content = result['list']
            # 检查list是否有内容
            log_bs_obj = BeautifulSoup(log_content, 'lxml')
            # 筛掉广告文章，广告链接含有tn-item-sales class属性
            log_item_list = log_bs_obj.find_all(class_='tn-item clearfix')
            if len(log_item_list) > 0:
                # 循环item list
                for item in log_item_list:
                    link_list = item.select('.tn-wrapper')[0].select('dt > a')
                    # 筛掉宝藏app链接等，游记链接不含class属性
                    for link in link_list:
                        if not link.has_attr('class'):
                            log_list.append(Tlog(link.text, prefix_url + link['href']))
    return log_list


def save_link_to_file(log_list):
    """
    存游记链接的结果到文件
    :param log_list:
    :return:
    """
    with open('link_list.txt', 'w') as f:
        for log in log_list:
            f.write("{0}^{1}\n".format(log.title, log.url))


if __name__ == '__main__':
    session = init_session()
    log_list = get_place_log_list(session)

    for log in log_list:
        print(log.title, log.url)

    save_link_to_file(log_list)