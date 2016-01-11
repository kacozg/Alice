# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from alice.items import AliceItem
import logging
logging.basicConfig(filename='zmart.txt',level=logging.ERROR)

encoding = "utf-8"

class ZmartSpider(CrawlSpider):
    name = "zmart"
    start_urls = (
    'http://www.zmart.cl/Scripts/default.asp',
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
        item['tag1'] = "VideoGaming"
        item['tag2'] = ""
        item['tag3'] = ""
        item['tag4'] = ""
        item['tag5'] = ""
        yield item



        '''

        try:
            item['tag1'] = response.xpath('//*[@id="imagen_producto"]/div[2]/span[2]//text()')[0].extract()
        except:
            item['tag1'] = ""
        try:
            item['tag2'] = response.xpath('//*[@id="imagen_producto"]/div[3]/span[2]//text()')[0].extract()
        except:
            item['tag2'] = ""
        try:
            item['tag3'] = response.xpath('//*[@id="imagen_producto"]/div[4]/span[2]//text()')[0].extract()
        except:
            item['tag3'] = ""
        try:
            item['tag4'] = response.xpath('//*[@id="imagen_producto"]/div[5]/span[2]//text()')[0].extract()
        except:
            item['tag4'] = ""
        try:
            item['tag5'] = response.xpath('//*[@id="imagen_producto"]/div[6]/span[2]//text()')[0].extract()
        except:
            item['tag5'] = ""
        yield item
        '''
