# Scrapy settings for todostuslibros project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'todostuslibros'

SPIDER_MODULES = ['todostuslibros.spiders']
NEWSPIDER_MODULE = 'todostuslibros.spiders'

TODOSTUSLIBROS_URL_LIST = ['https://www.todostuslibros.com/materia/genero-policiaco-y-misterio_FF']
#  URLs for other categories:
#  Modern literary fiction: https://www.todostuslibros.com/materia/ficcion-moderna-y-contemporanea_FA
#  Mistery and crime: https://www.todostuslibros.com/materia/genero-policiaco-y-misterio_FF
#  Fantasy: https://www.todostuslibros.com/materia/fantasia_FM
#  Classical Science fiction: https://www.todostuslibros.com/materia/ciencia-ficcion-clasica_FLC
#  Mistery and suspense (including Stephen King): https://www.todostuslibros.com/materia/obra-de-misterio-y-suspense_FH
#  Terror and ghosts: https://www.todostuslibros.com/materia/cuentos-de-terror-y-fantasmas_FK
#
TODOSTUSLIBROS_BOOK_DETAIL_URL_TEMPLATE = 'https://www.todostuslibros.com/isbn/{isbn}'

# Feed export as JSON
FEED_EXPORTERS = {
 'jsonlines': 'scrapy.exporters.JsonItemExporter',
}
FEED_FORMAT = 'jsonlines'
FEED_URI = "todostuslibros_misterio.json"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'todostuslibros (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 20

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
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
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'todostuslibros.middlewares.TodostuslibrosSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'todostuslibros.middlewares.TodostuslibrosDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'todostuslibros.pipelines.TodostuslibrosCleanupPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
