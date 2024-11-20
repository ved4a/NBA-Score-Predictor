import requests
from bs4 import BeautifulSoup
import pandas as pd

# URLs for the two players
player_urls = {
    "D'Angelo Russell": "https://www.basketball-reference.com/players/r/russeda01/gamelog/2019/",
    "Mo Williams": "https://www.basketball-reference.com/players/w/willima01/gamelog/2009/"
}

player_stats = []

# Loop through each player and scrape their data
for player_name, url in player_urls.items():
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {player_name}. URL: {url}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", id="pgl_basic")

    if not table:
        print(f"No stats table found for {player_name}.")
        continue

    rows = table.find("tbody").find_all("tr")

    for row in rows:
        # Skip rows with class "thead" (header rows repeated in the table body)
        if "thead" in row.get("class", []):
            continue

        points = row.find("td", {"data-stat": "pts"})
        field_goal_pct = row.find("td", {"data-stat": "fg_pct"})
        three_pointer_pct = row.find("td", {"data-stat": "fg3_pct"})
        free_throw_pct = row.find("td", {"data-stat": "ft_pct"})
        orb = row.find("td", {"data-stat": "orb"})
        turnovers = row.find("td", {"data-stat": "tov"})

        player_stats.append({
            "Player": player_name,
            "Season": url.split("/")[-2],  # Extract season year from URL
            "Points": points.text.strip() if points else None,
            "Field Goal %": field_goal_pct.text.strip() if field_goal_pct else None,
            "Three Pointer %": three_pointer_pct.text.strip() if three_pointer_pct else None,
            "Free Throw %": free_throw_pct.text.strip() if free_throw_pct else None,
            "ORB": orb.text.strip() if orb else None,
            "Turnovers": turnovers.text.strip() if turnovers else None
        })

# Save data to CSV
df = pd.DataFrame(player_stats)
df.to_csv("specific_player_stats.csv", index=False)

print("Data extraction complete. Saved to 'specific_player_stats.csv'.")
