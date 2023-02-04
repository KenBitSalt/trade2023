def activate_ts_pro():
    #初始化pro接口
    token = 'edde8271b419fde9edbb0cfba7e223476af8286db034fc4f7ae10556'
    ts.set_token(token)
    pro = ts.pro_api(token)
    return pro

if __name__ == "__main__":
    import os
    import argparse
    import json
    import tushare as ts
    import pandas as pd
    import json
    import datetime
    from datetime import datetime

    pro = activate_ts_pro()
    stocks = pd.read_parquet("stock_config.gzip")
    today = datetime.today().strftime('%Y%m%d') 
    print(stocks)
