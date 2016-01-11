# -*- coding: utf-8 -*-

# Scrapy settings for alice project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'alice'

SPIDER_MODULES = ['alice.spiders']
NEWSPIDER_MODULE = 'alice.spiders'


DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'random_useragent.RandomUserAgentMiddleware': 400
}

USER_AGENT_LIST = "C:/alice/useragents.txt"
#USER_AGENT_LIST = "C:/Users/Carlos/Google Drive/ZetUp/Buscato/alice/useragents.txt"
#USER_AGENT_LIST = "/home/kaco/Desktop/alice/useragents.txt"

COOKIES_ENABLED = False

DOWNLOAD_DELAY = 2

''' Servidor
MYSQL_HOST = '192.168.1.34'
MYSQL_DBNAME = 'quevale_bd'
MYSQL_USER = 'pma'
MYSQL_PASSWD = 's3rv3r'
'''


''' Localhost'''
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'buscato'
MYSQL_USER = 'root'
MYSQL_PASSWD = ''

ITEM_PIPELINES = {
    'alice.pipelines.MySQLStorePipeline': 0,
}

DOWNLOAD_HANDLERS = {
  's3': None,
}



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'abcdin (+http://www.yourdomain.com)'
#execute everything from windows

#WINDOWS
#scrapy crawl abcdin & scrapy crawl casaximena & scrapy crawl corona & scrapy crawl easy & scrapy crawl falabella & scrapy crawl hites & scrapy crawl lapolar & scrapy crawl paris & scrapy crawl pcfactory & scrapy crawl ripley & scrapy crawl sodimac & scrapy crawl zmart & scrapy crawl linio & scrapy crawl dafiti
#LINUX
#scrapy crawl
#python core.py

#en el log, buscar por "Spider error processing"
