import pandas as pd
import os

# --- Configuration ---
SOURCE_REPORT = '/Users/Andy.Li/Asset_Strategy/Asset Harvesting/4_Reconciled_Assets_Report.xlsx'
MASTER_FILE = '/Users/Andy.Li/Asset_Strategy/Asset Harvesting/Taxonomy & Inventory.xlsx'
SHEET_NAME = 'Asset Inventory'

def update_asset_inventory():
    # 1. Verify file existence
    if not os.path.exists(SOURCE_REPORT):
        print(f"Error: Source report '{SOURCE_REPORT}' not found.")
        return
    if not os.path.exists(MASTER_FILE):
        print(f"Error: Master file '{MASTER_FILE}' not found.")
        return

    try:
        # 2. Load the reconciliation report
        report_df = pd.read_excel(SOURCE_REPORT)
        
        # 3. Filter for items matching your criteria
        # Logic: "Add into" OR "Mid match, keep it for now"
        valid_statuses = ["Add into", "Mid match, keep it for now"]
        to_add_df = report_df[report_df['Reconciliation Results'].isin(valid_statuses)].copy()
        
        if to_add_df.empty:
            print("No items qualify for addition based on the reconciliation status.")
            return

        # 4. Load the existing Master File content
        # We read the master first to ensure we append to the end of existing data
        master_df = pd.read_excel(MASTER_FILE, sheet_name=SHEET_NAME)

        # 5. Data Preparation
        # Remove the reconciliation-specific helper columns before adding to master
        cols_to_remove = ['Reconciliation Results', 'Reconciliation Details', 'clean_name', 'fingerprint']
        clean_to_add = to_add_df.drop(columns=[c for c in cols_to_remove if c in to_add_df.columns])

        # 6. Append and Save
        # Using 'openpyxl' engine with 'overlay' mode to update only the specific sheet
        with pd.ExcelWriter(MASTER_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            updated_master = pd.concat([master_df, clean_to_add], ignore_index=True)
            updated_master.to_excel(writer, sheet_name=SHEET_NAME, index=False)
            
        print(f"Update Successful!")
        print(f"Total items appended: {len(clean_to_add)}")
        print(f"File updated: {MASTER_FILE} -> Sheet: {SHEET_NAME}")

    except Exception as e:
        print(f"An error occurred during the update: {e}")

if __name__ == "__main__":
    update_asset_inventory()