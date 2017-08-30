"""
links 生产者,负责发布links任务
"""
from tasks.links import crawl_place_links

place_id = 10065
page_numbers = 300

if __name__ == '__main__':
    for p_number in range(1, page_numbers+1):
        r = crawl_place_links.delay(place_id, p_number)

