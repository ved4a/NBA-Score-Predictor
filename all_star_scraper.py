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

    table = soup.find("table", {"id": "roster"})
    if table:
        rows = table.find_all("tr")
        for row in rows:
            player_cell = row.find("td", {"data-stat": "player"})
            if player_cell:
                player_name = player_cell.text.strip()
                all_stars.append({"Player": player_name, "Year": year})
    else:
        print(f"No roster table found for {year}.")

