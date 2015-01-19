# -*- coding: utf-8 -*-

# Scrapy settings for hhf project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'hhf'

SPIDER_MODULES = ['hhf.spiders']
NEWSPIDER_MODULE = 'hhf.spiders'

DOWNLOAD_TIMEOUT = 1800
# DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_IP = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
RETRY_TIMES = 50
RETRY_HTTP_CODES = [503, 504, 400, 403, 404, 408]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36"\
             " (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 8,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 20,
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 30,
    'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': True,
}
RETRY_ENABLED = False
ITEM_PIPELINES = {
    'hhf.pipelines.MyImagesPipeline' : 1,
    'hhf.pipelines.XmlExportPipeline': 2

}
IMAGES_STORE= 'D:/work/images'

