"""
log解析
"""
from bs4 import BeautifulSoup
import datetime
import jieba.analyse
from snownlp import SnowNLP

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
    # 字数,图片
    try:
        total_obj = html_bs_obj.find(class_='vc_total')
        tlog.total_words, tlog.total_pictures = total_obj.find_all('span')
        tlog.help_persons = total_obj.find(class_='_j_total_person').text
        if tlog.total_words.text == '':
            tlog.total_words = len(tlog.text_content)
        else:
            tlog.total_words = int(tlog.total_words.text)
        if tlog.total_pictures.text == '':
            # 使用bs统计图片
            tlog.total_pictures = len(html_bs_obj.find_all('div', class_='add_pic'))
        else:
            tlog.total_pictures = int(tlog.total_pictures.text)
        if tlog.help_persons == '':
            tlog.help_persons = -1
        else:
            tlog.help_persons = int(tlog.help_persons)
    except Exception as e:
        print(e)
    keywords_parser(tlog)
    tlog.status = 3
    tlog.save()


def keywords_parser(tlog):
    """
    关键词提取
    """
    try:
        s = SnowNLP(tlog.text_content)
        # print('Keywords:', s.keywords(10))
        tlog.sentiments = cal_content_avg_sentiments(s.sentences)
        # jieba
        tlog.keywords = jieba.analyse.extract_tags(tlog.text_content)
    except Exception as e:
        # 暂不处理
        pass


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