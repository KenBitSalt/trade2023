def create_dict(list1,list2):
    result = dict()
    return result

def activate_ts_pro():
    #初始化pro接口
    token = 'edde8271b419fde9edbb0cfba7e223476af8286db034fc4f7ae10556'
    ts.set_token(token)
    pro = ts.pro_api(token)
    return pro

def setup_stock_config(stock_array):
    pool = stock_array
    df = pd.DataFrame()
    # uodate the stocks in the pool
    for stock_id in tqdm(pool):
        df_now = pro.stock_basic(**{
        "ts_code": stock_id,
        }, fields=[
        "ts_code",
        "symbol",
        "name",
        "industry",
        "market",
        "list_date"
        ])
        df = pd.concat([df,df_now],axis = 0)
    df.columns = [
        "instrument_id",
        "symbol",
        "name",
        "industry",
        "market",
        "list_date"
        ]
    df.to_parquet("stock_config.gzip")

if __name__ == "__main__":
    import os
    import tushare as ts
    import pandas as pd
    from tqdm import tqdm
    pro = activate_ts_pro()
    stock_ids = ['000001.SZ', '000002.SZ', '000008.SZ', '000004.SZ', '000005.SZ', '002594.SZ']
    setup_stock_config(stock_ids)
    df = pd.read_parquet("stock_config.gzip")
    print(df)


        

