import tushare as ts
token = 'edde8271b419fde9edbb0cfba7e223476af8286db034fc4f7ae10556'
ts.set_token(token)
pro = ts.pro_api(token)
print('using tushare at version: %s' % ts.__version__)


def get_index_weight(id):
    # 拉取数据
    df = pro.index_weight(**{
        "index_code": id,
        "trade_date": "",
        "start_date": "",
        "end_date": "",
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

def get_index_perf(id):
    # 拉取数据
    df = pro.index_daily(**{
        "ts_code": id,
        "trade_date": "",
        "start_date": "",
        "end_date": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "ts_code",
        "trade_date",
        "close",
        "open",
        "high",
        "low",
        "pre_close",
        "change",
        "pct_chg",
        "vol",
        "amount"
    ])

    return df

def process_raw_weight(df):
    result = []
    return result

weight_df = get_index_weight('000852.SH')
performance_df = get_index_perf('000852.SH')
print(performance_df)