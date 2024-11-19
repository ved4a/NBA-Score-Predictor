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
        print(f"Failed to get data for {year}.")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table", class_="sortable stats_table")
    for table in tables:
        team_id = table.get("id")
        if team_id:
            rows = table.find("tbody").find_all("tr")
            for row in rows:
                player_cell = row.find("td", {"data-stat": "player"})
                if player_cell:
                    player_name = player_cell.text.strip()
                    all_stars.append({"Player": player_name, "Year": year, "Team": team_id})

df = pd.DataFrame(all_stars)
df.to_csv("all_stars_2000_to_2024.csv", index=False)