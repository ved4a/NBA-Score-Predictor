import pandas as pd

input_file = "all_stars_2000_to_2023.csv"
output_file = "all_stars_cleaned.csv"

data = pd.read_csv(input_file)

player_column = 'Player'

player_counts = data[player_column].value_counts().reset_index()
player_counts.columns = ['Player', 'Appearances']

player_counts.to_csv(output_file, index=False)

print(f"Unique All-Star players and their appearances saved to '{output_file}'")