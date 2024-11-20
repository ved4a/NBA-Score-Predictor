import pandas as pd

input_file = "all_stars_2000_to_2023.csv"
output_file = "all_stars_cleaned.csv"

data = pd.read_csv(input_file)

player_column = 'Player'
year_column = 'Year'

data = data[data[player_column].str.lower() != "reserves"] # remove 'reserves' as player

player_stats = (
    data.groupby(player_column)[year_column]
    .agg(Appearances='count', YearLastPlayed='max')
    .reset_index()
)

player_stats.to_csv(output_file, index=False)

print(f"Unique All-Star players and their appearances saved to '{output_file}'")