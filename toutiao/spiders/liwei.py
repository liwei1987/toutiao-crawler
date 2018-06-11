#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys

from scrapy import Spider, Request

reload(sys)
sys.setdefaultencoding('utf-8')


class ToutiaoSpider(Spider):
    # spider 名称
    name = 'liwei'
    # 允许抓取的域名
    allowed_domains = ['liwei1987.com']
    # 自定义配置
    custom_settings = dict(
        COOKIES_ENABLED=True,
        DEFAULT_REQUEST_HEADERS={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'
        },
        USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
        DOWNLOADER_MIDDLEWARES={
            'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
            'toutiao.middlewares.UserAgentMiddleware': 100,
            'toutiao.middlewares.HttpProxyMiddleware': 200,
            'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 300,

        },
        ITEM_PIPELINES={
        },
        DOWNLOAD_DELAY=10,
        DOWNLOAD_TIMEOUT=10
    )

    def start_requests(self):
        url = 'http://www.liwei1987.com'
        yield Request(url=url, callback=self.parse_index, dont_filter=True)

    def parse_index(self, response):
        index_html = response.body
        print index_html
