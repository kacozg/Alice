# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from alice.items import AliceItem
import logging
logging.basicConfig(filename='test.txt',level=logging.ERROR)

encoding = "utf-8"

class Zmartpider(CrawlSpider):
    name = "test"
    start_urls = (
    'http://www.zmart.cl/scripts/prodList.asp?idCategory=420',
    )

    rules = (
    Rule(LinkExtractor(allow=('scripts/prodList.asp?')), follow=True),
    Rule(LinkExtractor(allow=('scripts/prodView.asp?')), callback = 'parse_product', follow=True),
    )

    def parse_product(self, response):

        item = AliceItem()
        item['url'] = response.url
        item['title'] = response.xpath('//*[@id="producto"]/h1/a/text()').extract()[0]
        item['picture'] = "http://www.zmart.cl" + response.xpath('//*[@id="imagen_producto"]/img/@src').extract()[0]
        item['price'] = int(response.xpath('//div[@id="PriceProduct"]//text()').re('\d.*\d')[0].replace('.',''))
        #generaly use as brand
        item['brand'] = ""
        item['store'] = "zmart"
        item['id_store'] = 15

        tags = response.xpath('/html/head/meta[22]/@content').extract()[0]
        item['tag1'] = "Videojuegos y Consolas"
        item['tag2'] = ""
        item['tag3'] = ""
        item['tag4'] = ""
        item['tag5'] = ""
        yield item
