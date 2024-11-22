import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time, random

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
    for i in range(1, 4):
        slug = f"{last_name[:5].lower()}{first_name[:2].lower()}{str(i).zfill(2)}"
        initial = last_name[0].lower()
        url = BASE_URL.format(initial, slug, last_allstar_year)

        response = requests.get(url)
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", id="pgl_basic")

        if table:
            found = True
            rows = table.find("tbody").find_all("tr")

            for row in rows:
                points = row.find("td", {"data-stat": "pts"})
                field_goals = row.find("td", {"data-stat": "fg"})
                field_goal_attempts = row.find("td", {"data-stat": "fga"})
                field_goal_pct = row.find("td", {"data-stat": "fg_pct"})
                three_pointers = row.find("td", {"data-stat": "fg3"})
                three_pointer_attempts = row.find("td", {"data-stat": "fg3a"})
                three_pointer_pct = row.find("td", {"data-stat": "fg3_pct"})
                free_throws = row.find("td", {"data-stat": "ft"})
                free_throw_attempts = row.find("td", {"data-stat": "fta"})
                free_throw_pct = row.find("td", {"data-stat": "ft_pct"})
                orb = row.find("td", {"data-stat": "orb"}) # offensive rebounds
                drb = row.find("td", {"data-stat": "drb"}) # defensive rebounds
                trb = row.find("td", {"data-stat": "trb"}) # total rebounds
                assists = row.find("td", {"data-stat": "ast"})
                blocks = row.find("td", {"data-stat": "blk"})
                steals = row.find("td", {"data-stat": "stl"})
                turnovers = row.find("td", {"data-stat": "tov"})
                personal_fouls = row.find("td", {"data-stat": "pf"})

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
            break

        time.sleep(random.uniform(1, 3))

    if not found:
        print(f"Failed to retrieve data for {player_name}. Please recheck the slugs.")


df = pd.DataFrame(player_stats)
df.to_csv("player_stats.csv", index=False)