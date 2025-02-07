import requests
import pandas as pd
from howlongtobeatpy import HowLongToBeat

# 🔑 API Credentials
STEAM_API_KEY = "your_steam_api_key"
STEAM_ID = "your_steam_id"
CLIENT_ID = "your_igdb_client_id"
CLIENT_SECRET = "your_igdb_client_secret"
MAX_KEYWORDS = 5  # Limit number of keywords

# 🎮 Get Steam Playtime Data
def fetch_steam_playtime():
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": STEAM_ID,
        "format": "json",
        "include_appinfo": True
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        games = response.json().get("response", {}).get("games", [])
        return {game["name"]: round(game["playtime_forever"] / 60, 2) for game in games}  # Convert minutes to hours
    
    return {}

# 🎮 Get OAuth Token from Twitch (IGDB API)
def get_igdb_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    response = requests.post(url, params)
    return response.json().get("access_token")

# 🕹 Fetch Platforms & Keywords from IGDB
def fetch_igdb_data(game_title, token):
    url = "https://api.igdb.com/v4/games"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {token}",
    }
    data = f'search "{game_title}"; fields name, platforms.name, keywords.name; limit 1;'
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200 and response.json():
        game_data = response.json()[0]
        
        platforms = [p["name"] for p in game_data.get("platforms", [])]
        platform_str = ", ".join(platforms) if platforms else "N/A"

        keywords = [k["name"] for k in game_data.get("keywords", [])][:MAX_KEYWORDS]
        keyword_str = ", ".join(keywords) if keywords else "N/A"

        return platform_str, keyword_str
    
    return "N/A", "N/A"

# ⏳ Fetch HLTB Main Story Time
def fetch_hltb_time(game_title):
    results = HowLongToBeat().search(game_title)
    
    if results and results[0]:
        best_match = results[0]
        return best_match.main_story if best_match.main_story else "N/A"
    
    return "N/A"

# 📝 Create Training Dataset
def create_training_dataset():
    # Get data
    steam_playtime = fetch_steam_playtime()
    token = get_igdb_token()
    
    games_data = []
    
    for game_title, playtime in steam_playtime.items():
        print(f"Processing: {game_title}...")

        platforms, keywords = fetch_igdb_data(game_title, token)
        hltb_time = fetch_hltb_time(game_title)

        games_data.append({
            "Game Title": game_title,
            "Platforms": platforms,
            "Keywords": keywords,
            "HLTB Main Story (Hours)": hltb_time,
            "Your Playtime (Hours)": playtime
        })
    
    # Convert to DataFrame
    df = pd.DataFrame(games_data)
    
    # Save to CSV
    df.to_csv("steam_training_dataset.csv", index=False)
    print("✅ Training dataset saved as 'steam_training_dataset.csv'")

if __name__ == "__main__":
    create_training_dataset()
