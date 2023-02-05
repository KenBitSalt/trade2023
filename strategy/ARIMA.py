import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA

# load the training data
df = pd.read_csv("stock_data.csv")

# create the label as the next day's price
df['label'] = df['price'].shift(-1)
df = df.dropna()

# split the data into training and validation sets
train_df = df[:int(df.shape[0] * 0.8)]
val_df = df[int(df.shape[0] * 0.8):]

# split the data into features (X) and labels (y)
X_train = train_df['price']
y_train = train_df['label']
X_val = val_df['price']
y_val = val_df['label']

# fit an ARIMA model on the training data
model = ARIMA(X_train, order=(3, 1, 2))
model_fit = model.fit()

# make predictions on the validation set
val_predictions = model_fit.predict(start=len(X_train), end=len(X_train)+len(X_val)-1, typ='levels')

# calculate the error of the model
error = mean_squared_error(y_val, val_predictions)
print("Validation MSE: ", error)

# plot the prediction versus ground truth
plt.plot(y_val.values, label='Ground Truth')
plt.plot(val_predictions, label='Prediction')
plt.legend()
plt.show()

# make predictions on new data
new_data = np.array([50, 100])
predictions = model_fit.predict(start=len(df), end=len(df)+len(new_data)-1, typ='levels')

print("Predictions: ", predictions)
