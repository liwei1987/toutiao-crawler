#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import datetime
import json
import os
import sys
import time

from scrapy import Spider, Request

from tools.database_tools import get_need_crawl_toutiao_user_list, update_toutiao_user_status
from tools.emoji_tools import remove_emoji
from tools.url_tools import get_index_url
from ..items import ToutiaoIndexItem

reload(sys)
sys.setdefaultencoding('utf-8')


class ToutiaoSpider(Spider):
    # spider 名称
    name = 'toutiao'
    # 允许抓取的域名
    allowed_domains = ['toutiao.com']

    def start_requests(self):
        """
        开始的请求
        :return:
        """
        user_list = get_need_crawl_toutiao_user_list()
        if user_list:
            total_user_count = len(user_list)
            self.logger.info('begin crawl user list, total is %s' % total_user_count)
            for user in user_list:
                user_id = user[0]
                media_id = user[1]
                url = get_index_url(user_id, media_id)
                yield Request(url=url, callback=self.parse_index, meta={'user_id': user_id, 'media_id': media_id}, dont_filter=True)

    def parse_index(self, response):
        """
        解析页面：
        item_id,article_url,title,total_read_count,share_count,has_video
        :param response:
        :return:
        """
        try:
            items = []
            user_id = response.meta.get('user_id')
            media_id = response.meta.get('media_id')
            index_html = response.body
            crawl_data_path = os.path.abspath('data') + '/' + time.strftime('%Y-%m-%d', datetime.datetime.now().timetuple())
            if not os.path.exists(crawl_data_path):
                os.mkdir(crawl_data_path)
            file_name = "%s_%s" % (user_id, media_id)
            outfile = crawl_data_path + "/" + file_name
            with open(outfile, "wb") as code:
                code.write(index_html)
            self.logger.info('crawl toutiao index finish: url is %s, outfile is %s' % (response.url, outfile))
            index_json = json.loads(index_html)
            if 'data' in index_json:
                data = index_json['data']
                self.logger.info('data is {}'.format(data))
                for i in range(len(data)):
                    article = data[i]
                    item = ToutiaoIndexItem()
                    if 'item_id' in article:
                        item['item_id'] = article['item_id']
                    elif 'str_item_id' in article:
                        item['item_id'] = article['str_item_id']
                    else:
                        continue
                    item['user_id'] = user_id
                    item['media_id'] = media_id
                    item['article_url'] = article['article_url']
                    item['title'] = remove_emoji(article['title'])
                    item['read_count'] = article['total_read_count']
                    item['share_count'] = article['share_count']
                    item['content_type'] = 2 if article['has_video'] else 0
                    item['publish_time'] = article['publish_time']
                    item['datetime'] = article['datetime']
                    items.append(item)
                    yield item
            if len(items) > 0:
                update_toutiao_user_status(user_id, media_id, 1)
            else:
                update_toutiao_user_status(user_id, media_id, -1)
        except Exception as e:
            self.logger.exception('crawl toutiao index has an error {}'.format(e))

    # def start_requests(self):
    #     """
    #     开始的请求
    #     :return:
    #     """
    #     last_crawl_id = 0
    #     crawl_round = 0
    #     round_size = 10000
    #     is_finish = False
    #     while not is_finish:
    #         query = 'select user_id, media_id, name from spider_toutiao_user where status !=1 and id >= %s order by id asc limit %s, %s' % (last_crawl_id, crawl_round * round_size, round_size)
    #         spider_conn = get_spider_conn()
    #         spider_cursor = spider_conn.cursor()
    #         spider_cursor.execute(query)
    #         rows = spider_cursor.fetchall()
    #         total = len(rows)
    #         self.logger.info('begin crawl query is {}, round is {}, total is {}'.format(query, crawl_round, total))
    #         if total < round_size:
    #             is_finish = True
    #         for row in rows:
    #             user_id = row[0]
    #             media_id = row[1]
    #             url = get_index_url(user_id, media_id)
    #             yield Request(url=url, callback=self.parse_index, meta={'user_id': user_id, 'media_id': media_id}, dont_filter=True)
    #             time.sleep(60)
    #         crawl_round = crawl_round + 1
    #         spider_cursor.close()
    #         spider_conn.close()

    # def parse_detail(self, response):
    #     detail_html = response.body
    #     self.logger.warning('detail html is {}'.format(detail_html))
    #     try:
    #         item = ToutiaoDetailItem()
    #         item.content = detail_html
    #         yield item
    #     except Exception as e:
    #         self.logger.exception('crawl toutiao detail has an error {}'.format(e))
    #     finally:
    #         self.logger.info('crawl toutiao detail finish')
