# -*- coding: utf-8 -*-
encoding = "utf-8"
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import logging
logging.basicConfig(filename='lapolar.txt',level=logging.ERROR)

from alice.items import AliceItem

class LapolarSpider(CrawlSpider):
    name = "lapolar"
    allowed_domains = ['lapolar.cl']
    start_urls = (
    'http://www.lapolar.cl/internet/catalogo/',
    )

    rules = (
    Rule(LinkExtractor(allow = "http://www.lapolar.cl/internet/catalogo/detalle"), callback='parse_product', follow=True),
    Rule(LinkExtractor(allow = ['http://www.lapolar.cl/internet/catalogo/grupo','http://www.lapolar.cl/internet/catalogo/categoria']), callback='parse', follow=True),
    Rule(LinkExtractor(allow = 'http://www.lapolar.cl/internet/catalogo/listados'), callback='parse_links', follow=True),
    Rule(LinkExtractor(allow = 'http://www.lapolar.cl/internet/catalogo/todolistados'), callback='parse_links', follow=True),
    )

    def parse_links(self, response):
        jsonlinks = response.xpath('//script[@language="javascript"]/text()').re('"ruta":"[a-z0-9/_]+')
        for link in jsonlinks:
            url = "http://www.lapolar.cl/internet/catalogo/detalles/" + link.replace('"ruta":"','')
            yield scrapy.Request(url, callback=self.parse_product)

    def parse_product(self, response):
        try:
            item = AliceItem()
            item['url'] = response.url

            try:
                item['title'] = response.xpath('//*[@class="titulo1 descrip_jq"]/text()').extract()[0].encode('ascii', 'ignore')
            except:
                item['title'] = response.xpath('//*[@class="titulo1 descrip_jq"]/text()').extract().encode('ascii', 'ignore')

            try:
                item['picture'] = response.xpath('/html/head/meta[3]/@content').extract()[0]
            except:
                item['picture'] = response.xpath('/html/head/meta[3]/@content').extract()

            try:
                item['price'] = int(response.xpath('//*[@class="precio precio_jq"]/text()').re('\d\S*')[0].replace('.',''))
            except:
                item['price'] = int(response.xpath('//*[@class="precio precio_jq"]/text()').re('\d\S*').replace('.',''))

            item['brand'] = ""
            item['store'] = "lapolar"
            item['id_store'] = 4

            tags = response.xpath('//tr[not(@id)]/td[@valign="top"]/div[@width]/a/text()').extract()

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
