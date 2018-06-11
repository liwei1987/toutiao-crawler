# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from tools.database_tools import insert_toutiao_article


class ToutiaoFilePipeline(object):

    def process_item(self, item, spider):
        pass


class ToutiaoDbPipeline(object):

    def process_item(self, item, spider):
        insert_toutiao_article(item)

