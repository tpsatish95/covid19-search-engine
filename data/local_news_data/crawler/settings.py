# -*- coding: utf-8 -*-

# Scrapy settings for COVID resources-search-engine project
#
# This file contains only settings considered important or
# commonly used. More settings available in documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

from data.local_news_data.crawler.items import NewsItem
from scrapy.utils.project import data_path
from pathlib import Path
import os
import logging

BOT_NAME = 'covid_search_engine'
LOG_LEVEL = 'INFO' # ('DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL') 

SPIDER_MODULES = ['data.local_news_data']
NEWSPIDER_MODULE = 'data.local_news_data'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# Note that if this is left unset (which uses a default Scrapy UA) then your
# crawler may be blocked from the start.
USER_AGENT = 'CovidLocalNewsBot (https://github.com/tpsatish95/covid19-search-engine)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

FEED_URI = str(Path.cwd())+'/data/local_news_data/jsonloutput/%(name)s/%(time)s-%(name)s.jsonl'
FEED_FORMAT = 'jsonlines'
# FEED_EXPORT_FIELDS = list(NewsItem().fields.keys()) # Critical for CSV
FEED_STORE_EMPTY = True
FEED_EXPORT_ENCODING = 'utf-8'
# FEED_EXPORT_ENCODING = None # UTF-8 except for JSON, which is ASCII-escaped

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# Note especially that high numbers are "close to the spider" (first to handle
# Requests, last to handle Responses) and low numbers are "close to the engine"
# (vice-versa)
SPIDER_MIDDLEWARES = {
    # NOTE: Subclassed as downloader middleware in a gross hack by
    #       OffsiteDownloaderShim. Don't load twice.
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
    # Note: Should be before RefetchControl, to ensure that fetch gets logged:
    'data.local_news_data.crawler.spmiddlewares.fake404.Fake404': 222,
    # Note: Should be before any middleware which discards <scripts>:
    'data.local_news_data.crawler.spmiddlewares.extractjsonld.ExtractJSONLD': 300,
    'data.local_news_data.crawler.spmiddlewares.refetchcontrol.RefetchControl': 800,
    # Note: Should be after RefetchControl, to ensure that the URLs stored
    #       are the altered "canonical" ones.
    'data.local_news_data.crawler.spmiddlewares.equivalentdomains.EquivalentDomains': 900,
    'data.local_news_data.crawler.spmiddlewares.unwantedcontent.UnwantedContent': 950,
}

# Enable RefetchControl, 8 fetches total, every 3 hours, including a
# trawl of previously-fetched pages for completeness (TN, 2017-03-15)
REFETCHCONTROL_ENABLED = True
REFETCHCONTROL_MAXFETCHES = 8
REFETCHCONTROL_REFETCHSECS = 10800
REFETCHCONTROL_REFETCHFROMDB = True
REFETCHCONTROL_TRIMDB = True
REFETCHCONTROL_RQCALLBACK = 'spider.parse_page'
REFETCHCONTROL_DIR = data_path('RefetchControl', createdir=True)

# Enable UnwantedContent, stripping figures etc. (TN, 2017-02-27)
UNWANTEDCONTENT_ENABLED = True
UNWANTEDCONTENT_XPATHS = ['//figure',
                          '//script',
                          '//style',
                          '//form',]

# Enable Fake404, dropping responses that are actually "page not found",
# but come with an improper HTTP 200 success code. Lookin' at you, foxnews.com.
FAKE404_ENABLED = True
# List of ( url regex, matching xpath ) tuples
FAKE404_DETECTIONSIGS = [
    ( r'https?://(www\.)?foxnews\.com/',
        '//h1[contains(., "Something has gone wrong")]'),
    ( r'https?://(www\.)?nbcnews\.com/',
        '//h2[contains(., "This live stream has ended")]'),
]

# Enable ExtractJSONLD; extract JSON-LD encoded metadata (TN, 2017-03-03)
EXTRACTJSONLD_ENABLED = True

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'data.local_news_data.crawler.dlmiddlewares.offsitedownloadershim.OffsiteDownloaderShim': 100,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'data.local_news_data.crawler.dlmiddlewares.stripnull.StripNull': 543,
}

# AP returns responses with ASCII NUL bytes embedded in them.
# This is very bad for Scrapy's parsing code. Strip them.
STRIPNULL_ENABLED = True

# Map all 'www.cnn.com' URLs to the equivalent 'edition.cnn.com' (dedupe)
# TN, 2017/03/27
EQUIVALENTDOMAINS_ENABLED = True
EQUIVALENTDOMAINS_MAPPINGS = {'www.cnn.com': 'edition.cnn.com'}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'data.local_news_data.crawler.pipelines.sentiment.Sentiment': 100,
    'data.local_news_data.crawler.pipelines.wordcount.WordCount': 200,
# Removed from pipeline to reduce DotscrapyPersistence S3 usage, TN 2017-04-06
#    'RISJbot.pipelines.namedpeople.NamedPeople': 300,
#    'RISJbot.pipelines.readingage.ReadingAge': 400,
    'data.local_news_data.crawler.pipelines.checkcontent.CheckContent': 800,
    'data.local_news_data.crawler.pipelines.striprawpage.StripRawPage': 900,
}

# Flag to determine storage of rawpagegzipb64 (to turn off for debugging)
# TN 2017/03/27
STRIPRAWPAGE_ENABLED = True

# A contract promising *not* to collect data for a particular field
# Currently not set up
# TN: 2017-02-27
# SPIDER_CONTRACTS = {
#     'data.local_news_data.crawler.contracts.NoScrapesContract': 10,
# }
