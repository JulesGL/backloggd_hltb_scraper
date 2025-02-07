import pandas as pd
from howlongtobeatpy import HowLongToBeat

def fetch_hltb_time(game_title):
    """Fetch HLTB main story time for a given game."""
    results = HowLongToBeat().search(game_title)
    
    if results and results[0]:
        best_match = results[0]  # Best matched result
        return best_match.main_story if best_match.main_story else "N/A"
    
    return "N/A"

def update_csv_with_hltb(csv_file):
    """Update backlog CSV file with HLTB times."""
    df = pd.read_csv(csv_file)
    
    if "Game Title" not in df.columns:
        print("CSV must contain a 'Game Title' column.")
        return
    
    df["HLTB Main Story (Hours)"] = df["Game Title"].apply(fetch_hltb_time)
    
    updated_file = "backloggd_games_hltb.csv"
    df.to_csv(updated_file, index=False)
    print(f"Updated CSV saved as: {updated_file}")

if __name__ == "__main__":
    update_csv_with_hltb("backloggd_games.csv")
