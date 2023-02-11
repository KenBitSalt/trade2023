
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
            close_df = close_df.sort_values(by = 'trade_date').reset_index(drop=True)
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

def get_coint_portfolio(y, X):
    clf = linear_model.Lasso(alpha=0.00001, positive=True)
    clf.fit(X,y)
    return clf.coef_

def gen_non_neg_raw_weight(index_close_df, comp_close_df):
    raw_weight_np = get_coint_portfolio(index_close_df['close'], comp_close_df)
    raw_weight_df = pd.DataFrame(raw_weight_np)
    raw_weight_df.columns = ['raw_weight']
    raw_weight_df['instrument_id'] = comp_close_df.columns
    raw_weight_df = raw_weight_df[raw_weight_df['raw_weight']>0].sort_values('raw_weight').reset_index(drop=True)
    return raw_weight_df

def normalize_raw(raw_df):
    result = raw_df
    result['normal_weight'] = result['raw_weight']/sum(result['raw_weight'])
    return result, sum(result['raw_weight'])

def add_premium_to_index(index_close_df, premium):
    premium_perday = premium/251
    index_close_multi = [1]
    for i in range(len(index_close_df)-1):
        index_close_multi.append(index_close_multi[i]*(1+premium_perday))
    index_close_multi = np.array(index_close_multi)
    index_close_df['close'] = index_close_df['close']*index_close_multi
    return index_close_df

def plot_result(normalized_weight_df, index_pure_close_df, index_close_df, comp_close_df, days):
    total = np.zeros(len(index_close_df))
    for i in range(len(normalized_weight_df)):  # for each stock, add their contributions
        raw = normalized_weight_df.loc[i,'raw_weight']
        id = normalized_weight_df.loc[i,'instrument_id']
        contribution  = comp_close_df.loc[:,id]*raw
        total = total+contribution

    factor = total[0]/index_pure_close_df.loc[0,'close']
    total = total/factor

    plt.plot(total,label='portfolio')
    plt.plot(index_close_df['close'],label='target')
    plt.plot(index_pure_close_df['close'],label='000905.SH')
    plt.axvline(x = days, color = 'black', label = 'train-test division')
    plt.legend()
    plt.show()
    return np.nan

def calculate_error(normalized_weight_df, index_pure_close_df, index_close_df, comp_close_df, train_days):
    total = np.zeros(len(index_close_df))
    for i in range(len(normalized_weight_df)):  # for each stock, add their contributions
        raw = normalized_weight_df.loc[i,'raw_weight']
        id = normalized_weight_df.loc[i,'instrument_id']
        contribution  = comp_close_df.loc[:,id]*raw
        total = total+contribution

    factor = total[0]/index_pure_close_df.loc[0,'close']
    total = np.array(total/factor)[train_days:]
    target = index_close_df["close"].to_numpy()[train_days:]
    error = np.var(total-target)
    return error

def split_df_train_test(label, train, days):
    return label[:days], train[:days], label[days:], train[days:]


def run(index_code, start_date, end_date, premium):
    index_close_df = get_index_close(index_code, start=start_date, end=end_date).sort_values("trade_date").reset_index(drop=True)
    index_pure_close_df = index_close_df.copy()

    comp_names = get_index_comp(index_code, end="20221230")["con_code"].to_list()
    index_close_df = add_premium_to_index(index_close_df, premium)  # with premium to index added

    print('original index is:')
    print(index_pure_close_df)
    print('Index added with premium is:')
    print(index_close_df)
    print()
    print("The index has %s components" % len(comp_names))
    print()

    # all constituients need to be present all along the window
    comp_close_df = get_comp_close(comp_names, start=start_date, end=end_date)
    comp_close_df.columns = comp_names
    comp_close_df = comp_close_df.dropna(axis = 1)  
    
    """
    a portfolio selection process is needed
    """
    print(comp_close_df.shape)

    # a training and test process
    error_list = []
    non_consider_headtime = 30
    for i in tqdm(range(non_consider_headtime,len(comp_close_df)-300)):
        train_days = i
        y, X, test_y,test_X = split_df_train_test(index_close_df, comp_close_df, train_days)
        # producing predictions
        raw_weight_df = gen_non_neg_raw_weight(y, X)
        normalized_weight_df, normalization_factor = normalize_raw(raw_weight_df)
        error = calculate_error(normalized_weight_df, index_pure_close_df, index_close_df, comp_close_df, train_days)
        error_list.append(error)

    plt.plot(error_list)
    plt.show()
    tmp = min(error_list)
    index = error_list.index(tmp)+non_consider_headtime
    print(index)

    plot_result(normalized_weight_df, index_pure_close_df, index_close_df, comp_close_df, index)

    
if __name__ == "__main__":
    import os
    import pandas as pd
    import numpy as np
    import tushare as ts
    from tqdm import tqdm
    import statsmodels.tsa.stattools as tsa
    from sklearn import linear_model
    import statsmodels.api as sm
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

    run(index_code, start_date, end_date, 0.05)

    