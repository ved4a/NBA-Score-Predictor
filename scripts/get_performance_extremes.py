import pandas as pd
import math

df = pd.read_csv("player_stats.csv")

stats_columns = [
    "Points", "Field Goals", "FG Attempts", "Three Pointers", 
    "3P Attempts", "Free Throws", "FT Attempts",
    "ORB", "DRB", "Assists", "Blocks", "Steals", 
    "Turnovers", "Personal Fouls"
]

results = []

for player in df['Player'].unique():
    player_data = df[df['Player'] == player]
    result = {"Player": player}
    
    for stat in stats_columns:
        # skip NaN and apply floor function to get avg points
        stat_mean = player_data[stat].mean(skipna=True)
        result[f"Average {stat}"] = math.floor(stat_mean) if not pd.isna(stat_mean) else 0
    
    results.append(result)

high_low_avg_stats = pd.DataFrame(results)

high_low_avg_stats.to_csv("avg_player_stats.csv", index=False)
print("Average stats calculated and saved to 'avg_player_stats.csv'")