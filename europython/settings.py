# -*- coding: utf-8 -*-

# Scrapy settings for europython project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'europython'

SPIDER_MODULES = ['europython.spiders']
NEWSPIDER_MODULE = 'europython.spiders'

ITEM_PIPELINES = ['europython.pipelines.EuropythonPipeline','europython.pipelines.EuropythonXmlExport','europython.pipelines.EuropythonMySQLPipeline']


DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'europython.middlewares.ProxyMiddleware': 100,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'europython (+http://www.yourdomain.com)'
