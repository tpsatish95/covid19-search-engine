# -*- coding: utf-8 -*-
"""
This script was borrowed from the RISJbot repository (https://github.com/pmyteh/RISJbot)
All credit goes to original author
"""

import logging

logger = logging.getLogger(__name__)


class CheckContent(object):
    def process_item(self, item, spider):
        if 'bodytext' not in item:
            u = item.get('url')
            if 'picture' not in u and 'video' not in u and 'gallery' not in u:
                logger.error("No bodytext: {}".format(u))
        return item
