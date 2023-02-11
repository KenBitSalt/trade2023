
def activate_ts_pro():
    token = 'edde8271b419fde9edbb0cfba7e223476af8286db034fc4f7ae10556'
    ts.set_token(token)
    pro = ts.pro_api(token)
    print('using tushare at version: %s' % ts.__version__)
    return pro


def get_index_comp(id,end):
    df = pro.index_weight(**{
        "index_code": id,
        "trade_date": "",
        "start_date": end,
        "end_date": end,
        "limit": "",
        "offset": ""
    }, fields=[
        "index_code",
        "con_code",
        "trade_date",
        "weight"
    ])
    #print(df)
    return df

def get_index_close(id,start,end):
    # 拉取数据
    df = pro.index_daily(**{
        "ts_code": id,
        "trade_date": "",
        "start_date": start,
        "end_date": end,
        "limit": "",
        "offset": ""
    }, fields=[
        "trade_date",
        "close",
    ])

    return df[["trade_date","close"]]

def get_comp_close(comp_names, start, end):
    result = []
    for comp in tqdm(comp_names):
        if os.path.exists("data/%s_%s_%s.gzip"%(comp,start,end)):
            close_df = pd.read_parquet("data/%s_%s_%s.gzip"%(comp,start,end))
        else:
            close_df = pro.daily(ts_code=comp, start_date=start, end_date=end)[['trade_date','close']]
            close_df.to_parquet("data/%s_%s_%s.gzip"%(comp,start,end))
        result.append(close_df["close"].to_numpy())

    result = pd.DataFrame(result).T
    return result

def test_tsa(refined_portfolio):
    for security in refined_portfolio.columns:
        result = tsa.adfuller(refined_portfolio[security])
        print(f"ADF test for {security}:")
        print(f"Test Statistic: {result[0]}")
        print(f"p-value: {result[1]}")
        print(f"Critical Values: {result[4]}")


def run(index_code, start_date, end_date):
    index_close_df = get_index_close(index_code, start=start_date, end=end_date)
    print(index_close_df)

    comp_names = get_index_comp(index_code, end="20221230")["con_code"].to_list()
    print()
    print("The index has %s components" % len(comp_names))
    print()
    comp_close_df = get_comp_close(comp_names, start=start_date, end=end_date)
    comp_close_df.columns = comp_names
    comp_close_df = comp_close_df.dropna(axis = 1)
    print(comp_close_df)


if __name__ == "__main__":
    import os
    import pandas as pd
    import numpy as np
    import tushare as ts
    from tqdm import tqdm
    import statsmodels.tsa.stattools as tsa
    import matplotlib.pyplot as plt

    import argparse
    parser = argparse.ArgumentParser(description='create refined portfolio using cointegration')
    parser.add_argument('-i', '--index_id', help='id of original index (e.g. 000852.SH)')
    parser.add_argument('-s', '--start', help='start date')
    parser.add_argument('-e', '--end', help='end date')
    args = parser.parse_args()

    # get the index data using Tushare
    index_code = args.index_id # specify the code for the index
    start_date = args.start # specify the start date
    end_date = args.end # specify the end date

    pro = activate_ts_pro()

    run(index_code, start_date, end_date)

    