import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


class Tlog(object):
    """
    自定义游记类，暂时就是参数信息
    """
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.error = None


    def download_content(self):
        """
        下载对应页面的内容
        """
        ua = UserAgent()
        # 检查url是否为标准的地址格式, 换正则mafengwo.cn/i/\d+$
        if r'mafengwo.cn/i/' not in self.url:
            return
        r = requests.get(self.url, ua.chrome)
        if r.status_code == 200:
            self.html = r.content.decode('utf-8')
            self.parse_content()


    def parse_content(self):
        """
        解析html页面内容
        """
        if self.html is None:
            return
        # 使用bs解析
        html_bs_obj = BeautifulSoup(self.html, 'lxml')
        try:
            # 大标题
            self.title = html_bs_obj.select('h1')[0].text
            print(self.title)
            # 出发时间
            self.start_time = html_bs_obj.select('.time')[0].text.split(r'/')[1]
            # 出行天数
            self.days = html_bs_obj.select('.day')[0].text.split(r'/')[1]
            # 文字内容
            self.text_content = html_bs_obj.find(class_='va_con').text
            self.text_content = ''.join(self.text_content.split())
        except IndexError:
            self.error = 'Parse content error. Index out of range.'
        except AttributeError:
            self.error = 'Parse content error. No attribute.'


    def to_string_for_save(self):
        """
        为了存储为文件，将所有属性转换为字符串
        """
        if not self.error:
            return '{}^{}^{}^{}^{}^{}'.format(self.title,
                                              self.start_time,
                                              self.days,
                                              self.text_content,
                                              self.url,
                                              self.html)
        else:
            return ''

