import requests
from bs4 import BeautifulSoup
import pandas as pd

players = pd.read_csv("all_stars_cleaned.csv")

BASE_URL = "https://www.basketball-reference.com/players/{}/{}/gamelog/{}"

player_stats = []

for _, row in players.iterrows():
    player_name = row['Player']
    appearances = row['Appearances']
    last_allstar_year = row['YearLastPlayed']

    first_name, last_name = player_name.split(" ", 1)
    slug = f"{last_name[:5].lower()}{first_name[:2].lower()}01"
    initial = last_name[0].lower()

    url = BASE_URL.format(initial, slug, last_allstar_year)

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve data for {player_name}: {url}")
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
            "Points": points,
            "Field Goal %": field_goal_pct,
            "Three Pointer %": three_pointer_pct,
            "Free Throw %": free_throw_pct,
            "ORB": orb,
            "Turnovers": turnovers
        })