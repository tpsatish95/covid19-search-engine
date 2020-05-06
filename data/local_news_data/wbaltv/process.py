"""
Script to format WBALTV data into .I .T .W
"""
import pandas as pd
import os
from data.local_news_data.utils.process import clean_raw


def main():
    path = '.'
    filename = 'wbaltv.csv'
    clean_raw(path, filename, 'WBALTV.ALL')


if __name__ == '__main__':
    main()
