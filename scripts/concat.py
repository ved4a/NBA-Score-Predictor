import pandas as pd

file1 = "current_szn_data.csv"
file2 = "prev_szn_data.csv"

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

combined_df = pd.concat([df1, df2], ignore_index=True)

combined_df.to_csv("player_stats.csv", index=False)
print("Combined files successfully.")