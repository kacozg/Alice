# -*- coding: utf-8 -*-
encoding = "utf-8"
import scrapy
import logging
logging.basicConfig(filename='falabella.txt',level=logging.ERROR)
from alice.items import AliceItem


class FalabellaSpider(scrapy.Spider):
    name = "falabella"
    start_urls = (
    'http://www.falabella.com/falabella-cl/category/?Nrpp=12&No=0',
    )
    def parse(self, response):
        found_number = response.xpath('//*[@id="verProductos"]/text()').re('\d+,\d+')[0].replace(",","")
        for initial_number in xrange(12, int(found_number)+12, 12):
            page = "http://www.falabella.com/falabella-cl/category/?Nrpp=12&No=" + str(initial_number)#initial_number
            yield scrapy.Request(page, callback=self.parse_page)

        for index in xrange(0,12,1):
            href = response.xpath('//*[@class="cajaLP4x"]/div[2]/div/a/@href').extract()[index]
            href = href.encode('utf-8')
            product = "http://www.falabella.com" + str(href)
            yield scrapy.Request(product, callback=self.parse_products)

    def parse_page(self, response):

        for index in xrange(0,12,1):
            href = response.xpath('//*[@class="cajaLP4x"]/div[2]/div/a/@href').extract()[index]
            href = href.encode('utf-8')
            product = "http://www.falabella.com" + str(href)
            yield scrapy.Request(product, callback=self.parse_products)

    def parse_products(self, response):
        try:
            item = AliceItem()
            item['url'] = response.url
            item['picture'] = response.xpath('//*[@id="contenedor1PP"]/meta/@content').extract()[0]
            try:
                item['price'] = int(response.xpath('//*[@id="skuPrice"]/div[@class="precio1"]/text()[2]').extract()[0].replace(".",""))
            except:
                item['price'] = int(response.xpath('//*[@id="skuPrice"]/div[@class="precio1"]/span[2]/text()').extract()[0].replace(".",""))
            item['brand'] = response.xpath('//*[@id="productBrand"]/text()').extract()[0].title()
            item['title'] = response.xpath('//*[@id="skuPrice"]/meta[@name="twitter:title"]/@content').extract()[0].title().encode('ascii', 'ignore')
            item['store'] = "falabella"
            item['id_store'] = 1

            tags = response.xpath('//div[@id="ruta"]//text()').re('\S.+\S')

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
            print "error", index, arg
