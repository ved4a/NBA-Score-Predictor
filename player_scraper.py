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
