import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_backlog(username,max_page):
    page = 1
    games = []
    
    while page<=max_page:
        url = f"https://www.backloggd.com/u/{username}/backlog?page={page}"
        response = requests.get(url)
        
        if response.status_code != 200:
            print("Failed to fetch backlog. Check username or site structure.")
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        game_entries = soup.find_all("div", class_="card mx-auto game-cover")
        
        if not game_entries:
            break  
        
        for game_entry in game_entries:
            title_tag = game_entry.find("div", class_="game-text-centered")
            if title_tag:
                games.append(title_tag.text.strip())
        
        page += 1 

    return games

def save_to_csv(game_list, file_name="backloggd_games.csv"):
    df = pd.DataFrame({"Game Title": game_list})
    df.to_csv(file_name, index=False)
    print(f"Saved {len(game_list)} games to {file_name}")

if __name__ == "__main__":
    USERNAME = ""  
    games = fetch_backlog(USERNAME,max_page=9)
    if games:
        save_to_csv(games)
