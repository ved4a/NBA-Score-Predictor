import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import random
from concurrent.futures import ThreadPoolExecutor

players = pd.read_csv("second.csv")

BASE_URL = "https://www.basketball-reference.com/players/{}/{}/gamelog/{}"

def fetch_player_stats(row):
    player_name = row['Player']
    last_allstar_year = row['YearLastPlayed']

    first_name, last_name = player_name.split(" ", 1)

    # remove apostrophes, special characters
    first_name = re.sub(r"[^a-zA-Z]", "", first_name)
    last_name = re.sub(r"[^a-zA-Z]", "", last_name)

    player_data = []

    for i in range(1, 3): # try only 2 slugs
        slug = f"{last_name[:5].lower()}{first_name[:2].lower()}{str(i).zfill(2)}"
        initial = last_name[0].lower()
        url = BASE_URL.format(initial, slug, last_allstar_year)

        try:
            response = requests.get(url)
            time.sleep(random.uniform(1, 3))
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", id="pgl_basic")
            if table:
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
                    orb = row.find("td", {"data-stat": "orb"})  # Offensive rebounds
                    drb = row.find("td", {"data-stat": "drb"})  # Defensive rebounds
                    trb = row.find("td", {"data-stat": "trb"})  # Total rebounds
                    assists = row.find("td", {"data-stat": "ast"})
                    blocks = row.find("td", {"data-stat": "blk"})
                    steals = row.find("td", {"data-stat": "stl"})
                    turnovers = row.find("td", {"data-stat": "tov"})
                    personal_fouls = row.find("td", {"data-stat": "pf"})

                    player_data.append({
                        "Player": player_name,
                        "Season": last_allstar_year,
                        "Points": points.text.strip() if points else None,
                        "Field Goals": field_goals.text.strip() if field_goals else None,
                        "FG Attempts": field_goal_attempts.text.strip() if field_goal_attempts else None,
                        "FG%": field_goal_pct.text.strip() if field_goal_pct else None,
                        "Three Pointers": three_pointers.text.strip() if three_pointers else None,
                        "3P Attempts": three_pointer_attempts.text.strip() if three_pointer_attempts else None,
                        "3P%": three_pointer_pct.text.strip() if three_pointer_pct else None,
                        "Free Throws": free_throws.text.strip() if free_throws else None,
                        "FT Attempts": free_throw_attempts.text.strip() if free_throw_attempts else None,
                        "FT%": free_throw_pct.text.strip() if free_throw_pct else None,
                        "ORB": orb.text.strip() if orb else None,
                        "DRB": drb.text.strip() if drb else None,
                        "TRB": trb.text.strip() if trb else None,
                        "Assists": assists.text.strip() if assists else None,
                        "Blocks": blocks.text.strip() if blocks else None,
                        "Steals": steals.text.strip() if steals else None,
                        "Turnovers": turnovers.text.strip() if turnovers else None,
                        "Personal Fouls": personal_fouls.text.strip() if personal_fouls else None
                    })
                break
        except Exception as e:
            print(f"Error fetching data for {player_name}: {e}")
            continue

    if not player_data:
        print(f"Failed to retrieve data for {player_name}. Please recheck the slugs.")
    return player_data

# enable parallel requests
with ThreadPoolExecutor(max_workers=5) as executor:
    all_stats = list(executor.map(fetch_player_stats, players.to_dict(orient='records')))

# flatten list
player_stats = [item for sublist in all_stats for item in sublist]

df = pd.DataFrame(player_stats)
df.to_csv("second_stats.csv", index=False)