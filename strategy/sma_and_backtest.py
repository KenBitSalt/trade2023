import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load daily price and volume data
df = pd.read_csv('daily_price_volume_data.csv')

# Calculate simple moving average (SMA) of closing prices over a specific window size
window_size = 14
df['sma'] = df['close'].rolling(window=window_size).mean()

# Create a new column to store the trading signals
df['signal'] = 0

# Generate signals based on the SMA and volume data
for i in range(len(df)):
    if df.at[i, 'volume'] > df.at[i, 'volume'].rolling(window=window_size).mean() and df.at[i, 'close'] > df.at[i, 'sma']:
        df.at[i, 'signal'] = 1
    elif df.at[i, 'volume'] < df.at[i, 'volume'].rolling(window=window_size).mean() and df.at[i, 'close'] < df.at[i, 'sma']:
        df.at[i, 'signal'] = -1

# Backtest the strategy by calculating the cumulative returns
df['returns'] = np.log(df['close'] / df['close'].shift(1))
df['strategy_returns'] = df['signal'].shift(1) * df['returns']
df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod()

# Plot the cumulative returns
plt.plot(df.index, df['cumulative_returns'])
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.title('Backtest Result')
plt.show()
