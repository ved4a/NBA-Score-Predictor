import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

current_season_data = pd.read_csv("current_szn_data.csv")
previous_season_data = pd.read_csv("prev_szn_data.csv")

data = pd.concat([current_season_data, previous_season_data])

X = data.drop(columns=["Points"])
y = data["Points"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)