def update_daily():
    # read the 'can_update' parameter in the config json file
    update_list = get_all_stocknames()
    print(update_list)
    if check_can_update():
        print("updating daily data to stocks...")
        for stock_id in tqdm(update_list):
            subprocess.call(('%s tushare_get_stock_updates_today.py -s %s' % ('python', stock_id)), shell=True)
    
def check_can_update():
    with open('config.json', 'r') as j:
        config_df = json.loads(j.read())
    ud = config_df['can_update']
    return ud

def change_can_update():
    pass

def get_all_stocknames():
    df = pd.read_parquet("stock_config.gzip")
    return df['instrument_id'].to_numpy()

def activate_ts_pro():
    # 初始化pro接口
    token = 'edde8271b419fde9edbb0cfba7e223476af8286db034fc4f7ae10556'
    ts.set_token(token)
    pro = ts.pro_api(token)

def is_today_tradeday(today_date):
    pass

if __name__ == "__main__":
    import os
    import time
    import subprocess
    import json
    import tushare as ts
    import pandas as pd
    import json
    import datetime
    from datetime import datetime
    import argparse
    from tqdm import tqdm

    pro = activate_ts_pro()

    today = datetime.today().strftime('%Y%m%d') 
    #print('today is: %s' % today)

    is_trade = is_today_tradeday(today)

    with open('config.json', 'r') as j:
        config_df = json.loads(j.read())
    can_update = False
    update_daily()

    
                

