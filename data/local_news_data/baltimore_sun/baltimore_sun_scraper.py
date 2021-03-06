import os
from collections import namedtuple

import pandas as pd
import requests
from bs4 import BeautifulSoup

from data.local_news_data.crawler.scraper import Scraper


class BaltimoreSunScraper(Scraper):

    def scrape(self):
        url = 'https://www.baltimoresun.com/coronavirus/bs-md-whats-open-closed-maryland-non-essential-business-20200323-rlebum7b45aw5ezcsw52p4p32m-story.html'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        Content = namedtuple('Content', 'text header hyperlink')
        content = []
        header = ''
        for div in soup.find_all('div', {'data-type': ['header', 'text']}):
            if div['data-type'] == 'header':
                header = div.get_text().strip()
                continue
            links = self.get_links(div)
            content.append(Content(div.get_text().strip(), header, links))

        df = pd.DataFrame(content)
        df.to_csv(os.path.join(self._path, self._filename), index=False)

    def get_links(self, block):
        if block.find('a'):
            return [{'text': link.text, 'link': link.get('href')} for link in block.find_all('a')]
        return None


def main():
    scraper = BaltimoreSunScraper(path='..', filename='baltimore_sun_open_closed.csv')
    scraper.scrape()


if __name__ == '__main__':
    main()
