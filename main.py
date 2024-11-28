import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score

current_season_data = pd.read_csv("current_szn_data.csv")
previous_season_data = pd.read_csv("prev_szn_data.csv")

data = pd.concat([current_season_data, previous_season_data])

# remove dependent features
X = data.drop(columns=["Points", "Player", "Season", "FG%", "3P%", "FT%", "TRB"])
y = data["Points"]

# check initial shape
print(f"Initial shape of X: {X.shape}")
print(f"Initial shape of y: {y.shape}")

# combine into 1 df
data_cleaned = pd.concat([X, y], axis=1)

# clean combined df of NaN values
data_cleaned = data_cleaned.dropna()

# reset X and y into different dfs
X = data_cleaned.drop(columns=["Points"])
y = data_cleaned["Points"]

# reset indices to ensure matching
X = X.reset_index(drop=True)
y = y.reset_index(drop=True)

# check shape after cleaning
print(f"Shape of X after cleaning: {X.shape}")
print(f"Shape of y after cleaning: {y.shape}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# models
linear_model = LinearRegression()
random_forest = RandomForestRegressor(random_state = 42)
xg_boost = xgb.XGBRegressor(random_state = 42)

# training
linear_model.fit(X_train_scaled, y_train)
random_forest.fit(X_train, y_train)
xg_boost.fit(X_train, y_train)

# evaluation
linear_predictor = linear_model.predict(X_test_scaled)
rf_predictor = random_forest.predict(X_test)
xgb_predictor = xg_boost.predict(X_test)

def evaluate_model(model_name, y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print(f"{model_name} - MSE: {mse:.2f}, R²: {r2:.2f}")

# evaluate_model("Linear Regression", y_test, linear_predictor)
# evaluate_model("Random Forest", y_test, rf_predictor)
# evaluate_model("XGBoost", y_test, xgb_predictor)