import pandas as pd
from howlongtobeatpy import HowLongToBeat

def fetch_hltb_data(game_title, attributes):
    """Fetch selected HLTB attributes for a given game."""
    results = HowLongToBeat().search(game_title)
    
    if results and results[0]:
        best_match = results[0]  # Best matched result
        return {attr: getattr(best_match, attr, "N/A") for attr in attributes}
    
    return {attr: "N/A" for attr in attributes}

def update_csv_with_hltb(csv_file, attributes=None):
    """Update backlog CSV file with selected HLTB data."""
    if attributes is None:
        attributes = ["main_story", "main_extra", "completionist", "all_styles"]
    
    df = pd.read_csv(csv_file)
    
    if "Game Title" not in df.columns:
        print("CSV must contain a 'Game Title' column.")
        return
    
    hltb_data = df["Game Title"].apply(lambda title: fetch_hltb_data(title, attributes))
    
    for attr in attributes:
        df[f"HLTB {attr.replace('_', ' ').title()}"] = hltb_data.apply(lambda x: x[attr])
    
    updated_file = "backloggd_games.csv"
    df.to_csv(updated_file, index=False)
    print(f"Updated CSV saved as: {updated_file}")

if __name__ == "__main__":
    selected_attributes = ["review_score","main_story", "main_extra", "completionist"]  # Modify as needed
    update_csv_with_hltb("backloggd_games.csv", selected_attributes)