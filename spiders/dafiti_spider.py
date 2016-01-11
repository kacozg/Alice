# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from alice.items import AliceItem
import logging
logging.basicConfig(filename='dafiti.txt',level=logging.ERROR)

encoding = "utf-8"

class DafitiSpider(CrawlSpider):
    name = "dafiti"
    start_urls = (
    'http://www.dafiti.cl/marcas/',
    )

    rules = (
    Rule(LinkExtractor(restrict_xpaths=('//li[@id]/ol/li/a')), follow=True),
    Rule(LinkExtractor(restrict_xpaths=('//ul/li[@class="lfloat"]')), follow=True),
    Rule(LinkExtractor(restrict_xpaths=('//ul[@id="productsCatalog"]//ul/li')), callback = 'parse_product', follow=True),
    )

    def parse_product(self, response):

        item = AliceItem()
        item['url'] = response.url
        item['title'] = response.xpath('/html/head/meta[@property="og:title"]/@content').extract()[0]
        item['picture'] = response.xpath('/html/head/meta[@property="og:image"]/@content').extract()[0]
        item['price'] = int(response.xpath('//meta[@itemprop="price"]/@content').re('\d+')[0])
        #generaly use as brand
        item['brand'] = ""
        item['store'] = "dafiti"
        item['id_store'] = 17

        tags = response.xpath('//li[@class="prs"]/a/@title').extract()

        try:
            item['tag1'] = tags[1]
        except:
            item['tag1'] = ""
        try:
            item['tag2'] = tags[2]
        except:
            item['tag2'] = ""
        try:
            item['tag3'] = tags[3]
        except:
            item['tag3'] = ""
        try:
            item['tag4'] = tags[4]
        except:
            item['tag4'] = ""
        try:
            item['tag5'] = tags[5]
        except:
            item['tag5'] = ""
        yield item
