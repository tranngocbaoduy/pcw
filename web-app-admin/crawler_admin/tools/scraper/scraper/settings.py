import os
import sys

# file_dir = os.path.dirname(os.path.realpath(__file__))
# root_dir = os.path.abspath(file_dir + '/..')
# sys.path.append(os.path.normpath(root_dir))

import django
from tools.scraper.scraper.utils import CrawlingHelper

# DJANGO INTEGRATION
sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..")
)
sys.path.append(os.path.dirname(os.path.abspath("")))
os.environ["DJANGO_SETTINGS_MODULE"] = "crawler_admin.settings"

django.setup()

# Scrapy settings for scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "meteor"

SPIDER_MODULES = ["tools.scraper.scraper.spiders"]
SPIRDER_MODULE = "tools.scraper.scraper.spiders"

LOG_LEVEL = 'DEBUG'
LOG_FILE = os.path.join(
    "tools/scraper/scraper/log", "{}.log".format(CrawlingHelper.get_name_by_time())
)

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'scraper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16 
CONCURRENT_ITEMS = 20

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 5
DOWNLOAD_TIMEOUT = 300
DOWNLOAD_FAIL_ON_DATALOSS = False
DEPTH_STATS_VERBOSE = True
# DEPTH_LIMIT = 20
CLOSESPIDER_TIMEOUT = 10*60
RETRY_TIMES = 3 
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 5
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
   "Accept-Encoding": "gzip, deflate, br", 
   "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,ja;q=0.4", 
   "Sec-Fetch-Dest": "document",
   "Referer": "https://www.google.com/",
   "Sec-Fetch-Site": "same-origin",
   "Sec-Fetch-Mode": "navigate",
   "Sec-Fetch-User": "?1",
   "Upgrade-Insecure-Requests": "1", 
   "Connection": "keep-alive",
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
}
 
# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
#    'tools.scraper.scraper.middlewares.ScraperSpiderMiddleware': 543,
    # "tools.scraper.scrapy_selenium.SeleniumMiddleware": 2000
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html 
DOWNLOADER_MIDDLEWARES = {
    # 'scraper.middlewares.ScraperDownloaderMiddleware': 543,
    # "tools.scraper.scrapy_selenium.SeleniumMiddleware": 2000
}


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "tools.scraper.scraper.pipelines.ScraperPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 16.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
 

DOWNLOADER_CLIENT_TLS_METHOD="TLS"
FEED_EXPORT_ENCODING = 'utf-8'
