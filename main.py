import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

current_season_data = pd.read_csv("current_szn_data.csv")
previous_season_data = pd.read_csv("prev_szn_data.csv")

data = pd.concat([current_season_data, previous_season_data])