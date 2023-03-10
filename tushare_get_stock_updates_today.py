def concat_2_df(df1, df2):
    result = pd.concat([df1, df2], axis=0)
    return result

# if stock already exists, update by concating to it, 
# if stock not exist, create new csv and save it
def update_df_to_dir(df, parquet_name, directory):
    target_save = directory+'/'+parquet_name
    #print(target_save)
    if os.path.isfile(target_save):
        concat_2_df(df, pd.read_parquet(target_save)).to_parquet(parquet_name, index=False)
    else:
        df.to_parquet(parquet_name, index=False)

def get_1day_path():
    with open('config.json', 'r') as j:
        config_df = json.loads(j.read())
    datapath = config_df['path']+ '/' + config_df['data_storage'] +'/' + '1day'
    #print('Using Storage at: %s' % datapath)
    return datapath

def update_1day(stock,path,date):
    base_dir = os.getcwd()  # memorize current dir as base dir
    if os.path.exists(path):
        os.chdir(path)
        #print('going to: %s' % path)
    else:
        os.makedirs(path)
        os.chdir(path)
        #print('Creating and going to: %s' % path)
    df = pro.daily(ts_code=stock, start_date=date, end_date=date)

    if df.shape[0] >= 1:  # if today's data exists
        parquet_name = stock+'.gzip'
        #print('updating daily data to dir: %s\%s' % (os.getcwd(),csv_name))
        update_df_to_dir(df, parquet_name, os.getcwd())
        os.chdir(base_dir)  # go back to base dir
    
    else:
        print('data is not significant, shape is: ')
        #print(df.shape)
        os.chdir(base_dir)  # go back to base dir

def get_1min_path():
    with open('config.json', 'r') as j:
        config_df = json.loads(j.read())
    datapath = config_df['path']+ '/' + config_df['data_storage'] +'/' + '1min'
    #print('Using Storage at: %s' % datapath)
    return datapath

def activate_ts_pro():
    # 初始化pro接口
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
    import argparse

    parser = argparse.ArgumentParser(description='store 1 day and 1 min data of stock into data directory')
    parser.add_argument('-s', '--stock_id', help='stock_id of interest')
    args = parser.parse_args()
    
    today = datetime.today().strftime('%Y%m%d') 
    #print('today is: %s' % today)

    pro = activate_ts_pro()

    # 目标股票：
    stock_id = args.stock_id
    update_1day(stock_id, get_1day_path(), today)
    #store_1min(stock_id, get_1min_path(), today)


