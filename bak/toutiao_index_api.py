#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import datetime
import os
import time

from scrapy import Spider, Request

from toutiao.items import ToutiaoDetailItem
from tools.url_tools import get_sign
from tools.tools import get_crawl_conn


class ToutiaoIndexApiSpider(Spider):
    name = 'toutiao_index_api'
    allowed_domains = ['toutiao.com']

    def start_requests(self):
        last_crawl_user_id = '0'
        round = 0
        round_size = 10000
        is_finish = False
        while not is_finish:
            query = 'select user_id, media_id, name from crawl_toutiao_user where last_number = 0 and status=0 and user_id >= "%s" order by user_id limit %s, %s' % (last_crawl_user_id, round * round_size, round_size)
            crawl_conn = get_crawl_conn()
            crawl_cursor = crawl_conn.cursor()
            crawl_cursor.execute(query)
            rows = crawl_cursor.fetchall()
            total = len(rows)
            self.logger.info('begin crawl query is {}, round is {}, total is {}'.format(query, round, total))
            if total < round_size:
                is_finish = True
            for row in rows:
                user_id = row[0]
                media_id = row[1]
                sign = get_sign()
                url = 'https://toutiao.com/pgc/ma/?page_type=1&max_behot_time=&uid={}&media_id={}&output=json&is_json=1&count=30&version=2&as={}&cp={}'.format(user_id, media_id, sign['as'], sign['cp'])
                yield Request(url=url, callback=self.parse_index, meta={'user_id': user_id, 'media_id': media_id}, dont_filter=True)
            round = round + 1

    def parse_index(self, response):
        try:
            user_id = response.meta.get('user_id')
            media_id = response.meta.get('media_id')
            index_html = response.body
            crawl_data_path = os.path.abspath('../../data/') + time.strftime('%Y-%m-%d', datetime.datetime.now().timetuple())
            if not os.path.exists(crawl_data_path):
                os.mkdir(crawl_data_path)
            file_name = "%s_%s" % (user_id, media_id)
            outfile = crawl_data_path + "/" + file_name
            with open(outfile, "wb") as code:
                code.write(index_html)
            self.logger.info('crawl toutiao index finish: url is %s, outfile is %s' % (response.url, outfile))
            # if 'data' in index_json:
            #     data = index_json['data']
            #     self.logger.info('data is {}'.format(data))
            #     for i in range(len(data)):
            #         article = data[i]
            #         item = ToutiaoIndexItem
            #         item.title = article['title']
            #         item.go_detail_count = article['go_detail_count']
            #         item.share_count = article['share_count']
            #         item.publish_time = article['publish_time']
            #         item.url = article['url']
            #         yield Request(url=item.url, callback=self.parse_detail)
        except Exception as e:
            self.logger.exception('crawl toutiao index has an error {}'.format(e))

    def parse_detail(self, response):
        detail_html = response.body
        self.logger.warning('detail html is {}'.format(detail_html))
        try:
            item = ToutiaoDetailItem()
            item.content = detail_html
            yield item
        except Exception as e:
            self.logger.exception('crawl toutiao detail has an error {}'.format(e))
        finally:
            self.logger.info('crawl toutiao detail finish')
