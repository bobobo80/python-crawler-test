"""
log解析
"""
from bs4 import BeautifulSoup
import datetime

from db.travellog import Tlog


def parser_log(place_id, url, html):
    """
    解析html页面内容
    """
    if html is None:
        return
    tlog = Tlog(url, place_id)
    tlog.html = html
    # 使用bs解析
    html_bs_obj = BeautifulSoup(tlog.html, 'lxml')
    try:
        # 大标题
        tlog.title = html_bs_obj.select('h1')[0].text.strip()
        # 文字内容
        # 两种content class va_con or a_con_text
        if html_bs_obj.find(class_='va_con'):
            tlog.text_content = html_bs_obj.find(class_='va_con').text
        elif html_bs_obj.find(class_='a_con_text'):
            tlog.text_content = html_bs_obj.find(class_='a_con_text').text
        else:
            raise AttributeError
        tlog.text_content = ''.join(tlog.text_content.split())
        print('已抓取:', tlog.title)
    except IndexError:
        tlog.error = 'Parse content error. Index out of range.'
    except AttributeError:
        tlog.error = 'Parse content error. No attribute.'
    # 如果时间，天数等非必要参数问题，可以忽略,使用标记值
    try:
        # 出发时间
        start_time = html_bs_obj.select('.time')[0].text.split(r'/')[1]
        # 转datetime
        tlog.start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    except:
        tlog.start_time = datetime.datetime(1900, 1, 1, 0, 0)
    try:
        # 出行天数
        days = html_bs_obj.select('.day')[0].text.split(r'/')[1]
        # 转int
        tlog.days = int(days.split('天')[0])
    except:
        tlog.days = -1
    tlog.save()