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
data = data.drop(columns=['3P%', 'FG%', 'FT%', 'TRB'])

# group by players
players = data['Player'].unique()

results = {}