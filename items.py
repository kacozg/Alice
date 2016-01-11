# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AliceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    picture = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    store = scrapy.Field()
    id_store = scrapy.Field()
    tag1 = scrapy.Field()
    tag2 = scrapy.Field()
    tag3 = scrapy.Field()
    tag4 = scrapy.Field()
    tag5 = scrapy.Field()
