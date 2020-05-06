# -*- coding: utf-8 -*-
from data.local_new_data.utils.newssitemapspider import NewsSitemapSpider
from data.local_new_data.utils.loaders import NewsLoader
# Note: mutate_selector_del_xpath is somewhat naughty. Read its docstring.
from data.local_new_data.utils.utils import mutate_selector_del_xpath
from scrapy.loader.processors import Identity, TakeFirst
from scrapy.loader.processors import Join, Compose, MapCompose

class CbsSpider(NewsSitemapSpider):
    name = 'cbs'
    # allowed_domains = ['cbsnews.com']
    # A list of XML sitemap files, or suitable robots.txt files with pointers.
    sitemap_urls = ['https://baltimore.cbslocal.com/sitemap.xml'] 
    # sitemap_urls = ['http://www.cbsnews.com/xml-sitemap/index/news.xml'] 
    

    def parse_page(self, response):
        """
        @url https://baltimore.cbslocal.com/sitemap.xml
        @returns items 1
        @scrapes bodytext bylines fetchtime firstpubtime modtime headline
        @scrapes keywords section source summary url
        """
        # import pdb; pdb.set_trace()
        s = response.selector
        # Remove any content from the tree before passing it to the loader.
        # There aren't native scrapy loader/selector methods for this.        
        #mutate_selector_del_xpath(s, '//*[@style="display:none"]')

        l = NewsLoader(selector=s)

        # Add a number of items of data that should be standardised across
        # providers. Can override these (for TakeFirst() fields) by making
        # l.add_* calls above this line, or supplement gaps by making them
        # below.
        l.add_fromresponse(response)
        l.add_htmlmeta()
#        l.add_schemaorg_mde(response, jsonld=True, rdfa=False, microdata=False)
        l.add_schemaorg(response)
        l.add_opengraph()
        l.add_scrapymeta(response)

        # Media pages. NOTE: These can be multipage; this will only get the
        # first page's text.
        
        l.add_xpath('bodytext', '//div[contains(@class, "article-content--body-text")]//text()')
        l.add_xpath('bodytext', '//div[contains(@class, "main-story-wrapper")]//text()')
        # l.add_xpath('bodytext', '//div[contains(@class, "post")]//text()')
        # l.add_xpath('bodytext', '//div[@itemid="#article-entry"]//text()')

        return l.load_item()
