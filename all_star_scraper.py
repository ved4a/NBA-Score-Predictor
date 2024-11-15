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
    
