import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.basketball-reference.com/allstar/NBA_{}.html"

START_YEAR = 2000
END_YEAR = 2023

all_stars = []

for year in range(START_YEAR, END_YEAR + 1):
    print(f"Scraping year: {year}.") # progress 'bar'
    url = BASE_URL.format(year)
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve data for {year}. Status code: {response.status_code}.")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table", class_="sortable stats_table")
    print(f"Found {len(tables)} tables for year {year}.")

    for table in tables:
        caption = table.find("caption")
        team_name = caption.text.strip() if caption else None
        team_name = team_name.replace(" Table", "")
        print(f"Processing team: {team_name}")

        if not team_name:
            print(f"No team name found for table in year {year}. Skipping.")
            continue

        rows = table.find("tbody").find_all("tr")
        print(f"Found {len(rows)} players in table for team: {team_name}")

        for row in rows:
            player_cell = row.find("th", {"data-stat": "player"})
            if player_cell:
                player_name = player_cell.text.strip()
                all_stars.append({
                    "Player": player_name,
                    "Year": year,
                    "Team": team_name
                })
            else:
                continue

df = pd.DataFrame(all_stars)
df.to_csv("all_stars_2000_to_2023.csv", index=False)