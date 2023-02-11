import tushare as ts
import pandas as pd
from tqdm import tqdm
import numpy as np
import statsmodels.tsa.stattools as smts
import matplotlib.pyplot as plt

# set up the Tushare Pro API
ts.set_token('edde8271b419fde9edbb0cfba7e223476af8286db034fc4f7ae10556')
pro = ts.pro_api()

# specify the code for the index
index_code = '000905.SH'

# get the constituents of the index using Tushare Pro
index_constituents = pro.index_weight(index_code=index_code)

# get the daily data for the constituents
start_date = '20210101'
end_date = '20211231'
constituents_data = pd.DataFrame()
for ts_code in tqdm(index_constituents['con_code']):
    stock_data = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    constituents_data[ts_code] = stock_data['close']

# calculate the returns for each constituent
returns = constituents_data.pct_change().dropna()

# calculate the correlation between each constituent and the index
correlation = returns.corrwith(returns['000905.SH'])

# select the top N constituents with the highest correlation and positive returns
N = 10
top_constituents = correlation[(correlation >= 0) & (returns.mean() >= 0)].nlargest(N).index

# create the refined portfolio using the top N constituents
refined_portfolio = constituents_data[top_constituents].mean(axis=1)

# perform cointegration test on the refined portfolio and the index
result = smts.coint(refined_portfolio, constituents_data['000905.SH'])
print("Cointegration test p-value: ", result[1])

# add a 5% premium to the tracked index
index_premium = (constituents_data['000905.SH'] * 1.05).dropna()

# plot the refined portfolio and the tracked index with premium
plt.plot(refined_portfolio, label='Refined Portfolio')
plt.plot(index_premium, label='Index with 5% Premium')
plt.legend()
plt.show()




