import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL for Mo Williams
url = "https://www.basketball-reference.com/players/w/willima01/gamelog/2009/"

def fetch_mo_williams_stats(url):
    # hardcoded since script wasn't able to find it
    player_name = "Mo Williams"
    last_allstar_year = "2009"
    player_data = []

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve data for {player_name}. URL: {url}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", id="pgl_basic")

        if not table:
            print(f"No stats table found for {player_name}.")
            return []

        rows = table.find("tbody").find_all("tr")

        for row in rows:
            if "thead" in row.get("class", []):
                continue

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
    except Exception as e:
        print(f"Error fetching data for {player_name}: {e}")

    return player_data

mo_williams_stats = fetch_mo_williams_stats(url)

df = pd.DataFrame(mo_williams_stats)
df.to_csv("mo_williams_stats.csv", index=False)

print("Data extraction complete. Saved to 'mo_williams_stats.csv'.")
