# -*- coding: utf-8 -*-
encoding = "utf-8"
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from alice.items import AliceItem
import logging
logging.basicConfig(filename='paris.txt')

class ParisSpider(CrawlSpider):
    name = "paris"
    start_urls = (
    'http://www.paris.cl/tienda/es/paris',
    )

    pageSize = 30

    def parse(self, response):
        categories = response.xpath('//a[@onclick="clearSearchValueCookie();"]/@href').extract()
        for category in categories:
            yield scrapy.Request(category, callback=self.parse_category)
        #yield scrapy.Request('http://www.paris.cl/tienda/es/paris/search/com-cel-smartphones-', callback=self.parse_category)

    def parse_category(self, response):
        #parse the first 24 itemsUrl of the first page
        for x in range(0,self.pageSize):
            try:
                itemUrl = response.xpath('//*[@class="item"]/div/div/div[@class="description_fixedwidth"]/a/@href').extract()[x]
                yield scrapy.Request(itemUrl, callback=self.parse_item)
            except:
                pass

        #pagination
        itemsTotal = int(response.xpath('//*[@id="WC_CatalogSearchResultDisplay_div_1"]/div[1]/div[1]/b/text()').extract()[0])
        pages = (itemsTotal +self.pageSize)
        for x in xrange(self.pageSize,itemsTotal,self.pageSize):
            pagination = response.url + "?beginIndex=" + str(x)
            yield scrapy.Request(pagination, callback=self.parse_pagination)

    def parse_pagination(self, response):
        for x in range(0,self.pageSize):
            try:
                itemUrl = response.xpath('//*[@class="item"]/div/div/div[@class="description_fixedwidth"]/a/@href').extract()[x]
                yield scrapy.Request(itemUrl, callback=self.parse_item)
            except:
                pass

    def parse_item(self, response):
        item = AliceItem()
        item['url'] = response.url
        item['title'] = response.xpath('//meta[@property="og:description"]/@content').extract()[0].title().encode('ascii', 'ignore')
        item['picture'] = response.xpath('//meta[@property="og:image"]/@content').extract()[0]
        item['price'] = int(response.xpath('//div[@class="price offerPrice bold"]/text()').re('\d\S*')[0].replace(".",""))
        #generaly use as brand
        item['brand'] = ""
        item['store'] = "Paris"
        item['id_store'] = 3

        tags = response.xpath('//*[@id="WC_BreadCrumbTrailDisplay_div_1"]//text()').re('\w.+')
        tags.pop()

        try:
            if (tags[0] == ""):
                item['tag1'] = "Sin categoría"
            else:
                item['tag1'] = tags[0].title()
        except:
            item['tag1'] = "Sin categoría"
        try:
            item['tag2'] = tags[1].title()
        except:
            item['tag2'] = ""
        try:
            item['tag3'] = tags[2].title()
        except:
            item['tag3'] = ""
        try:
            item['tag4'] = tags[3].title()
        except:
            item['tag4'] = ""
        try:
            item['tag5'] = tags[4].title()
        except:
            item['tag5'] = ""
        yield item
