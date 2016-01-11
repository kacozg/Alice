# -*- coding: utf-8 -*-
encoding = "utf-8"
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from alice.items import AliceItem
import logging
logging.basicConfig(filename='corona.txt',level=logging.ERROR)

class CoronaSpider(CrawlSpider):
    name = "corona"
    start_urls = (
    'http://www.corona.cl/coronaonline/webapp/home.htm',
    )

    siteUrl = "http://www.corona.cl/coronaonline"
    paginator = '&pag='
    pageSize = 16
    counter = 0

    def parse(self, response):
        categories = response.xpath('//*[@id="contenedor_nav"]//div[@class="listCol"]/ul/li/a/@href').extract()
        for category in categories:
            categoryUrl = category.replace('..',self.siteUrl)
            yield scrapy.Request(categoryUrl, callback = self.parse_category)

        #yield scrapy.Request('http://www.corona.cl/coronaonline/webapp/cat_display_det.htm?cat_id=351&cat_id_sup=258&category_path=258,351', callback = self.parse_category)

    def parse_category(self, response):

        itemList = response.xpath('//*[@id="destacado_box2"]/a/@href').extract()
        for item in itemList:
            itemUrl = "http://www.corona.cl/coronaonline/webapp/" + item
            yield scrapy.Request(itemUrl, callback = self.parse_item)

        try:
            pages = response.xpath('//div[@id="paginacion_contenedor"]/div[@id="paginas_contenedor2"]/ul/li/a/text()').extract()
            last_page = int(pages[-1])
            for x in range(2,last_page+1):
                itemList = response.url + self.paginator + str(x)
                yield scrapy.Request(itemList, callback = self.parse_list)
        except:
            pass

    def parse_list(self, response):

        itemList = response.xpath('//*[@id="destacado_box2"]/a/@href').extract()
        for item in itemList:
            itemUrl = "http://www.corona.cl/coronaonline/webapp/" + item
            yield scrapy.Request(itemUrl, callback = self.parse_item)

    def parse_item(self, response):
        try:
            item = AliceItem()
            item['url'] = response.url

            try:
                item['title'] = str(response.xpath('//*[@id="breadcrum"]/text()')[-1].re('\S.+\S')[0].replace('| ',''))
            except:
                try:
                    item['title'] = str(response.xpath('//*[@id="cont_ficha_right"]/h1/text()')[0])
                except:
                    item['title'] = str(response.xpath('//*[@id="cont_ficha_right"]/h1/text()'))

            item['picture'] = "http://www.corona.cl" + response.xpath('//img[@id="img_zoom"]/@src')[0].extract()
            try:
                item['price'] = int(response.xpath('//div[@id="cont_ficha_precio"]/span[@class="precio_internet"]/text()').re('\d\S*')[0].replace(',',''))
            except:
                item['price'] = int(response.xpath('//div[@id="cont_ficha_precio"]/span/text()').re('\d\S*')[0].replace(',',''))

            item['brand'] = ""
            item['store'] = "corona"
            item['id_store'] = 13

            tags = response.xpath('//*[@id="breadcrum"]/a/text()').re('\S.+\S')
            tags.pop(0)

            try:
                item['tag1'] = tags[0]
            except:
                item['tag1'] = ""
            try:
                item['tag2'] = tags[1]
            except:
                item['tag2'] = ""
            try:
                item['tag3'] = tags[2]
            except:
                item['tag3'] = ""
            try:
                item['tag4'] = tags[3]
            except:
                item['tag4'] = ""
            try:
                item['tag5'] = tags[4]
            except:
                item['tag5'] = ""


            yield item
        except IOError:
            print 'cannot open', arg
