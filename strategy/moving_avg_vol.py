import pandas as pd
import numpy as np

def generate_signals(data):
    # Calculate simple moving average
    short_rolling_mean = data['Close'].rolling(window=20).mean()
    long_rolling_mean = data['Close'].rolling(window=50).mean()
    
    # Calculate volume moving average
    vol_short_rolling_mean = data['Volume'].rolling(window=20).mean()
    vol_long_rolling_mean = data['Volume'].rolling(window=50).mean()
    
    # Generate signals
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0
    signals['short_mavg'] = short_rolling_mean
    signals['long_mavg'] = long_rolling_mean
    signals['vol_short_mavg'] = vol_short_rolling_mean
    signals['vol_long_mavg'] = vol_long_rolling_mean
    
    signals['signal'][20:] = np.where(
    (short_rolling_mean[20:] > long_rolling_mean[20:]) &
    (vol_short_rolling_mean[20:] > vol_long_rolling_mean[20:]), 1.0, 0.0)
    
    # Generate trading orders
    signals['positions'] = signals['signal'].diff()
    
    return signals

# Load daily data
data = pd.read_csv("daily_data.csv")

# Generate signals
signals = generate_signals(data)

# Print signals
print(signals)



