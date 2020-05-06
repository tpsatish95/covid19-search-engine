import scrapy


class BaltimoreSunSpider(scrapy.Spider):
    name = 'baltimore_sun_spider'
    start_urls = ['https://www.baltimoresun.com/search/coronavirus/100-y/ALL/score/1/']

    def parse(self, response):
        SET_SELECTOR = '.div'
        for content in response.css(SET_SELECTOR):
            NAME_SELECTOR = 'h3 ::text'
            yield {
                'name': content.css(NAME_SELECTOR).extract_first()
            }
