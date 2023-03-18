def activate_ts_pro():
    #初始化pro接口
    token = 'edde8271b419fde9edbb0cfba7e223476af8286db034fc4f7ae10556'
    ts.set_token(token)
    pro = ts.pro_api(token)
    return pro

def get_1day_path():
    with open('config.json', 'r') as j:
        config_df = json.loads(j.read())
    datapath = config_df['path']+ '/' + config_df['data_storage'] +'/' + '1day'
    #print('Using Storage at: %s' % datapath)
    return datapath

def get_stockconfig():
    datapath = 'trade2023/stock_config.gzip'
    df = pd.read_parquet(datapath)
    #print('Using Storage at: %s' % datapath)
    return df

def get_historical(stock_lists,today_date):
    print(stock_lists)
    
    #df = pro.daily(ts_code=stock, start_date=date, end_date=date)
    for i in tqdm(range(len(stock_lists))):
        id = stock_lists.loc[i,'instrument_id']
        start_date = stock_lists.loc[i,'list_date']
        end_date = today_date
        df = pro.daily(ts_code=id, start_date=start_date, end_date=end_date)
        path = (get_1day_path())
        save_name = path+'/'+id+'.gzip'
        df.to_parquet(save_name)
        stock_lists.loc[:,'latest_update'] = today_date

    stock_lists.to_parquet('stock_config.gzip')


if __name__ == "__main__":
    import os
    import argparse
    import json
    from tqdm import tqdm
    import tushare as ts
    import pandas as pd
    import json
    import datetime
    from datetime import datetime

    pro = activate_ts_pro()
    daily_path = get_1day_path()
    stocks = pd.read_parquet("stock_config.gzip")
    today = datetime.today().strftime('%Y%m%d') 
    get_historical(stocks,today)



