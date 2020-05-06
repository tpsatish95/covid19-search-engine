# -*- coding: utf-8 -*-
"""
This script was borrowed from the RISJbot repository (https://github.com/pmyteh/RISJbot)
All credit goes to original author
"""

import logging
from scrapy.exceptions import NotConfigured

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

logger = logging.getLogger(__name__)

class WordCount(object):
    def process_item(self, item, spider):
        try:
            item['wordcount'] = len(item['bodytext'].split())
        except KeyError:
            pass
        return item
