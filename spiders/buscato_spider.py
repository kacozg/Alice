# -*- coding: utf-8 -*-

import scrapy
from alice.items import AliceItem

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.crawler import CrawlerProcess
import logging

logging.basicConfig(filename='critical.txt',level=logging.CRITICAL)
logging.basicConfig(filename='error.txt',level=logging.ERROR)
logging.basicConfig(filename='warning.txt',level=logging.WARNING)
logging.basicConfig(filename='info.txt',level=logging.INFO)
logging.basicConfig(filename='debug.txt',level=logging.DEBUG)

class Spider0(CrawlSpider):
    name : "spider0"

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


class DafitiSpider(CrawlSpider):
    name = "dafiti"
    start_urls = (
    'http://www.dafiti.cl/marcas/',
    )

    rules = (
    Rule(LinkExtractor(restrict_xpaths=('//li[@id]/ol/li/a')), follow=True),
    Rule(LinkExtractor(restrict_xpaths=('//ul/li[@class="lfloat"]')), follow=True),
    Rule(LinkExtractor(restrict_xpaths=('//ul[@id="productsCatalog"]//ul/li')), callback = 'parse_product', follow=True),
    )

    def parse_product(self, response):

        item = AliceItem()
        item['url'] = response.url
        item['title'] = response.xpath('/html/head/meta[@property="og:title"]/@content').extract()[0]
        item['picture'] = response.xpath('/html/head/meta[@property="og:image"]/@content').extract()[0]
        item['price'] = int(response.xpath('//meta[@itemprop="price"]/@content').re('\d+')[0])
        #generaly use as brand
        item['brand'] = ""
        item['store'] = "dafiti"
        item['id_store'] = 17

        tags = response.xpath('//li[@class="prs"]/a/@title').extract()

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

class LinioSpider(CrawlSpider):
    name = "linio"
    start_urls = (
    'http://www.linio.cl/',
    )

    rules = (
    Rule(LinkExtractor(restrict_xpaths=('//*[@id="headerMainMenu"]/ul//a')), follow=True),
    Rule(LinkExtractor(restrict_xpaths=('//*[@class="category-level-1 "]')), follow=True),
    Rule(LinkExtractor(restrict_xpaths=('//*[@class="category-level-1"]')), follow=True),
    Rule(LinkExtractor(restrict_xpaths=('//*[@id="catalog-items"]//a')), callback = 'parse_product', follow=True),
    )

    def parse_product(self, response):

        item = AliceItem()
        item['url'] = response.url
        item['title'] = response.xpath('//*[@id="title-product-detail"]/h1/text()').extract()[0]
        item['picture'] = response.xpath('/html/head/meta[14]/@content').extract()[0]
        item['price'] = int(response.xpath('//*[@id="product-special-price"]/span[@property="gr:hasCurrencyValue"]/text()').re('\d.+\d')[0].replace(".",""))
        #generaly use as brand
        item['brand'] = ""
        item['store'] = "linio"
        item['id_store'] = 16

        tags = response.xpath('//*[@id="category-navigation-breadcrumbs"]/li/a/text()').extract()

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

class RipleySpider(CrawlSpider):
    name = "ripley"
    start_urls = (
    'https://www.ripley.cl/ripley-chile',
    )

    def parse(self, response):
        categories = response.xpath('//div[@class="Grid"]/a[not(@class)]/@href').extract()
        for category in categories:
            yield scrapy.Request(category, callback=self.parse_category)
        #yield scrapy.Request('http://www.ripley.cl/ripley-chile/tecnologia/celulares/smartphones', callback=self.parse_category)

    def parse_category(self, response):
        #parse the first 24 itemsUrl of the first page
        for x in range(0,24):
            try:
                itemUrl = response.xpath('//div[@class="product"]/div[@class="product_image"]/a/@href').extract()[x]
                yield scrapy.Request(itemUrl, callback=self.parse_item)
            except:
                pass

        #pagination
        try:
            itemsTotal = int(response.xpath('//*[@id="searchBasedNavigation_widget"]/div[1]/div/div/div/div/div/div[1]/div[3]/div[1]/text()')[0].re('\d+')[2])
        except:
            itemsTotal = int(response.xpath('//span[@id="paginationTotal"]/text()')[0].extract())
        pages = (itemsTotal +24)
        for x in xrange(0,itemsTotal,24):
            pagination = response.url + "?beginIndex=" + str(x)
            yield scrapy.Request(pagination, callback=self.parse_pagination)

    def parse_pagination(self, response):
        for x in range(0,24):
            try:
                itemUrl = response.xpath('//div[@class="product"]/div[@class="product_image"]/a/@href').extract()[x]
                yield scrapy.Request(itemUrl, callback=self.parse_item)
            except:
                pass

    def parse_item(self, response):
        item = AliceItem()
        item['url'] = response.url
        try:
            item['title'] = response.xpath('//span[@itemprop="name"]/text()').re('(\S.+\S)')[0].title()
        except:
            item['title'] = response.xpath('//span[@itemprop="name"]/text()').re('(\S.+\S)').title()
        item['picture'] = "http://www.ripley.cl/ripley-chile" + str(response.xpath('//img[@id="imagen-mini"]/@src').extract()[0])
        item['price'] = int(response.xpath('//p[@class="ofomp"]/text()').re('\d\S*')[0].replace(".",""))
        #generaly use as brand
        item['brand'] = ""
        item['store'] = "ripley"
        item['id_store'] = 2
        try:
            item['tag1'] = response.xpath('//*[@id="breadcrumb"]//text()')[5].extract().title()
        except:
            pass
        try:
            item['tag2'] = response.xpath('//*[@id="breadcrumb"]//text()')[8].extract().title()
        except:
            pass
        try:
            item['tag3'] = response.xpath('//*[@id="breadcrumb"]//text()')[11].extract().title()
        except:
            pass
        try:
            item['tag4'] = response.xpath('//meta[@name="keyword"]/@content').extract()[0].split(',')[0].title()
        except:
            pass
        try:
            item['tag5'] = response.xpath('//meta[@name="keyword"]/@content').extract()[0].split(',')[1].title()
        except:
            item['tag5'] = ""

        yield item

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

class ZmartSpider(CrawlSpider):
    name = "zmart"
    start_urls = (
    'http://www.zmart.cl/Scripts/default.asp',
    )

    rules = (
    Rule(LinkExtractor(allow=('scripts/prodList.asp?')), follow=True),
    Rule(LinkExtractor(allow=('scripts/prodView.asp?')), callback = 'parse_product', follow=True),
    )

    def parse_product(self, response):

        item = AliceItem()
        item['url'] = response.url
        item['title'] = response.xpath('//*[@id="producto"]/h1/a/text()').extract()[0]
        item['picture'] = "http://www.zmart.cl" + response.xpath('//*[@id="imagen_producto"]/img/@src').extract()[0]
        item['price'] = int(response.xpath('//div[@id="PriceProduct"]//text()').re('\d.*\d')[0].replace('.',''))
        #generaly use as brand
        item['brand'] = ""
        item['store'] = "zmart"
        item['id_store'] = 15

        tags = response.xpath('/html/head/meta[22]/@content').extract()[0]
        item['tag1'] = "VideoGaming"
        item['tag2'] = ""
        item['tag3'] = ""
        item['tag4'] = ""
        item['tag5'] = ""
        yield item

process = CrawlerProcess()
process.crawl(AbcdinSpider)
process.crawl(CasaximenaSpider)
process.crawl(CoronaSpider)
process.crawl(DafitiSpider)
process.crawl(EasySpider)
process.crawl(FalabellaSpider)
process.crawl(HitesSpider)
process.crawl(LapolarSpider)
process.crawl(LinioSpider)
process.crawl(ParisSpider)
process.crawl(PcfactorySpider)
process.crawl(RipleySpider)
process.crawl(SodimacSpider)
process.crawl(ZmartSpider)

process.start()
