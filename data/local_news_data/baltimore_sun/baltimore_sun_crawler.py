import argparse
import logging
import re
from queue import PriorityQueue
from urllib import parse, request

import pandas as pd
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG, filename='output.log', filemode='w')
visitlog = logging.getLogger('visited')


def parse_links(root, html):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            text = link.string
            if not text:
                text = ''
            text = re.sub(r'\s+', ' ', text).strip()
            yield (parse.urljoin(root, link.get('href')), text)


def get_links(url):
    res = request.urlopen(url)
    return list(parse_links(url, res.read()))


def get_domain(url):
    return parse.urlparse(url).netloc


def get_search_path(url):
    if len(parse.urlparse(url).path.split('/')) > 2:
        return '/'.join(parse.urlparse(url).path.split('/')[:-2])
    return None


def get_non_self_referencing(url):
    '''Get a list of links on the page specificed by the url,
    but only keep non-local links and non self-references.
    Return a list of (link, title) pairs, just like get_links()'''

    args = get_args()
    domain = get_domain(args.site)
    links = get_links(url)
    filtered = []
    for link, title in links:
        if parse.urlparse(link).netloc == domain:
            if len(parse.urlparse(link).fragment) == 0:
                filtered.append((link, title))  # get non self-referencing
    return filtered


def crawl(root, within_domain, wanted_content=None):
    '''Crawl the url specified by `root`.
    `wanted_content` is a list of content types to crawl
    `within_domain` specifies whether the crawler should limit itself to the domain of `root`
    '''
    args = get_args()
    queue = PriorityQueue()
    queue.put((1, root))
    search_path = get_search_path(root)
    iteration = 0

    visited = []
    scraped = []

    df = pd.DataFrame(columns=['url', 'title', 'body'])

    while not queue.empty():
        url = queue.get()[1]
        if url in visited:
            continue
        if iteration > args.max_iterations:
            break
        print(url)
        try:
            req = request.urlopen(url)

            content_type = req.info().get_content_type()
            if wanted_content and content_type not in wanted_content:
                continue
            visited.append(url)
            visitlog.debug(url)
            iteration += 1

            for link, title in get_non_self_referencing(url):
                if get_search_path(link) == search_path:
                    if link not in visited:
                        priority = int(parse.urlparse(link).path.split('/')[-2])
                        queue.put((priority, link))
                elif 'search' not in parse.urlparse(link).path:
                    if link not in scraped:
                        try:
                            df = df.append(scrape(link))
                            scraped.append(link)
                        except Exception as e:
                            print(e, link)
            df.to_csv('baltimore.sun.csv', index=False)

        except Exception as e:
            print(e, url)

    return visited, scraped


def scrape(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find('h1').get_text()
    article = soup.find(
        'div', attrs={'class': 'wrapper clearfix full pb-feature pb-layout-item pb-f-article-body'})
    print(title)
    content = []
    for div in article.find_all('div', {'data-type': ['header', 'text', 'list']}):
        content.append(div.get_text().strip())
    return pd.DataFrame({'url': [url], 'title': [title], 'body': [' '.join(content)]})


def get_args():
    parser = argparse.ArgumentParser(description="Web crawler")
    parser.add_argument('site', help='The URL to crawl', type=str)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    # site = 'https://www.baltimoresun.com/search/coronavirus/100-y/ALL/score/1/'
    visited, extracted = crawl(args.site, True)


if __name__ == '__main__':
    main()
