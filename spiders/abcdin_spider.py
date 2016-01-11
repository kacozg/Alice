# -*- coding: utf-8 -*-

import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import logging
logging.basicConfig(filename='abcdin.txt')

from alice.items import AliceItem

class AbcdinSpider(CrawlSpider):
    name = "abcdin"
    start_urls = (
    'http://www.abcdin.cl/webapp/wcs/stores/servlet/SiteMap_10001_10001_-5',
    )

    pageSize=12

    def parse(self, response):
        categories = response.xpath('//div[@class="links"]/p/a/@href').extract()
        for category in categories:
            yield scrapy.Request(category, callback=self.parse_category)
        #yield scrapy.Request('http://www.abcdin.cl/webapp/wcs/stores/servlet/es/abcdin/search/consolas-y-videojuegos', callback=self.parse_category)

    def parse_category(self, response):
        #parse the first 24 itemsUrl of the first page
        for x in range(0,self.pageSize):
            try:
                itemUrl = response.xpath('//div/div[@class="dojoDndItem"]/a/@href').extract()[x]
                yield scrapy.Request(itemUrl, callback=self.parse_item)
            except:
                pass

        #pagination
        itemsTotal = int(response.xpath('//*[@id="WC_CatalogSearchResultDisplay_div_1"]/div[4]/text()').re('\d+')[2])

        for x in xrange(0,itemsTotal,self.pageSize):
            pagination = response.url + "?beginIndex=" + str(x)
            yield scrapy.Request(pagination, callback=self.parse_pagination)

    def parse_pagination(self, response):
        for x in range(0,self.pageSize):
            try:
                itemUrl = response.xpath('//div/div[@class="dojoDndItem"]/a/@href').extract()[x]
                yield scrapy.Request(itemUrl, callback=self.parse_item)
            except:
                pass

    def parse_item(self, response):
        try:
            title = response.xpath('//*[@id="producto-no-disponible-texto"]/div/text()').extract()[0]
        except:
            title = "Product founded"
        if not "no se encuentra" in title:

            try:
                item = AliceItem()
                item['url'] = response.url
                try:
                    item['title'] = response.xpath('//html/head/meta[@name="description"]/@content').extract()[0].title()
                except:
                    item['title'] = response.xpath('//*[@id="catalog_link"]/text()').extract()[0].title()
                item['picture'] = "http://www.abcdin.cl" + response.xpath('//img[@id="productMainImage"]/@src').extract()[0]
                item['price'] = int(response.xpath('//td[@class="offerprice"]/text()').re('\d\S*')[0].replace(".",""))
                #generaly use as brand
                item['brand'] = ""
                item['store'] = "abcdin"
                item['id_store'] = 5

                tags = response.xpath('//div[@class="breadcrumb_links"]//text()').re('\w.+')
                tags.pop(0)

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
            except IOError:
                print 'cannot open', arg
        else:
            print "Product not found"
