# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from alice.items import AliceItem
import logging
logging.basicConfig(filename='ripley.txt',level=logging.ERROR)

class RipleySpider(CrawlSpider):
    name = "ripley"
    start_urls = (
    'https://www.ripley.cl/ripley-chile',
    )

    def parse(self, response):
        categories = response.xpath('//div[@class="Grid"]/a[not(@class)]/@href').extract()
        for category in categories:
            yield scrapy.Request(category, callback=self.parse_category)
        #yield scrapy.Request('http://www.ripley.cl/ripley-chile/tecnologia/celulares/smartphones', callback=self.parse_category)

    def parse_category(self, response):
        #parse the first 24 itemsUrl of the first page
        for x in range(0,24):
            try:
                itemUrl = response.xpath('//div[@class="product"]/div[@class="product_image"]/a/@href').extract()[x]
                yield scrapy.Request(itemUrl, callback=self.parse_item)
            except:
                pass

        #pagination
        try:
            itemsTotal = int(response.xpath('//*[@id="searchBasedNavigation_widget"]/div[1]/div/div/div/div/div/div[1]/div[3]/div[1]/text()')[0].re('\d+')[2])
        except:
            itemsTotal = int(response.xpath('//span[@id="paginationTotal"]/text()')[0].extract())
        pages = (itemsTotal +24)
        for x in xrange(0,itemsTotal,24):
            pagination = response.url + "?beginIndex=" + str(x)
            yield scrapy.Request(pagination, callback=self.parse_pagination)

    def parse_pagination(self, response):
        for x in range(0,24):
            try:
                itemUrl = response.xpath('//div[@class="product"]/div[@class="product_image"]/a/@href').extract()[x]
                yield scrapy.Request(itemUrl, callback=self.parse_item)
            except:
                pass

    def parse_item(self, response):
        item = AliceItem()
        item['url'] = response.url
        try:
            item['title'] = response.xpath('//span[@itemprop="name"]/text()').re('(\S.+\S)')[0].title()
        except:
            item['title'] = response.xpath('//span[@itemprop="name"]/text()').re('(\S.+\S)').title()
        item['picture'] = "http://www.ripley.cl/ripley-chile" + str(response.xpath('//img[@id="imagen-mini"]/@src').extract()[0])
        item['price'] = int(response.xpath('//p[@class="ofomp"]/text()').re('\d\S*')[0].replace(".",""))
        #generaly use as brand
        item['brand'] = ""
        item['store'] = "ripley"
        item['id_store'] = 2
        try:
            item['tag1'] = response.xpath('//*[@id="breadcrumb"]//text()')[5].extract().title()
        except:
            pass
        try:
            item['tag2'] = response.xpath('//*[@id="breadcrumb"]//text()')[8].extract().title()
        except:
            pass
        try:
            item['tag3'] = response.xpath('//*[@id="breadcrumb"]//text()')[11].extract().title()
        except:
            pass
        try:
            item['tag4'] = response.xpath('//meta[@name="keyword"]/@content').extract()[0].split(',')[0].title()
        except:
            pass
        try:
            item['tag5'] = response.xpath('//meta[@name="keyword"]/@content').extract()[0].split(',')[1].title()
        except:
            item['tag5'] = ""

        yield item
