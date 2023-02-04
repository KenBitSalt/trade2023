def activate_ts_pro():
    #初始化pro接口
    token = 'edde8271b419fde9edbb0cfba7e223476af8286db034fc4f7ae10556'
    ts.set_token(token)
    pro = ts.pro_api(token)

def get_stocknames():
    names = pd.read_parquet('stock_config.gzip')['instrument_id'].to_numpy()
    return names

def get_stockstarts():
    starts = names = pd.read_parquet('stock_config.gzip')['list_date'].to_numpy()
    return starts

if __name__ == "__main__":
    import os
    import argparse
    import json
    import tushare as ts
    import pandas as pd
    import json
    import datetime
    from datetime import datetime
    import argparse

    activate_ts_pro()
    stock_names = get_stocknames()
    print(stock_names)
