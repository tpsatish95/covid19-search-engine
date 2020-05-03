"""
Script to format CBS data into .I .T .W
"""
import pandas as pd
import os


def clean_raw(path, filename, new_filename):
    df = pd.read_csv(os.path.join(path, filename))
    with open(os.path.join(path, new_filename), 'w') as f:
        for i, row in df.iterrows():
            f.write('.I {}\n'.format(i + 1))
            if len(row.headline) > 0:
                f.write('.T\n{}\n'.format(row.headline))
            f.write('.W\n{}\n\n{}\n'.format(row.summary, row.bodytext))


def main():
    path = '.'
    filename = 'baltimore.cbslocal.csv'
    clean_raw(path, filename, 'CBS.ALL')


if __name__ == '__main__':
    main()
