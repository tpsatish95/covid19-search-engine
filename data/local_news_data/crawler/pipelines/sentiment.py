# -*- coding: utf-8 -*-
"""
This script was borrowed from the RISJbot repository (https://github.com/pmyteh/RISJbot)
All credit goes to original author
"""

import logging
from scrapy.exceptions import NotConfigured
from textblob import TextBlob

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

logger = logging.getLogger(__name__)

class Sentiment(object):
    """Uses textblob to determine and record sentiment and
       subjectivity scores for the bodytext of each item."""
    def process_item(self, item, spider):
        try:
            blob = TextBlob(item['bodytext'])
            item['sentiment'] = blob.sentiment.polarity
            item['subjectivity'] = blob.sentiment.subjectivity
        except KeyError:
            pass
        return item
