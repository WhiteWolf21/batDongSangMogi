# -*- coding: utf-8 -*-

# Scrapy settings for mogi_vn project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import urllib.parse

BOT_NAME = 'mogi_vn'

SPIDER_MODULES = ['mogi_vn.spiders']
NEWSPIDER_MODULE = 'mogi_vn.spiders'

ITEM_PIPELINES = {
    'mogi_vn.pipelines.PostExtractPipeline': 300,
    'mogi_vn.pipelines.MongoPipeline': 400,
}


MONGO_SERVER  = "local"
MONGO_LINK    = "localhost:27017"

MONGO_DB      = "mogi"
MONGO_DATA    = "marker"


# PROVINCES = {
#     1:  ["an-giang",        "An Giang"],
#     2:  ["bac-can",         "Bắc Kạn"],
#     3:  ["bac-giang",       "Bắc Giang"],
#     4:  ["bac-lieu",        "Bạc Liêu"],
#     5:  ["bac-ninh",        "Bắc Ninh"],
#     6:  ["ba-ria-vung-tau", "bà rịa - vũng tàu"],
#     7:  ["ben-tre",         "Bến Tre"],
#     8:  ["binh-dinh",       "Bình Định"],
#     9:  ["binh-duong",      "bình dương"],
#     10: ["binh-phuoc",      "Bình Phước"],
#     11: ["binh-thuan",      "Bình Thuận"],
#     12: ["ca-mau",          "Cà Mau"],
#     13: ["can-tho",         "Cần Thơ"],
#     14: ["cao-bang",        "Cao Bằng"],
#     15: ["dak-lak",         "Đắk Lắk"],
#     16: ["dak-nong"         "Đắk Nông"],
#     17: ["da-nang",         "Đà Nẵng"],
#     18: ["dien-bien"        "Điện Biên"],
#     19: ["dong-nai",        "đồng nai"],
#     20: ["dong-thap",       "Đồng Tháp"],
#     21: ["gia-lai",         "Gia Lai"],
#     22: ["ha-giang",        "Hà Giang"],
#     23: ["hai-duong",       "Hải Dương"],
#     24: ["hai-phong",       "Hải Phòng"],
#     25: ["ha-nam",          "Hà Nam"],
#     26: ["ha-noi",          "hà nội"],
#     27: ["ha-tinh",         "Hà Tĩnh"],
#     28: ["hau-giang"        "Hậu Giang"],
#     29: ["hoa-binh",        "Hoà Bình"],
#     30: ["ho-chi-minh",     "hồ chí minh"],
#     31: ["hung-yen",        "Hưng Yên"],
#     32: ["khanh-hoa",       "Khánh Hoà"],
#     33: ["kien-giang",      "Kiên Giang"],
#     34: ["kon-tum",         "Kon Tum"],
#     35: ["lai-chau",        "Lai Châu"],
#     36: ["lam-dong",        "Lâm Đồng"],
#     37: ["lang-son",        "Lạng Sơn"],
#     38: ["lao-cai",         "Lào Cai"],
#     39: ["long-an",         "Long An"],
#     40: ["nam-dinh",        "Nam Định"],
#     41: ["nghe-an",         "Nghệ An"],
#     42: ["ninh-binh",       "Ninh Bình"],
#     43: ["ninh-thuan",      "Ninh Thuận"],
#     44: ["phu-tho",         "Phú Thọ"],
#     45: ["phu-yen",         "Phú Yên"],
#     46: ["quang-binh",      "Quảng Bình"],
#     47: ["quang-nam",       "Quảng Nam"],
#     48: ["quang-ngai",      "Quảng Ngãi"],
#     49: ["quang-ninh",      "Quảng Ninh"],
#     50: ["quang-tri",       "Quảng Trị"],
#     51: ["soc-trang",       "Sóc Trăng"],
#     52: ["son-la",          "Sơn La"],
#     53: ["tay-ninh",        "Tây Ninh"],
#     54: ["thai-binh",       "Thái Bình"],
#     55: ["thai-nguyen",     "Thái Nguyên"],
#     56: ["thanh-hoa",       "Thanh Hoá"],
#     57: ["thua-thien-hue",  "huế"],
#     58: ["tien-giang",      "Tiền Giang"],
#     59: ["tra-vinh",        "Trà Vinh"],
#     60: ["tuyen-quang",     "Tuyên Quang"],
#     61: ["vinh-long",       "Vĩnh Long"],
#     62: ["vinh-phuc",       "Vĩnh Phúc"],
#     63: ["yen-bai",         "Yên Bái"]
# }


PROVINCES = [
    30
]

MAX_SCROLL   = 5




# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mogi_vn (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'mogi_vn.middlewares.MogiVnSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'mogi_vn.middlewares.MogiVnDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'mogi_vn.pipelines.MogiVnPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
