import pandas as pd
import json
import requests
import os

# --- Configuration ---
# 1. Get your API Key at https://serpapi.com/ (Free tier available)
SERPAPI_KEY = "e1efcae656fd0bfecdd356dc6bd511f0a4448bc892c35c7bdd3a02cf5500b679"
INPUT_FILE = '/Users/Andy.Li/Asset_Strategy/Asset Harvesting/Taxonomy & Inventory.xlsx'
OUTPUT_FILE = '/Users/Andy.Li/Asset_Strategy/Asset Harvesting/6_External_Market_Analysis.json'

def perform_web_search(asset_name, use_case, sector):
    """
    Step 1: Execute a real-time Google search for competitors and COTS.
    """
    print(f"--- RESEARCHING: {asset_name} ---")
    
    # Building a professional research query
    # Example: "Top competitors and COTS software for production planning in Agnostic industry"
    query = f"top competitors and COTS software for {use_case} in {sector} industry"
    
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": 5  # Capture top 5 organic results
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        
        # Extract title, link, and snippet to provide 'Grounding' for the AI
        search_results = []
        if "organic_results" in data:
            for res in data["organic_results"]:
                search_results.append({
                    "competitor_source": res.get("title"),
                    "link": res.get("link"),
                    "description": res.get("snippet")
                })
        return search_results
    except Exception as e:
        print(f"Search API Error: {e}")
        return []

def create_strategic_prompt(row, search_data):
    """
    Step 2: Construct the 'Deep-Dive' prompt using real-world evidence.
    """
    # Converting search findings into a readable context for the LLM
    market_evidence = "\n".join([f"- {s['competitor_source']}: {s['description']}" for s in search_data])
    
    prompt = f"""
### ROLE: STRATEGIC MARKET INTELLIGENCE ANALYST

### INTERNAL ASSET UNDER REVIEW:
- Asset Name: {row['Asset Name']}
- Internal Use Case: {row['Primary Use Case']}
- Sector Focus: {row['Sector']}

### EXTERNAL MARKET DATA (RETRIEVED VIA GOOGLE SEARCH):
{market_evidence if market_evidence else "No specific web results found. Use general market knowledge."}

### ASSIGNMENT:
Perform a 1.3 Deep-Dive Competitiveness Analysis. You must:
1. Identify the top 3 direct COTS (Commercial Off-The-Shelf) competitors.
2. Conduct a 'Functional Gap Analysis': Compare our asset's features vs these market leaders.
3. Determine 'Market Standing': Are we a Challenger, Niche Player, or Leader?
4. Generate an 'Improvement Roadmap': List 3 technical suggestions to beat the competition.

### JSON OUTPUT FORMAT:
{{
    "asset_name": "{row['Asset Name']}",
    "found_competitors": ["Comp 1", "Comp 2", "Comp 3"],
    "gap_analysis": {{
        "our_pros": [],
        "our_cons": [],
        "functional_missing_features": []
    }},
    "strategic_recommendation": "",
    "improvement_roadmap": ["Action 1", "Action 2", "Action 3"]
}}
"""
    return prompt

def main():
    # Load the asset inventory from Excel
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    # Using the CSV version if Excel is not directly accessible in this environment
    # In your local env, use: df = pd.read_excel(INPUT_FILE, sheet_name='Asset Inventory')
    # df = pd.read_csv('/Users/Andy.Li/Asset_Strategy/Asset Harvesting/Taxonomy & Inventory.xlsx - Asset Inventory.csv')
    df = pd.read_excel('/Users/Andy.Li/Asset_Strategy/Asset Harvesting/Taxonomy & Inventory.xlsx', sheet_name='Asset Inventory')
    
    # Targeting the two experiment assets
    targets = ["PFEP/IVO Core Platform", "Customer Service Chatbot"]
    target_df = df[df['Asset Name'].isin(targets)].copy()
    
    final_output = []

    for _, row in target_df.iterrows():
        # Execute Real Search
        web_info = perform_web_search(row['Asset Name'], row['Primary Use Case'], row['Sector'])
        
        # Build Prompt with Evidence
        strategic_prompt = create_strategic_prompt(row, web_info)
        
        # Store for AI processing
        final_output.append({
            "asset": row['Asset Name'],
            "web_search_evidence": web_info,
            "ai_analysis_prompt": strategic_prompt
        })

    # Save to JSON for the next step (LLM Inference)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=4)
    
    print(f"\nCOMPLETED. Results saved to {OUTPUT_FILE}")
    print("This JSON contains the real web data needed for accurate benchmarking.")

if __name__ == "__main__":
    main()