import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

def find_spread(y, x):
    model = sm.OLS(y, x)
    results = model.fit()
    spread = y - results.predict(x)
    return spread

def zscore(spread):
    return (spread - spread.mean()) / spread.std()

def find_pairs(prices):
    # Calculate the returns for each stock
    returns = prices.pct_change().dropna()
    
    # Calculate the pairwise correlation matrix
    corr = returns.corr()
    
    # Find pairs with a high degree of correlation
    pairs = [(symbol1, symbol2) for symbol1 in corr.columns for symbol2 in corr.columns if symbol1 < symbol2 and abs(corr[symbol1][symbol2]) > 0.8]
    
    # Calculate the spread for each pair and apply a Z-score to find opportunities
    opportunities = []
    for symbol1, symbol2 in pairs:
        y = returns[symbol1]
        x = returns[symbol2]
        spread = find_spread(y, x)
        zscore = zscore(spread)
        if zscore.abs().iloc[-1] > 2:
            opportunities.append((symbol1, symbol2, zscore))
    
    # Sort the opportunities by Z-score and display the top results
    opportunities.sort(key=lambda x: x[2].abs().iloc[-1], reverse=True)
    for symbol1, symbol2, zscore in opportunities[:10]:
        print("Opportunity found:", symbol1, symbol2)
        plt.figure(figsize=(10, 5))
        zscore.plot()
        plt.title(f"Spread ({symbol1} - {symbol2})")
        plt.xlabel("Date")
        plt.ylabel("Z-Score")
        plt.axhline(zscore.mean(), color="black", linestyle="--")
        plt.axhline(2, color="red", linestyle="--")
        plt.axhline(-2, color="red", linestyle="--")
        plt.show()

# Load daily price data for a set of stocks
prices = pd.read_csv("stock_prices.csv", index_col=0, parse_dates=True)

# Find pairs trading opportunities
find_pairs(prices)
