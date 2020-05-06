"""
Script to format CBS data into .I .T .W
"""
import pandas as pd
import os
from utils.process import clean_raw


def main():
    path = '.'
    filename = 'baltimore.cbslocal.csv'
    clean_raw(path, filename, 'CBS.ALL')


if __name__ == '__main__':
    main()
