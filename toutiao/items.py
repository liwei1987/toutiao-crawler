# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.org/en/latest/topics/items.html

from scrapy import Item, Field


class ToutiaoIndexItem(Item):
    item_id = Field()
    user_id = Field()
    media_id = Field()
    article_url = Field()
    title = Field()
    read_count = Field()
    share_count = Field()
    content_type = Field()
    publish_time = Field()
    datetime = Field()
