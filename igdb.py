import requests
import pandas as pd

# 🔑 Set up your IGDB credentials
CLIENT_ID = "wky210z34gscdrknl5u11xf2pbxn67"
CLIENT_SECRET = "pq6d8vm5k7yg1sgedmg5xqwi6yjr7r"

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

# 🔍 Search for a game on IGDB and fetch keywords
def fetch_igdb_keywords(game_title, token):
    url = "https://api.igdb.com/v4/games"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {token}",
    }
    data = f'search "{game_title}"; fields name, genres.name, themes.name, keywords.name; limit 1;'
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200 and response.json():
        game_data = response.json()[0]
        genres = [g["name"] for g in game_data.get("genres", [])]
        themes = [t["name"] for t in game_data.get("themes", [])]
        keywords = [k["name"] for k in game_data.get("keywords", [])]
        return ", ".join(genres + themes + keywords) if (genres or themes or keywords) else "N/A"
    
    return "N/A"

# 📝 Update CSV with IGDB Keywords
def update_csv_with_igdb(csv_file):
    token = get_igdb_token()
    
    df = pd.read_csv(csv_file)
    
    if "Game Title" not in df.columns:
        print("CSV must contain a 'Game Title' column.")
        return
    
    df["IGDB Keywords"] = df["Game Title"].apply(lambda title: fetch_igdb_keywords(title, token))
    
    updated_file = "backloggd_games.csv"
    df.to_csv(updated_file, index=False)
    print(f"Updated CSV saved as: {updated_file}")

if __name__ == "__main__":
    update_csv_with_igdb("backloggd_games.csv")
