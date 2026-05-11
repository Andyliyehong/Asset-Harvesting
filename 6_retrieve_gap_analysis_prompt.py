import json
from datetime import datetime

# --- Configuration ---
# Note: Ensure the model used has 'Web Browsing' capabilities enabled via tools
OUTPUT_PROMPT_FILE = '6_new_dynamic_benchmarking_task.md'

def generate_llm_search_instruction(asset_data):
    """
    Creates a high-context instruction for a browsing-capable LLM.
    """
    current_date = datetime.now().strftime("%Y-%m")
    
    # Constructing a 'Search + Analyze' prompt
    prompt = f"""
### STEP 1: WEB RESEARCH MISSION
Search the internet for the most current (2024-2026) information regarding:
- Asset Focus: {asset_data['Asset Name']}
- Domain: {asset_data['Asset Description']}
- Target Industry: {asset_data['Sector']}
- Core Function: {asset_data['Primary Use Case']}

Specifically, look for 'Winning Assets', 'Gartner Magic Quadrant leaders', and 'Market Challengers' in the PFEP and Industrial Inventory Optimization space.

### STEP 2: COMPETITIVE DEEP-DIVE
Based on your search results, identify the Top 3 COTS (Commercial Off-The-Shelf) competitors. Compare them against our asset based on:
1. Functional Granularity (Can they do 'Part-level' as well as we do?)
2. Integration effort for Industrial Product (IP) companies.
3. Market proven ROI vs our 'Evidence of Value'.

### STEP 3: OUTPUT REQUIREMENTS
Generate the final analysis and save it as a JSON block.
- Report ID: GAP_ANALYSIS_{current_date}
- Format:
{{
    "asset_name": "{asset_data['Asset Name']}",
    "market_standing": "Leader/Challenger/Niche",
    "benchmarking": {{
        "top_3_competitors": [],
        "pros": [],
        "cons": [],
        "functional_gaps": []
    }},
    "improvement_suggestions": [],
    "reference_links": []
}}
"""
    return prompt

# Example asset for testing
pfep_asset = {
    "Asset Name": "PFEP/IVO Core Platform",
    "Asset Description": "Empowers organizations to standardize and scale part‑level planning, inventory, and replenishment decisions by unifying data, analytics, and planning processes into a centralized PFEP platform—enabling faster, more confident decisions across sites, functions, and value streams.",
    "Sector": "IP - Industrial Product",
    "AI Feature": "No AI",
    "Primary Use Case": "Provide a centralized PFEP foundation for scalable part‑level planning and execution."
}

# Generate the MD file for Copilot/ChatGPT
with open(OUTPUT_PROMPT_FILE, 'w', encoding='utf-8') as f:
    f.write(generate_llm_search_instruction(pfep_asset))

print(f"Instruction generated in {OUTPUT_PROMPT_FILE}. You can now paste this into a browsing-enabled AI.")



# import json
# import os

# # --- Configuration ---
# INPUT_JSON = '/Users/Andy.Li/Asset_Strategy/Asset Harvesting/6_External_Market_Analysis.json'
# OUTPUT_MD = '/Users/Andy.Li/Asset_Strategy/Asset Harvesting/6_gap_analysis_prompt.md'

# def generate_gap_analysis_prompt_task():
#     """
#     Reads the research JSON and transforms it into a structured Markdown 
#     for GitHub Copilot or ChatGPT to process.
#     """
#     if not os.path.exists(INPUT_JSON):
#         print(f"Error: {INPUT_JSON} not found. Please run the research script first.")
#         return

#     with open(INPUT_JSON, 'r', encoding='utf-8') as f:
#         research_data = json.load(f)

#     md_content = []
    
#     # 1. System Header
#     md_content.append("# Strategic Benchmarking Task for GitHub Copilot\n")
#     md_content.append("## Role: Strategic Market Analyst\n")
#     md_content.append("Please analyze the following assets based on the provided internal data and external web evidence.\n")

#     # 2. Asset Specific Sections
#     for entry in research_data:
#         asset_name = entry.get('asset', 'Unknown Asset')
#         web_evidence = entry.get('web_search_evidence', [])
        
#         md_content.append(f"### Asset Analysis: {asset_name}")
#         md_content.append("#### [Internal Metadata & Instruction]")
#         md_content.append(entry.get('ai_analysis_prompt', 'No prompt generated.'))
        
#         md_content.append("#### [Raw Market Evidence Found]")
#         if not web_evidence:
#             md_content.append("- No specific web evidence found. Please use your general knowledge of COTS in this sector.")
#         else:
#             for i, evidence in enumerate(web_evidence, 1):
#                 md_content.append(f"{i}. **{evidence['competitor_source']}**")
#                 md_content.append(f"   - Snippet: {evidence['description']}")
#                 md_content.append(f"   - Link: {evidence['link']}")
        
#         md_content.append("\n---\n")

#     # 3. Final Critical Instruction
#     md_content.append("## CRITICAL FINAL INSTRUCTION")
#     md_content.append("After performing the analysis for all assets above, you MUST consolidate the output into a single JSON object.")
#     md_content.append("The final JSON must follow the schema below and you must prompt the user to save it as `6_gap_analysis.json`.")
    
#     json_schema = {
#         "report_id": "GAP_ANALYSIS_2026_May",
#         "assets": [
#             {
#                 "asset_name": "Name",
#                 "market_standing": "Leader/Challenger/Niche",
#                 "benchmarking": {
#                     "top_3_competitors": [],
#                     "pros": [],
#                     "cons": [],
#                     "functional_gaps": []
#                 },
#                 "improvement_suggestions": []
#             }
#         ]
#     }
    
#     md_content.append(f"```json\n{json.dumps(json_schema, indent=4)}\n```")
#     md_content.append("\n**IMPORTANT: Ensure the JSON is complete and valid before finishing.**")

#     # Write to file
#     with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
#         f.write("\n".join(md_content))

#     print(f"Success! Please feed '{OUTPUT_MD}' to GitHub Copilot or ChatGPT.")

# if __name__ == "__main__":
#     generate_gap_analysis_prompt_task()