
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

if __name__ == "__main__":
    import tushare as ts
    import matplotlib.pyplot as plt
    import argparse
    pro = activate_ts_pro()

    # get the index data using Tushare
    index_code = '000852.SH' # specify the code for the index
    start_date = '20180101' # specify the start date
    end_date = '20181010' # specify the end date


    index_close = get_index_close(index_code, start=start_date, end=end_date)
    performance_df = get_index_comp(index_code, end="20221230")['']
    print(performance_df)