"""
解析link抓取结果
"""

from bs4 import BeautifulSoup

from db.travellog import Tlog


def parser_link(result, place_id):
    """
    解析link结果,放入数据库
    """
    # 链接的前缀
    prefix_url = 'http://www.mafengwo.cn'

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
                        tlog = Tlog(prefix_url + link['href'], place_id)
                        if not tlog.error:
                            tlog.save()


