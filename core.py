"""
How to run scrapers programmatically from a script
"""
import sys
#ubuntu 	sys.path.insert(0, '/home/kaco/Desktop/alice')
#windows 	sys.path.insert(0, 'C:/Users/Carlos/Google Drive/ZetUp/Buscato/alice')
sys.path.insert(0, 'C:/alice')
from spiders.abcdin_spider import AbcdinSpider
from spiders.casaximena_spider import CasaximenaSpider
from spiders.corona_spider import CoronaSpider
from spiders.dafiti_spider import DafitiSpider
from spiders.easy_spider import EasySpider
from spiders.falabella_spider import FalabellaSpider
from spiders.hites_spider import HitesSpider
from spiders.lapolar_spider import LapolarSpider
from spiders.linio_spider import LinioSpider
from spiders.paris_spider import ParisSpider
from spiders.pcfactory_spider import PcfactorySpider
from spiders.ripley_spider import RipleySpider
from spiders.sodimac_spider import SodimacSpider
from spiders.zmart_spider import ZmartSpider

import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging

from scrapy.utils.project import get_project_settings



configure_logging()
runner = CrawlerProcess(get_project_settings())
runner.crawl(AbcdinSpider)
runner.crawl(CasaximenaSpider)
runner.crawl(CoronaSpider)
runner.crawl(DafitiSpider)
runner.crawl(EasySpider)
runner.crawl(FalabellaSpider)
runner.crawl(HitesSpider)
runner.crawl(LapolarSpider)
runner.crawl(LinioSpider)
runner.crawl(ParisSpider)
runner.crawl(PcfactorySpider)
runner.crawl(RipleySpider)
runner.crawl(SodimacSpider)
runner.crawl(ZmartSpider)

d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run() # the script will block here until all crawling jobs are finished
