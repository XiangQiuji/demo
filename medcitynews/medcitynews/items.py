# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MedcitynewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    topics = scrapy.Field()
    image_url = scrapy.Field()
    image_path = scrapy.Field()
    crawled_url = scrapy.Field()
    crawled_time = scrapy.Field()
    publish_time = scrapy.Field()