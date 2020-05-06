import jsonlines
import os
import pandas as pd
from data.local_news_data.crawler.utils import process_jsonl


def main():
    filename = './2020-04-26T03-56-31-wbaltv.jsonl'
    df = process_jsonl(filename)
    df.to_csv(os.path.join("./", 'baltimore.cbslocal.csv'), index=False)


if __name__ == '__main__':
    main()
