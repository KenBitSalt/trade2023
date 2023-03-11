import talib as ta
import pandas_datareader as web
import tushare as ts
import matplotlib.pyplot as plt

def activate_ts_pro():
    # 初始化pro接口
    token = 'edde8271b419fde9edbb0cfba7e223476af8286db034fc4f7ae10556'
    ts.set_token(token)
    pro = ts.pro_api(token)
    return pro


pro = activate_ts_pro()

df = pro.daily(ts_code="002594.SZ", start_date='20050101', end_date="20230210")
df = df.sort_values('trade_date')
df = df.reset_index()

df['SMA_5'] = ta.SMA(df['close'],5)
df['SMA_10'] = ta.SMA(df['close'],10)
df['SMA_50'] = ta.SMA(df['close'],50)
df['SMA_100'] = ta.SMA(df['close'],100)
df = df.loc[100:,:]

print(df)

df.to_csv('000002.SZ.csv',index = False)


plt.plot(df['close'])
plt.plot(df['SMA_5'])
plt.plot(df['SMA_10'])

plt.show()