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
        print(f"Error Fetching Stats for Player ID: {player_id}: {e}.")
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

# this function can be updated to X years
def filter_players(player_list, start_season, end_season):
    active_players = []

    for player in player_list:
        seasons = get_player_seasons(player["id"])
        if any(start_season <= season <= end_season for season in seasons):
            active_players.append(player)

    return active_players

def is_all_star(award_data, start_season, end_season):
    if not award_data or "PlayerAwards" not in award_data:
        return False

    awards = award_data["PlayerAwards"]
    all_star_awards = [
        award for award in awards
        if "All-Star" in award["DESCRIPTION"] and start_season <= award["SEASON"] <= end_season
    ]
    return len(all_star_awards) > 0

def fetch_all_stars(player_ids, start_season, end_season, max_workers=5):
    all_star_players = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(fetch_player_awards, player_ids))

    for player, award_data in zip(active_players, results):
        if is_all_star(award_data, start_season, end_season):
            all_star_players.append({
                "id": player["id"],
                "full_name": player["full_name"],
                "awards": award_data
            })

    return all_star_players

if __name__ == "__main__":
    # Get all players
    all_players = players.get_players()

    print("Filtering players active between 2020-2023...")
    active_players = filter_players(all_players)

    # Get player IDs for active players
    player_ids = [player["id"] for player in active_players]

    print(f"Found {len(active_players)} Players Active Between 2020-2023.")
    print("Fetching All-Star Players...")
    start_time = time.time()
    all_star_players = fetch_all_stars(player_ids, max_workers=10)
    end_time = time.time()

    print(f"\nFound {len(all_star_players)} All-Star players in {end_time - start_time:.2f} seconds.")
    
    # Output the results
    for player in all_star_players:
        print(f"Player: {player['full_name']} | Awards: {player['awards']}")