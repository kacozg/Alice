# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from alice.items import AliceItem
import logging
logging.basicConfig(filename='linio.txt',level=logging.ERROR)

encoding = "utf-8"

class LinioSpider(CrawlSpider):
    name = "linio"
    start_urls = (
    'http://www.linio.cl/',
    )

    rules = (
    Rule(LinkExtractor(restrict_xpaths=('//*[@id="headerMainMenu"]/ul//a')), follow=True),
    Rule(LinkExtractor(restrict_xpaths=('//*[@class="category-level-1 "]')), follow=True),
    Rule(LinkExtractor(restrict_xpaths=('//*[@class="category-level-1"]')), follow=True),
    Rule(LinkExtractor(restrict_xpaths=('//*[@id="catalog-items"]//a')), callback = 'parse_product', follow=True),
    )

    def parse_product(self, response):

        item = AliceItem()
        item['url'] = response.url
        item['title'] = response.xpath('//*[@id="title-product-detail"]/h1/text()').extract()[0]
        item['picture'] = response.xpath('/html/head/meta[14]/@content').extract()[0]
        item['price'] = int(response.xpath('//*[@id="product-special-price"]/span[@property="gr:hasCurrencyValue"]/text()').re('\d.+\d')[0].replace(".",""))
        #generaly use as brand
        item['brand'] = ""
        item['store'] = "linio"
        item['id_store'] = 16

        tags = response.xpath('//*[@id="category-navigation-breadcrumbs"]/li/a/text()').extract()

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
