# -*- coding: utf-8 -*-
encoding = "utf-8"
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from alice.items import AliceItem
import logging
logging.basicConfig(filename='casaximena.txt',level=logging.ERROR)

class CasaximenaSpider(CrawlSpider):
    name = "casaximena"
    start_urls = (
    'https://www.casaximena.cl/new/index.php',
    )

    siteUrl = "https://www.casaximena.cl/new/"
    paginator = '&pagina='
    pageSize = 16
    counter = 0

    def parse(self, response):
        categories = response.xpath('//*[@id="wrapper"]/nav/ul/li/div/ul/li/a/@href').extract()
        for category in categories:
            categoryUrl = self.siteUrl + category
            yield scrapy.Request(categoryUrl, callback = self.parse_category)

    def parse_category(self, response):

        itemList = response.xpath('//*[@id="main"]/div[2]/ul[@class="row-result"]/li/a/@href').extract()
        for item in itemList:
            itemUrl = self.siteUrl + item
            yield scrapy.Request(itemUrl, callback = self.parse_item)

        try:
            pages = response.xpath('//*[@id="main"]/div[@class="container-right-search"]/div[@class="containder-order"][2]/ul/li[@class="pagina"]/a[@class="paginador"]/text()').extract()
            last_page = int(pages[-1])
            for x in range(2,last_page+1):
                itemList = response.url + self.paginator + str(x)
                yield scrapy.Request(itemList, callback = self.parse_list)
        except:
            pass

    def parse_list(self, response):

        itemList = response.xpath('//*[@id="main"]/div[2]/ul[@class="row-result"]/li/a/@href').extract()
        for item in itemList:
            itemUrl = self.siteUrl + item
            yield scrapy.Request(itemUrl, callback = self.parse_item)

    def parse_item(self, response):
        try:
            item = AliceItem()
            item['url'] = response.url

            item['title'] = (response.xpath('//*[@id="main"]/div[@class="container-data-product"]/h3[@class="title-product"]/text()').re('\S.+\S')[0].title())
            item['picture'] = response.xpath('//img[@id]/@src')[0].extract().replace('..','https://www.casaximena.cl').replace('public/img/productos','https://www.casaximena.cl/new/public/img/productos')
            item['price'] = int(response.xpath('//*[@id="main"]/div[2]/h3[2]/span/text()').re('\d\S*')[0].replace('.',''))
            item['brand'] = ""
            item['store'] = "casaximena"
            item['id_store'] = 14

            tags = response.xpath('//*[@id="main"]/ul/li/a/text()').re('\S.+\S')
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
