def activate_ts_pro():
    #初始化pro接口
    token = 'edde8271b419fde9edbb0cfba7e223476af8286db034fc4f7ae10556'
    ts.set_token(token)
    pro = ts.pro_api(token)

def get_stock_conf_path():
    with open('config.json', 'r') as j:
        config_df = json.loads(j.read())
    datapath = config_df['stock_config']
    #print('Using Storage at: %s' % datapath)
    return datapath

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
    stock_conf_path = get_stock_conf_path()
    df = pd.read_parquet(stock_conf_path)
    print(df)
