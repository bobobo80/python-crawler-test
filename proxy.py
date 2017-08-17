import requests
import re
from bs4 import BeautifulSoup
import json


test_url = 'http://www.mafengwo.cn'
base_url = 'http://www.66ip.cn/areaindex_1/'
ip_check = re.compile(r'^(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}$')

proxies = []
proxies_number = 30

def get_proxy():
    """
    获取代理，写入proxies.json
    """
    current_number = 1
    is_enough = False
    while not is_enough:
        html = BeautifulSoup(requests.get(base_url+str(current_number)+'.html').content, 'lxml')
        try:
            ip_table = html.find('table', bordercolor='#6699ff')
        except Exception as e:
            print(e)
        if ip_table:
            for ip_tr in ip_table.find_all('tr')[1:]:
                tds = ip_tr.find_all('td')
                # check ip
                ip_addr = check_ip('{}:{}'.format(tds[0].text, tds[1].text))
                if ip_addr:
                    proxies.append({'http': 'http://'+ip_addr})
                    if len(proxies) >= proxies_number:
                        is_enough = True
                        break
        current_number += 1


def check_ip(ip_addr):
    """
    检查ip的格式是否正确
    检查ip的速度是否可以
    :return: 正确则返回ip:port格式，不正确则返回None
    """
    if ip_check.findall(ip_addr):
        # test speed
        try:
            resp = requests.get(test_url, timeout=10,
                                proxies={'http': 'http://'+ip_addr})
            if resp.status_code == 200:
                print('可用ip：', ip_addr)
                return ip_addr
        except Exception as e:
            print('不可用：', ip_addr)
    return None


if __name__ == '__main__':
    get_proxy()
    with open('proxies.json', 'w') as f:
        json.dump(proxies, f)