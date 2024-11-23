import pandas as pd

file1 = "first_stats.csv"
file2 = "second_stats.csv"
file3 = "third_stats.csv"
file4 = "mo_williams_stats.csv"
file5 = "missed_stats.csv"

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df3 = pd.read_csv(file3)
df4 = pd.read_csv(file4)
df5 = pd.read_csv(file5)

combined_df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)

combined_df.to_csv("player_stats.csv", index=False)
print("Combined files successfully.")