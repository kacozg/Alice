# -*- coding: utf-8 -*-
encoding = "utf-8"
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from alice.items import AliceItem
import logging
logging.basicConfig(filename='pcfactory.txt',level=logging.ERROR)

class PcfactorySpider(CrawlSpider):
    name = "pcfactory"
    start_urls = (
    'https://www.pcfactory.cl',
    )

    pageSize=12
    dom = "https://www.pcfactory.cl"

    def parse(self, response):
        categories = response.xpath('//ul[@class="dropdown-menu"]/li[@id]/div[@class="popover"]//ul/li/a/@href').extract()
        for category in categories:
            categoryUrl = self.dom + str(category)
            yield scrapy.Request(categoryUrl, callback=self.parse_category)
        #yield scrapy.Request('https://www.pcfactory.cl/?categoria=432&papa=645', callback=self.parse_category)

    def parse_category(self, response):
        #parse the first 24 itemsUrl of the first page
        items = response.xpath('//*[@id="center"]/div/div/table[3]/tr/td/table[2]/tr[2]/td/table/tr[2]/td/a/@href').extract()
        for url in items:
            itemUrl = self.dom + str(url)
            yield scrapy.Request(itemUrl, callback=self.parse_item)

        #pagination
        try:
            itemsTotal = int(response.xpath('//*[@id="center"]/div/div/table[2]/tr[2]/td/table/tr/td[4]/strong').re('\d+')[0])
        except:
            itemsTotal = int(response.xpath('//span[@class="main_title2"]/text()')[0].extract())

        for x in range(0,(itemsTotal+self.pageSize)/12):
            pagination = response.url + "&pagina=" + str(x)
            yield scrapy.Request(pagination, callback=self.parse_pagination)

    def parse_pagination(self, response):
        items = response.xpath('//*[@id="center"]/div/div/table[3]/tr/td/table[2]/tr[2]/td/table/tr[2]/td/a/@href').extract()
        for url in items:
            itemUrl = self.dom + str(url)
            yield scrapy.Request(itemUrl, callback=self.parse_item)

    def parse_item(self, response):
        try:
            item = AliceItem()
            item['url'] = response.url
            title = response.xpath('//tr/td/strong/span[@class="main_titulo_ficha_bold"]/text()').re('\S.+\S')
            try:
                title.pop(2)
            except:
                title.pop(1)
            item['title'] = " ".join(title).title().encode('ascii', 'ignore')
            item['picture'] = self.dom + response.xpath('//div[@id="loadarea"]/a[@href]/img/@src').extract()[0]
            try:
                item['price'] = int(response.xpath('//span[@class="main_precio_efectivo"]/strong/text()').re('\d\S*')[0].replace('.',''))
            except:
                item['price'] = int(response.xpath('//div[@class="precio_lg"]/text()')[0].re('\d\S*')[0].replace('.',''))
            #generaly use as brand
            item['brand'] = title[0]
            item['store'] = "pcfactory"
            item['id_store'] = 6

            tags = response.xpath('//a[@class="main_ruta_link"]/text()').extract()

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
        except IOError:
            print 'cannot open', arg
