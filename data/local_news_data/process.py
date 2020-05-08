"""
Script to format data into .I .T .W
"""
import os

import pandas as pd

from crawler.utils import clean_raw, process_jsonl, clean_search_crawl


def main():
    # CBS Baltimore
    df = process_jsonl(filename='jsonloutput/cbs/2020-05-06T17-58-56-cbs.jsonl')
    df.to_csv('cbs/baltimore.cbslocal.csv', index=False)
    clean_raw(path='cbs', filename='baltimore.cbslocal.csv', new_filename='CBS.ALL')

    # WBALTV
    df = process_jsonl(filename='jsonloutput/wbaltv/2020-05-06T18-55-36-wbaltv.jsonl')
    df.to_csv('wbaltv/wbaltv.csv', index=False)
    clean_raw(path='wbaltv', filename='wbaltv.csv', new_filename='WBALTV.ALL')

    # Baltimore Sun
    clean_search_crawl(path='baltimore_sun', filename='baltimore.sun.csv', new_filename='BALTIMORE_SUN.ALL')


if __name__ == '__main__':
    main()
