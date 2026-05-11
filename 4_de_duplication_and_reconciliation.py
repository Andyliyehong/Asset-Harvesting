# Ensure these files are in the same directory as this script
import pandas as pd
import json
import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Configuration ---
MASTER_FILE = '/Users/Andy.Li/Asset_Strategy/Asset Harvesting/Taxonomy & Inventory.xlsx'
NEW_ASSETS_JSON = '/Users/Andy.Li/Asset_Strategy/Asset Harvesting/3_asset_harvest_output.json'
OUTPUT_FILE = '/Users/Andy.Li/Asset_Strategy/Asset Harvesting/4_Reconciled_Assets_Report.xlsx'
HIST_FILE = '/Users/Andy.Li/Asset_Strategy/Asset Harvesting/4_Reconciled_Assets_Report_History.xlsx'

def clean_text(text):
    """Basic cleaning: strip whitespace and lowercase for matching."""
    if pd.isna(text) or text is None:
        return ""
    return str(text).strip().lower()

def get_fingerprint(row):
    """Extract asset fingerprint: Sector + AI Feature + Primary Use Case."""
    s = clean_text(row.get('Sector', ''))
    f = clean_text(row.get('AI Feature', ''))
    u = clean_text(row.get('Primary Use Case', ''))
    return f"{s}|{f}|{u}"

def get_semantic_content(row):
    """Extract text content for semantic similarity matching."""
    desc = str(row.get('Asset Description', ''))
    val = str(row.get('Evidence of Value', ''))
    return f"{desc} {val}".strip()


def append_to_history(df, history_file):
    """Append records to history workbook with a timestamp column."""
    if df.empty:
        print("No rows to append to history.")
        return

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hist_df = df.copy()
    hist_df.insert(0, 'Insert Timestamp', timestamp)

    if os.path.exists(history_file):
        existing_df = pd.read_excel(history_file)
        # Excel row index is 1-based and includes header at row 1.
        write_row = len(existing_df) + 2

        with pd.ExcelWriter(history_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            hist_df.to_excel(writer, index=False, header=False, startrow=write_row - 1)
    else:
        # Create a new history workbook and write with headers.
        with pd.ExcelWriter(history_file, engine='openpyxl', mode='w') as writer:
            hist_df.to_excel(writer, index=False)

    print(f"Success! Appended {len(hist_df)} row(s) into history file: {history_file}")

def run_reconciliation():
    # 1. Load Data
    if not os.path.exists(MASTER_FILE):
        print(f"Error: Master file '{MASTER_FILE}' not found.")
        return
    
    if not os.path.exists(NEW_ASSETS_JSON):
        print(f"Error: JSON file '{NEW_ASSETS_JSON}' not found.")
        return

    try:
        master_df = pd.read_excel(MASTER_FILE, sheet_name='Asset Inventory')
        
        with open(NEW_ASSETS_JSON, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Access assets from root key and filter for "Source Type" == "Asset"
        raw_list = json_data.get("assets", []) if isinstance(json_data, dict) else json_data
        
        filtered_data = [
            item for item in raw_list 
            if isinstance(item, dict) and item.get("Source Type") == "Asset"
        ]
        
        if not filtered_data:
            print("No items with Source Type 'Asset' found in the JSON file.")
            return
            
        new_assets_df = pd.DataFrame(filtered_data)
        print(f"Processing {len(new_assets_df)} items with Source Type: Asset.")
        
    except Exception as e:
        print(f"Data Loading Error: {e}")
        return

    # 2. Pre-process Master Data
    master_df['clean_name'] = master_df['Asset Name'].apply(clean_text)
    master_df['fingerprint'] = master_df.apply(get_fingerprint, axis=1)
    master_semantic_texts = master_df.apply(get_semantic_content, axis=1).tolist()

    # 3. Initialize TF-IDF for Semantic Analysis
    vectorizer = TfidfVectorizer(stop_words='english')
    valid_master_texts = [t for t in master_semantic_texts if t.strip()]
    
    if valid_master_texts:
        vectorizer.fit(valid_master_texts)
        master_vectors = vectorizer.transform(master_semantic_texts)
    else:
        master_vectors = None

    results = []
    details = []

    # 4. Execute Three-Tier Reconciliation Logic
    for _, new_row in new_assets_df.iterrows():
        res = "Add into"
        det = "No significant overlap found. Ready for insertion."
        
        c_name = clean_text(new_row.get('Asset Name', ''))
        c_finger = get_fingerprint(new_row)
        c_semantic = get_semantic_content(new_row)

        name_matches = master_df[master_df['clean_name'] == c_name]
        finger_matches = master_df[master_df['fingerprint'] == c_finger]

        max_sim = 0
        best_match_name = "N/A"
        if master_vectors is not None and c_semantic.strip():
            new_vec = vectorizer.transform([c_semantic])
            sim_scores = cosine_similarity(new_vec, master_vectors)[0]
            max_sim = sim_scores.max()
            best_match_name = master_df.iloc[sim_scores.argmax()]['Asset Name']

        # Decision Logic
        if not name_matches.empty and not finger_matches.empty and max_sim > 0.85:
            res = "Duplicate should be removed"
            det = f"Replicating with existing asset: '{name_matches.iloc[0]['Asset Name']}'. Match confirmed via Name, Fingerprint, and high similarity ({max_sim:.2%})."
        
        elif name_matches.empty and not finger_matches.empty:
            res = "Potential match need human review"
            det = f"Unique name, but Fingerprint matches exactly with existing asset: '{finger_matches.iloc[0]['Asset Name']}'."
            
        elif max_sim > 0.85:
            res = "Potential match need human review"
            det = f"High semantic similarity ({max_sim:.2%}) with asset: '{best_match_name}'."
            
        elif 0.5 <= max_sim <= 0.85:
            res = "Mid match, keep it for now"
            det = f"Moderate similarity ({max_sim:.2%}) with asset: '{best_match_name}'."
            
        else:
            res = "Add into"
            det = f"Asset appears to be unique. Max similarity score: {max_sim:.2%}."

        results.append(res)
        details.append(det)

    # 5. Save Final Report
    new_assets_df['Reconciliation Results'] = results
    new_assets_df['Reconciliation Details'] = details
    
    new_assets_df.to_excel(OUTPUT_FILE, index=False)
    print(f"Success! Reconciliation report generated: {OUTPUT_FILE}")

    # 6. Append to history workbook with insertion timestamp
    append_to_history(new_assets_df, HIST_FILE)

if __name__ == "__main__":
    run_reconciliation()