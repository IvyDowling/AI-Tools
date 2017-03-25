import pandas as pd
import operator
import json
import sys

def run(fn):
    df = pd.read_csv(fn, na_values=["?"], thousands='.')
    df = df.fillna("?")
    sparse_dict = {k: sparse(df[k]) for k in df.head(1)}
    print(json.dumps(sorted(sparse_dict.items(), key=operator.itemgetter(1))
        , indent=2))


def sparse(col):
    i = 0
    tot = 0
    for k in col:
        if k is not "?":
            i += 1
        tot += 1
    return int((i/tot) * 100)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        print("what csv file?")
