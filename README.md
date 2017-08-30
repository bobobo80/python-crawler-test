# python爬虫测试练习

##第一个python爬虫的小项目

准备做一个收集马蜂窝中游记的爬虫，收集一个地点的所有游记
的文字内容，然后通过对文字内容进行语义情感分析，得出各个
地点的好感程度，关键字等内容。

### -----

抓取内容为马蜂窝游记页面的内容。先通过城市页面，使用游记的ajax接口，获取所有游记的链接
通过各个链接访问单独的游记页面，下载游记内容。

经过一轮体验，现改为使用celery开发分布式爬虫,

tasks模块，celery任务定义。
通过schedule定时任务，定时抓取地点的链接和游记。

config.py用于定义数据库接口等内容

db模块，包装redis和mongodb的连接和操作，
redis用于proxy和useragent等数据，
以及celery的broker和backend。
mongodb储存爬取页面之后的解析结果。
并包含游记的数据层相关操作。

proxy模块，调用proxy_pool的接口，从中提取代理ip和端口

mfw_parser模块，包装对html页面解析等操作。

web_get模块，包装request的网络请求

tasks模块，celery的worker接口文件，由此启动celery worker

mfw_parser模块，游记链接，内容等的解析


TODO：
游记的语义分析
游记深层次属性提取，图片数量，评论数等
重新梳理一下架构，拆分抓取页面与解析页面功能，结合消息队列等工具，分化功能
同步爬取，多进程，多线程，分布式
评论的爬取，由评论内容，统计游记的好坏

(mfw-logs-parser)游记内容解析，应用jieba,snownlp提取游记内容的关键词，
情感指数，可是没有相关模型，简单先填一下

test_jupter中是些测试的小例子，requests/selenium等测试
