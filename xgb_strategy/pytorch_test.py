import torch
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.model_selection import GridSearchCV

# Print PyTorch version
print(f"PyTorch version: {torch.__version__}")

# Check if CUDA is available and use it if possible
if torch.cuda.is_available():
    print("CUDA is available. Using GPU for model training.")
    device = torch.device("cuda")
    print(f"GPU model: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is not available. Using CPU for model training.")
    device = torch.device("cpu")



# Read in stock data from Parquet file
data = pd.read_parquet("D:/trade2023/trade/market_data/1day/000002.SZ.gzip")

#print(data)
param_grid = {
    'max_depth': [3, 4, 5, 6],
    'learning_rate': [0.5, 0.1, 0.05, 0.01, 0.001],
    'n_estimators': [50, 100, 200]
}

# Define features and target variables
features = ["open", "high", "low", "vol"]
target = "close"

# Split data into training and testing sets
train_size = int(data.shape[0] * 0.8)
train_data = data.iloc[:train_size]
test_data = data.iloc[train_size:]

# Initialize XGBoost model
model = xgb.XGBRegressor(objective='reg:squarederror')

# Use GridSearchCV to search over the parameter grid and find the best hyperparameters
grid_search = GridSearchCV(model, param_grid, cv=5)
grid_search.fit(train_data[features],train_data[target])

# Print the best hyperparameters and their corresponding score
print("Best parameters: ", grid_search.best_params_)
print("Best score: ", grid_search.best_score_)


'''
model.fit(train_data[features], train_data[target])

# Make predictions on testing data
predictions = model.predict(test_data[features])

# Compute MSE and RMSE of predictions
mse = mean_squared_error(test_data[target], predictions)
rmse = sqrt(mse)

# Print results
print(f"MSE: {mse:.2f}")
print(f"RMSE: {rmse:.2f}")
'''
# Train model on training data
