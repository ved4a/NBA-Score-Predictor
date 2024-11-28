import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

# load the data
data = pd.read_csv('player_stats.csv')

# remove dependent columns
data = data.drop(columns=['3P%', 'FG%', 'FT%', 'TRB', 'Season'])

# group by players
players = data['Player'].unique()

results = {}

# iterate through each player
for player in players:
    player_data = data[data['Player'] == player]
    X = player_data.drop(columns=['Player', 'Points'])
    y = player_data['Points']

    data_cleaned = pd.concat([X, y], axis=1).dropna()

    X = data_cleaned.drop(columns=["Points"]).reset_index(drop=True)
    y = data_cleaned["Points"].reset_index(drop=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(random_state=42),
        'XGBoost': XGBRegressor(random_state=42)
    }

    player_results = {}

    for name, model in models.items():
        # training
        model.fit(X_train, y_train)

        # predicting on test data
        y_pred = model.predict(X_test)

        # root mean squared error
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        player_results[name] = {'model': model, 'rmse': rmse}

    # identify the best model for each lpayer
    best_model_name = min(player_results, key=lambda x: player_results[x]['rmse'])
    results[player] = {
        'best_model': best_model_name,
        'model': player_results[best_model_name]['model'],
        'rmse': player_results[best_model_name]['rmse']
    }