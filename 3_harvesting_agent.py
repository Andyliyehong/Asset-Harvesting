#Currently using Githup Copilot to do the harvesting work:
# prompts = "please follow the asset_harvest_prompt md file prompts"


import json
import pandas as pd
import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI # Using LangChain's Azure wrapper
from langchain_core.messages import HumanMessage

load_dotenv()

class Settings:
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", "2023-05-15")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")

settings = Settings()

def get_llm_client():
    """
    Initialize and cache the AzureChatOpenAI client.
    """
    print("--- Initializing Azure LLM Client ---")
    llm = AzureChatOpenAI(
        azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        api_version=settings.OPENAI_API_VERSION,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        api_key=settings.AZURE_OPENAI_KEY,
        temperature=0,
    )
    print("--- LLM Client Initialized Successfully ---")
    return llm

# Global initialization of LLM client
llm = get_llm_client()

# print(settings.AZURE_OPENAI_ENDPOINT)
prompt = """
You are a data validation assistant.
Return a JSON object with the following schema:
{
    "status": "success",
    "row_count": integer,
    "columns": list of strings
}
Assume a dataframe with 10 rows and columns: ["id", "name", "amount"]
"""

response = llm.invoke([
    HumanMessage(content=prompt)
])
print("LLM Response:", response.content)




# def harvest_chunk(chunk_text, schema):
#     prompt = f"""
#     You are an Asset Harvesting Agent. Extract project/asset info based on the taxonomy.
    
#     TAXONOMY SCHEMA:
#     {json.dumps(schema, indent=2)}

#     TEXT CHUNK:
#     {chunk_text}

#     INSTRUCTIONS:
#     1. Identify all distinct assets. Fill ALL columns. 
#     2. If info is missing, use "Unavailable".
#     3. Return ONLY a valid JSON object with an "assets" list.
#     """
    
#     try:
#         # LangChain's invocation method
#         response = llm.invoke([HumanMessage(content=prompt)])
        
#         # Handle possible Markdown formatting (```json ... ```)
#         content = response.content.strip()
#         if content.startswith("```json"):
#             content = content.split("```json")[1].split("```")[0].strip()
        
#         return json.loads(content).get("assets", [])
#     except Exception as e:
#         print(f"Error processing chunk: {e}")
#         return []

# def deduplicate_assets(all_assets):
#     unique_assets = {}
#     for asset in all_assets:
#         name = asset.get("Asset Name", "").strip()
#         if name and name != "Unavailable":
#             if name not in unique_assets:
#                 unique_assets[name] = asset
#             else:
#                 current_unavail = list(asset.values()).count("Unavailable")
#                 existing_unavail = list(unique_assets[name].values()).count("Unavailable")
#                 if current_unavail < existing_unavail:
#                     unique_assets[name] = asset
#     return list(unique_assets.values())

# if __name__ == "__main__":
#     # 1. Load local resources
#     with open('source_content.txt', 'r', encoding='utf-8') as f:
#         full_text = f.read()
#     with open('schema.json', 'r') as f:
#         schema = json.load(f)

#     # 2. Split text into chunks (Azure also has token limits, so chunking is recommended)
#     from chunk_utils import split_text # Assuming you put the previous split_text in utils, or paste it directly
#     chunks = [] 
#     # Reuse the previous split_text logic...
#     def split_text_internal(text, chunk_size=8000, overlap=1000):
#         res = []
#         start = 0
#         while start < len(text):
#             res.append(text[start:start + chunk_size])
#             start += (chunk_size - overlap)
#         return res
    
#     chunks = split_text_internal(full_text)
#     print(f"Total chunks to process: {len(chunks)}")

#     # 3. Loop through chunks and harvest assets
#     all_harvested_assets = []
#     for i, chunk in enumerate(chunks):
#         print(f"Processing chunk {i+1}/{len(chunks)}...")
#         chunk_assets = harvest_chunk(chunk, schema)
#         all_harvested_assets.extend(chunk_assets)

#     # 4. 去重与导出
#     final_assets = deduplicate_assets(all_harvested_assets)
#     if final_assets:
#         df = pd.DataFrame(final_assets)
#         # 确保列顺序一致[cite: 1]
#         original_cols = list(schema.keys())
#         df = df.reindex(columns=original_cols).fillna("Unavailable")
#         df.to_excel("Azure_Harvest_Result.xlsx", index=False)
#         print(f"Success! Extracted {len(final_assets)} assets.")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# import json
# import pandas as pd
# # from openai import OpenAI
# from google import genai
# from google.genai import types
# import os
# from dotenv import load_dotenv

# load_dotenv()
# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
# MODEL_ID = "gemini-2.5-flash"


# def split_text(text, chunk_size=8000, overlap=1000):
#     """Split text into chunks with overlap to prevent information loss across page breaks."""
#     chunks = []
#     start = 0
#     while start < len(text):
#         end = start + chunk_size
#         chunks.append(text[start:end])
#         start += (chunk_size - overlap)
#     return chunks

# def harvest_chunk(chunk_text, schema):
#     """Extract information from a single text chunk based on the taxonomy."""
#     prompt = f"""
#     You are an Asset Harvesting Agent. Extract project/asset info based on the taxonomy.
    
#     TAXONOMY SCHEMA:
#     {json.dumps(schema, indent=2)}

#     TEXT CHUNK:
#     {chunk_text}

#     INSTRUCTIONS:
#     1. Extract all distinct assets. Fill ALL columns. 
#     2. If info is missing, use "Unavailable".
#     3. Return a JSON object with an "assets" list.
#     """
    
#     try:
#         response = client.models.generate_content(
#             model=MODEL_ID,
#             contents=prompt,
#             config=types.GenerateContentConfig(
#                 response_mime_type="application/json",
#                 max_output_tokens=2048
#             )
#         )
#         return json.loads(response.text).get("assets", [])
#     except Exception as e:
#         print(f"Error processing chunk: {e}")
#         return []

# def deduplicate_assets(all_assets):
#     """Simple deduplication logic based on Asset Name."""
#     unique_assets = {}
#     for asset in all_assets:
#         name = asset.get("Asset Name", "").strip()
#         # If the name is valid and not already in the library, or the new record has more complete information (fewer "Unavailable"), keep it
#         if name and name != "Unavailable":
#             if name not in unique_assets:
#                 unique_assets[name] = asset
#             else:
#                 # Simple optimization: keep the version with fewer "Unavailable" fields
#                 current_unavail = list(asset.values()).count("Unavailable")
#                 existing_unavail = list(unique_assets[name].values()).count("Unavailable")
#                 if current_unavail < existing_unavail:
#                     unique_assets[name] = asset
#     return list(unique_assets.values())

# if __name__ == "__main__":
#     # 1. Load resources
#     with open('source_content.txt', 'r', encoding='utf-8') as f:
#         full_text = f.read()
#     with open('schema.json', 'r') as f:
#         schema = json.load(f)

#     # 2. Split text into chunks (each ~8000 characters, with 1000 character overlap to prevent asset descriptions from being cut off)
#     chunks = split_text(full_text)
#     print(f"Total chunks to process: {len(chunks)}")

#     # 3. Harvest loop
#     all_harvested_assets = []
#     for i, chunk in enumerate(chunks):
#         print(f"Processing chunk {i+1}/{len(chunks)}...")
#         chunk_assets = harvest_chunk(chunk, schema)
#         all_harvested_assets.extend(chunk_assets)

#     # 4. Deduplication and cleaning
#     final_assets = deduplicate_assets(all_harvested_assets)

#     # 5. Export to Excel
#     original_cols = list(schema.keys())
#     if final_assets:
#         # Ensure all assets have all columns, filling missing ones with "Unavailable"
#         df = pd.DataFrame(final_assets)
#         df = df.reindex(columns=original_cols).fillna("Unavailable")
#         df.to_excel("Harvest_Result.xlsx", index=False)
#         print(f"Done! Extracted {len(final_assets)} unique assets.")
#     else:
#         print("No assets were extracted.")