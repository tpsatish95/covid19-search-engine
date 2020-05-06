"""
Script to format data into .I .T .W
"""
import pandas as pd
import os
from crawler.utils import clean_raw, process_jsonl


def main():
    df = process_jsonl(filename='jsonloutput/cbs/2020-05-06T17-58-56-cbs.jsonl')
    df.to_csv('cbs/baltimore.cbslocal.csv', index=False)

    df = process_jsonl(filename='jsonloutput/wbaltv/2020-05-06T18-55-36-wbaltv.jsonl')
    df.to_csv('wbaltv/wbaltv.csv', index=False)

    clean_raw(path='cbs', filename='baltimore.cbslocal.csv', new_filename='CBS.ALL')
    clean_raw(path='wbaltv', filename='wbaltv.csv', new_filename='WBALTV.ALL')


if __name__ == '__main__':
    main()
