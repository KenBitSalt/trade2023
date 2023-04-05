import torch
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.model_selection import GridSearchCV
import seaborn as sns
import matplotlib.pyplot as plt

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
# Create a new column called "next_close"
data["next_open"] = data["open"].shift(-1)
# Define features and target variables
features = ["open", "high", "low", "vol" , "close"]
target = "next_open"
data = data.dropna()

# Split data into training and testing sets
train_size = int(data.shape[0] * 0.8)
train_data = data.iloc[:train_size]
test_data = data.iloc[train_size:]

# Initialize XGBoost model
model = xgb.XGBRegressor(objective='reg:squarederror')

#print(data)
param_grid = {
    'max_depth': [7, 8, 9, 10, 11],
    'learning_rate': [0.2, 0.1, 0.05],
    'n_estimators': [50, 100, 200, 300]
}
# Use GridSearchCV to search over the parameter grid and find the best hyperparameters
grid_search = GridSearchCV(model, param_grid, cv=5)
grid_search.fit(train_data[features],train_data[target])

# Print the best hyperparameters and their corresponding score
print("Best parameters: ", grid_search.best_params_)
print("Best score: ", grid_search.best_score_)

learning_rate = grid_search.best_params_['learning_rate']
max_depth = grid_search.best_params_['max_depth']
n_estimators = grid_search.best_params_['n_estimators']


model = xgb.XGBRegressor(objective='reg:squarederror', 
                         learning_rate = learning_rate, 
                         max_depth = max_depth, 
                         n_estimators = n_estimators)
# Train model on training data
model.fit(train_data[features], train_data[target])
# Make predictions on testing data
predictions = model.predict(test_data[features])
# Compute MSE and RMSE of predictions
mse = mean_squared_error(test_data[target], predictions)
rmse = sqrt(mse)

test_data['predictions'] = predictions
print(test_data)

# Print results
print(f"MSE: {mse:.2f}")
print(f"RMSE: {rmse:.2f}")

# Visualize training and testing results using matplotlib
plt.plot(test_data.index,test_data['open'], color='blue')
plt.plot(test_data.index,test_data['predictions'], color='green')
plt.plot([min(predictions), max(predictions)], [min(predictions), max(predictions)], color='red')
plt.ylabel('Predictions')
plt.xlabel('True Values')
plt.xlim(min(test_data.index),max(test_data.index))
plt.title('Training (blue) vs. Testing (green) Predictions')
plt.show()


