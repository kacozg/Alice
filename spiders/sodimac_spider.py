# -*- coding: utf-8 -*-

import scrapy
import logging
logging.basicConfig(filename='sodimac.txt',level=logging.ERROR)
from alice.items import AliceItem


class SodimacSpider(scrapy.Spider):
    name = "sodimac"
    start_urls = (
    'http://www.sodimac.cl/sodimac-cl/search/N-1z141ws?Nrpp=16&No=0', #Para sodimac, se encontro la forma de ver el catalogo completo
    )
    def parse(self, response):
#        yield scrapy.Request('http://www.sodimac.cl/sodimac-cl/search/N-1z141ws?Nrpp=16&No=1552', callback=self.parse_page)
        found_number = response.xpath('//*[@id="verProductos"]/text()').re('\d+,\d+')[0].replace(",","") #Se obtiene el total de productos.
        for initial_number in xrange(16, int(found_number)+17, 16):
            page = "http://www.sodimac.cl/sodimac-cl/search/N-1z141ws?Nrpp=16&No=" + str(initial_number)#pagina inicial
            yield scrapy.Request(page, callback=self.parse_page)

        for index in xrange(0,16,1): #primeros 16 productos
            href = response.xpath('//*[@class="cajaLP4x"]/div[2]/div/a/@href').extract()[index]
            href = href.encode('utf-8')
            product = "http://www.sodimac.cl" + str(href)
            yield scrapy.Request(product, callback=self.parse_products)

    def parse_page(self, response):

        for index in xrange(0,16,1):
            href = response.xpath('//*[@class="cajaLP4x"]/div[2]/div/a/@href').extract()[index]
            href = href.encode('utf-8')
            product = "http://www.sodimac.cl" + str(href)
            yield scrapy.Request(product, callback=self.parse_products)

    def parse_products(self, response):
        try:
            item = AliceItem()
            item['url'] = response.url
            item['title'] = response.xpath('//meta[@property="og:title"]/@content').extract()[0].replace(' - Sodimac.com','')
            item['picture'] = response.xpath('//meta[@property="og:image"]/@content').extract()[0]
            try:
                item['price'] = int(response.xpath('//div[@class="precio1-1"]/div/text()').re('\d\S*')[0].replace('.',''))
            except:
                item['price'] = int(response.xpath('//div[@id="skuPrice"]//div[@class="precio1-1"]/text()').re('\d\S*')[0].replace('.',''))

            try:
                item['brand'] = response.xpath('//div[@class="marca"]/text()').re('\S.+\S')[0]
            except:
                try:
                    item['brand'] = response.xpath('//div[@class="marca"]/text()').re('\S.+\S')
                except:
                    item['brand'] = ''

            item['store'] = "sodimac"
            item['id_store'] = 11

            tags = response.xpath('//div[@id="ruta"]//span/text()').re('\S.+\S')
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
