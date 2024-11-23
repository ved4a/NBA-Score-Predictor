import pandas as pd
import math

df = pd.read_csv("player_stats.csv")

stats_columns = [
    "Points", "Field Goals", "FG Attempts", "FG%", "Three Pointers", 
    "3P Attempts", "3P%", "Free Throws", "FT Attempts", "FT%", 
    "ORB", "DRB", "TRB", "Assists", "Blocks", "Steals", 
    "Turnovers", "Personal Fouls"
]

results = []

for player in df['Player'].unique():
    player_data = df[df['Player'] == player]
    result = {"Player": player}
    
    for stat in stats_columns:
        result[f"Highest {stat}"] = player_data[stat].max()
        result[f"Lowest {stat}"] = player_data[stat].min()

        # skip NaN and apply floor function to get avg points
        stat_mean = player_data[stat].mean(skipna=True)
        result[f"{stat} Avg"] = math.floor(stat_mean) if not pd.isna(stat_mean) else 0
    
    results.append(result)

high_low_avg_stats = pd.DataFrame(results)

high_low_avg_stats.to_csv("player_HLA_stats.csv", index=False)
print("High, low, and average stats calculated and saved to 'player_HLA_stats.csv'")