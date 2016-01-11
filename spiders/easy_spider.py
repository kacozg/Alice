# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

logging.basicConfig(filename='easy.txt')

from alice.items import AliceItem

class EasySpider(CrawlSpider):
    name = "easy"
    allowed_domains = ['easy.cl']
    start_urls = (
    'http://www.easy.cl/easy',
    )

    rules = (
    # Extract links matching 'category.php' (but not matching 'subsection.php')
    # and follow links from them (since no callback means follow=True by default).
    Rule(LinkExtractor(allow = 'http://www.easy.cl/easy/ProductDisplay'), callback='parse_product', follow=True),
    Rule(LinkExtractor(allow = 'easy'), callback='parse', follow=True),
    )

    def parse_product(self, response):
        title = response.xpath('//title/text()').extract()[0]
        if not "Problemas" in title:

            try:
                item = AliceItem()
                item['url'] = response.url

                try:
                    item['title'] = response.xpath('/html/head/meta[@property="og:title"]/@content').extract()[0]
                except:
                    item['title'] = response.xpath('/html/head/meta[@property="og:title"]/@content').extract()

                try:
                    item['picture'] = response.xpath('/html/head/meta[@property="og:image"]/@content').extract()[0]
                except:
                    item['picture'] = response.xpath('/html/head/meta[@property="og:title"]/@content').extract()

                try:
                    item['price'] = int(response.xpath('//*[starts-with(@class,"txt_info_precio_")]/text()').re('\d\S*')[0].replace('.',''))
                except:
                    try:
                        item['price'] = int(response.xpath('//*[starts-with(@class,"txt_info_precio_")]/text()').re('\d\S*').replace('.',''))
                    except:
                        try:
                            item['price'] = int(response.xpath('//*[starts-with(@class,"txt_info_precio_")]/text()')[1].re('\d\S*')[0])
                        except:
                            item['price'] = int(response.xpath('//*[starts-with(@class,"txt_info_precio_")]/text()')[1].re('\d\S*')[0].replace('.',''))

                item['brand'] = ""
                item['store'] = "easy"
                item['id_store'] = 10

                tags = response.xpath('//div[@class="ruta_ubicacion_lista" and not(@style)]//text()').re('\w.+')
                tags.pop(0)
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


                yield item
            except IOError:
                print 'cannot open', arg
                logging.warning(arg)
        else:
            print "Tecnical Problem on Server"
