import xgboost as xgb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# load the training data
df = pd.read_csv("stock_data.csv")

# create the label as the next day's price
df['label'] = df['price'].shift(-1)
df = df.dropna()

# split the data into training and validation sets
train_df = df[:int(df.shape[0] * 0.8)]
val_df = df[int(df.shape[0] * 0.8):]

# split the data into features (X) and labels (y)
X_train = train_df[['price', 'volume']]
y_train = train_df['label']
X_val = val_df[['price', 'volume']]
y_val = val_df['label']

# convert the data into DMatrix format, which is the format XGBoost accepts
dtrain = xgb.DMatrix(data=X_train, label=y_train)
dval = xgb.DMatrix(data=X_val, label=y_val)

# set the XGBoost hyperparameters
params = {
    'max_depth': 3,
    'eta': 0.1,
    'objective': 'reg:linear'
}

# train the XGBoost model
model = xgb.train(params, dtrain, num_boost_round=100, 
                  evals=[(dval, "Validation")], 
                  early_stopping_rounds=10, 
                  verbose_eval=False)

# make predictions on the validation set
val_predictions = model.predict(dval)

# calculate the error of the model
error = mean_squared_error(y_val, val_predictions)
print("Validation MSE: ", error)

# plot the prediction versus ground truth
plt.plot(y_val.values, label='Ground Truth')
plt.plot(val_predictions, label='Prediction')
plt.legend()
plt.show()

# make predictions on new data
new_data = np.array([[50, 1000], [100, 2000]])
new_dmatrix = xgb.DMatrix(data=new_data)
predictions = model.predict(new_dmatrix)

print("Predictions: ", predictions)
