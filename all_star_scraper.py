from nba_api.stats.endpoints import playerawards, playercareerstats
from nba_api.stats.static import players
from concurrent.futures import ThreadPoolExecutor
import time

def get_player_seasons(player_id):
    try:
        # will get stats in a normalized dictionary
        stats = playercareerstats.PlayerCareerStats(player_id=player_id).get_normalized_dict()
        seasons = [row['SEASON_ID'] for row in stats.get('SeasonTotalsRegularSeason', [])]
        return seasons
    except Exception as e:
        print(f"Error fetching stats for player ID: {player_id}: {e}.")
        return []
    
def fetch_player_awards(player_id, retries=3, delay=5):
    for attempt in range(retries):
        try:
            print(f"Fetching Awards for Player ID {player_id} (Attempt {attempt + 1})...")
            awards = playerawards.PlayerAwards(player_id=player_id, timeout=60)
            return awards.get_normalized_dict()
        except Exception as e:
            print(f"Error fetching awards for Player ID {player_id} (Attempt {attempt + 1}): {e}")
            time.sleep(delay)
    return {"error": f"Failed to fetch awards for Player ID {player_id} after {retries} retries."}
