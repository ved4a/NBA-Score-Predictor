import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

players = pd.read_csv("all_stars_cleaned.csv")

BASE_URL = "https://www.basketball-reference.com/players/{}/{}/gamelog/{}"

player_stats = []

for _, row in players.iterrows():
    player_name = row['Player']
    appearances = row['Appearances']
    last_allstar_year = row['YearLastPlayed']

    first_name, last_name = player_name.split(" ", 1)
    last_name = re.sub(r"[^a-zA-Z]", "", last_name)  # remove apostrophes / special characters
    found = False

    # try more than 1 slug variation
    for i in range(1, 4):
        slug = f"{last_name[:5].lower()}{first_name[:2].lower()}{str(i).zfill(2)}"
        initial = last_name[0].lower()
        url = BASE_URL.format(initial, slug, last_allstar_year)

        response = requests.get(url)
        if response.status_code == 200:
            found = True
            break

    if not found:
        print(f"Failed to retrieve data for {player_name}.")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", id="pgl_basic")

    if not table:
        print(f"No stats table found for {player_name}. Skipping.")
        continue

    rows = table.find("tbody").find_all("tr")

    for row in rows:
        points = row.find("td", {"data-stat": "pts"})
        field_goal_pct = row.find("td", {"data-stat": "fg_pct"})
        three_pointer_pct = row.find("td", {"data-stat": "fg3_pct"})
        free_throw_pct = row.find("td", {"data-stat": "ft_pct"})
        orb = row.find("td", {"data-stat": "orb"})
        turnovers = row.find("td", {"data-stat": "tov"})

        player_stats.append({
            "Player": player_name,
            "Season": last_allstar_year,
            "Points": points.text.strip() if points else None,
            "Field Goal %": field_goal_pct.text.strip() if field_goal_pct else None,
            "Three Pointer %": three_pointer_pct.text.strip() if three_pointer_pct else None,
            "Free Throw %": free_throw_pct.text.strip() if free_throw_pct else None,
            "ORB": orb.text.strip() if orb else None,
            "Turnovers": turnovers.text.strip() if turnovers else None
        })

# Save data to CSV
df = pd.DataFrame(player_stats)
df.to_csv("player_stats.csv", index=False)