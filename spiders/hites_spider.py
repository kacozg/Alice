# -*- coding: utf-8 -*-
encoding = "utf-8"
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import logging
logging.basicConfig(filename='hites.txt',level=logging.ERROR)

from alice.items import AliceItem

class HitesSpider(CrawlSpider):
    name = "hites"
    allowed_domains = ['hites.cl']
    start_urls = (
    'http://www.hites.cl/b2c/',
    )

    rules = (
    # Extract links matching 'category.php' (but not matching 'subsection.php')
    # and follow links from them (since no callback means follow=True by default).
    Rule(LinkExtractor(allow = 'id_product='), callback='parse_product', follow=True),
    Rule(LinkExtractor(allow = 'http://www.hites.cl/b2c/index.php?controller=product'), callback='parse_product', follow=True),
    Rule(LinkExtractor(allow = 'http://www.hites.cl/b2c/'), callback='parse', follow=True),
    )

    def parse_product(self, response):
        try:
            item = AliceItem()
            item['url'] = response.url

            try:
                item['title'] = response.xpath('//meta[@name="description"]/@content').extract()[0].title().encode('ascii', 'ignore')
            except:
                item['title'] = response.xpath('//meta[@name="description"]/@content').extract().title().encode('ascii', 'ignore')

            try:
                item['picture'] = response.xpath('//meta[@property="og:image"]/@content').extract()[0]
            except:
                item['picture'] = response.xpath('///meta[@property="og:title"]/@content').extract()

            try:
                item['price'] = int(response.xpath('//span[@id="our_price_display"]/strong/text()').re('\d\S*')[0].replace('.',''))
            except:
                item['price'] = int(response.xpath('//span[@id="our_price_display"]/strong/text()').re('\d\S*').replace('.',''))

            item['brand'] = response.xpath('//*[@id="pb-left-column"]/h1/text()').extract()[0].title()
            item['store'] = "hites"
            item['id_store'] = 12

            tags = response.xpath('//*[@id="center_column"]/div[@class="breadcrumb"]/a/text()').extract()
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
