import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
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
for idx, player in enumerate(players):
    print(f"Processing player {idx + 1}/{len(players)}: {player}")

    player_data = data[data['Player'] == player]
    X = player_data.drop(columns=['Player', 'Points'])
    y = player_data['Points']

    # drop NaN values
    data_cleaned = pd.concat([X, y], axis=1).dropna()

    X = data_cleaned.drop(columns=["Points"]).reset_index(drop=True)
    y = data_cleaned["Points"].reset_index(drop=True)

    # in case of lack of data
    if len(X) < 10:
        print(f"Skipping {player}: Insufficient data.")
        continue

    # check variance in data
    # print(f"Variance in target for {player}: {y.var()}")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.fit_transform(X_test)

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

        # compare predictions with actual values
        # print(f"y_test for {player}: {y_test.values}")
        # print(f"Predictions for {player} using {name}: {y_pred}")

        # root mean squared error
        mse = mean_squared_error(y_test, y_pred)
        r2 = model.score(X_test, y_test) # R^2
        player_results[name] = {'model': model, 'mse': mse, 'r2': r2}

        print(f"Model: {name} | MSE: {mse:.4f} | R^2: {r2:.4f}")

    # identify the best model for each lpayer
    best_model_name = min(player_results, key=lambda x: player_results[x]['mse'])
    results[player] = {
        'best_model': best_model_name,
        'model': player_results[best_model_name]['model'],
        'mse': player_results[best_model_name]['mse'],
        'r2': player_results[best_model_name]['r2']
    }
    print(f"Best model for {player}: {best_model_name} (MSE: {results[player]['mse']:.4f})")

print("Processing complete. All players have been evaluated :)")