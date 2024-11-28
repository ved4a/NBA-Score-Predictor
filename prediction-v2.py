import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

# Load the data (player stats)
data = pd.read_csv('player_stats.csv')
avg_player_stats = pd.read_csv('avg_player_Stats.csv')  # New CSV with player's average stats

# Remove dependent columns from the main dataset
data = data.drop(columns=['3P%', 'FG%', 'FT%', 'TRB', 'Season'])

# Group by players
players = data['Player'].unique()

# This will hold the best model for each player
best_models = []

# Iterate through each player to train models
for idx, player in enumerate(players):
    print(f"Processing player {idx + 1}/{len(players)}: {player}")

    player_data = data[data['Player'] == player]
    X = player_data.drop(columns=['Player', 'Points'])  # Don't want to check 'Player' and 'Points'
    y = player_data['Points']  # Target variable: Points

    # Drop NaN values
    data_cleaned = pd.concat([X, y], axis=1).dropna()

    # Get X and y back
    X = data_cleaned.drop(columns=["Points"]).reset_index(drop=True)
    y = data_cleaned["Points"].reset_index(drop=True)

    # Skip if insufficient data
    if len(X) < 10:
        print(f"Skipping {player}: Insufficient data.")
        continue

    # Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale for regression models
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Define models
    models = {
        'Ridge Regression': Ridge(alpha=1.0),
        'Lasso Regression': Lasso(alpha=0.1),
        'Random Forest': RandomForestRegressor(random_state=42),
        'XGBoost': XGBRegressor(random_state=42)
    }

    best_mse = float('inf')
    best_model_name = None
    best_model = None

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"Model: {name} | MSE: {mse:.4f}")

        # Track the best model with the smallest MSE
        if mse < best_mse:
            best_mse = mse
            best_model_name = name
            best_model = model

    # Store the best model and player details
    best_models.append({
        'Player': player,
        'Best Model': best_model_name,
        'Model': best_model,
        'Scaler': scaler  # Save scaler for consistent scaling
    })

# Convert the results to a DataFrame
best_models_df = pd.DataFrame(best_models)

print("Processing complete. All players have been evaluated :)")
print(best_models_df)

# Function to predict the score of a new player
def predict_score(player_name, player_stats, best_models_df):
    # Find the best model for the player
    player_data = best_models_df[best_models_df['Player'] == player_name]
    if player_data.empty:
        print(f"No model found for {player_name}.")
        return None

    best_model = player_data['Model'].values[0]
    scaler = player_data['Scaler'].values[0]

    # Prepare the player stats for prediction (ensure it matches the feature set with column names)
    player_stats_df = pd.DataFrame([player_stats], columns=X.columns)  # Use the original feature names
    player_stats_scaled = scaler.transform(player_stats_df)  # Scale the stats using the previously fitted scaler

    # Predict the score
    predicted_score = best_model.predict(player_stats_scaled)[0]

    # Round to the nearest integer
    return round(predicted_score)


# Make predictions for each player
team_one_players = ['Stephen Curry', 'Mo Williams', 'Ben Simmons', 'Ja Morant', 'LaMelo Ball']
team_two_players = ['Klay Thompson', 'LeBron James', "Shaquille O'Neal", 'Zion Williamson', 'Yao Ming']

team_one_score = 0
for player in team_one_players:
    player_data = avg_player_stats[avg_player_stats['Player'] == player]
    if player_data.empty:
        print(f"Stats not found for player: {player}")
        continue

    # Align columns with training features
    player_stats = player_data.drop(columns=['Player'])[X.columns].iloc[0].values.tolist()

    predicted_score = predict_score(player, player_stats, best_models_df)
    if predicted_score is not None:
        print(f"Predicted score for {player}: {predicted_score}")
        team_one_score += predicted_score

team_two_score = 0
for player in team_two_players:
    player_data = avg_player_stats[avg_player_stats['Player'] == player]
    if player_data.empty:
        print(f"Stats not found for player: {player}")
        continue

    # Align columns with training features
    player_stats = player_data.drop(columns=['Player'])[X.columns].iloc[0].values.tolist()

    predicted_score = predict_score(player, player_stats, best_models_df)
    if predicted_score is not None:
        print(f"Predicted score for {player}: {predicted_score}")
        team_two_score += predicted_score

print(f"Team One Score: {team_one_score}")
print(f"Team Two Score: {team_two_score}")
