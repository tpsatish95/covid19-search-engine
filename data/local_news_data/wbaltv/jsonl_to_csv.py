import jsonlines
import os
import pandas as pd
from data.local_news_data.utils.jsonl_to_csv import process_jsonl


def main():
    filename = './2020-04-26T03-56-31-wbaltv.jsonl'
    df = process_jsonl(filename)
    df.to_csv(os.path.join("./", 'wbaltv.csv'), index=False)


if __name__ == '__main__':
    main()
