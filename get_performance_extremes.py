import pandas as pd

df = pd.read_csv("player_stats.csv")

stats_columns = [
    "Points", "Field Goals", "FG Attempts", "FG%", "Three Pointers", 
    "3P Attempts", "3P%", "Free Throws", "FT Attempts", "FT%", 
    "ORB", "DRB", "TRB", "Assists", "Blocks", "Steals", 
    "Turnovers", "Personal Fouls"
]

# calc high, low, avg of each stat
def calculate_high_low_average(group):
    result = {}
    for stat in stats_columns:
        result[f"Highest {stat}"] = group[stat].max()
        result[f"Lowest {stat}"] = group[stat].min()
        result[f"Average {stat}"] = group[stat].mean()
    return pd.Series(result)

# group by player, apply calculation
high_low_stats = df.groupby("Player").apply(calculate_high_low_average).reset_index()

high_low_stats.to_csv("player_stats_HLA.csv", index=False)
print("Highest, lowest, and average stats calculated and saved to CSV.")
