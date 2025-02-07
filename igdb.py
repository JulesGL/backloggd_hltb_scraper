import requests
import pandas as pd

# 🔑 Set up your IGDB credentials
CLIENT_ID = ""
CLIENT_SECRET = ""
MAX_KEYWORDS = 5

# 🎮 Get OAuth Token from Twitch
def get_igdb_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    response = requests.post(url, params)
    return response.json().get("access_token")

# 🕹 Fetch platforms & keywords from IGDB
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
        
        # Extract platforms
        platforms = [p["name"] for p in game_data.get("platforms", [])]
        platform_str = ", ".join(platforms) if platforms else "N/A"

        # Extract keywords (limit to MAX_KEYWORDS)
        keywords = [k["name"] for k in game_data.get("keywords", [])][:MAX_KEYWORDS]
        keyword_str = ", ".join(keywords) if keywords else "N/A"

        return platform_str, keyword_str
    
    return "N/A", "N/A"

# 📝 Update CSV with IGDB Platforms & Keywords
def update_csv_with_igdb_data(csv_file):
    token = get_igdb_token()
    
    df = pd.read_csv(csv_file)
    
    if "Game Title" not in df.columns:
        print("CSV must contain a 'Game Title' column.")
        return
    
    df[["IGDB Platforms", "IGDB Keywords"]] = df["Game Title"].apply(lambda title: pd.Series(fetch_igdb_data(title, token)))
    
    updated_file = "backloggd_games_igdb_data.csv"
    df.to_csv(updated_file, index=False)
    print(f"Updated CSV saved as: {updated_file}")

if __name__ == "__main__":
    update_csv_with_igdb_data("backloggd_games.csv")