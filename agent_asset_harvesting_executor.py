import os
from typing import override
import fitz # uv add pymupdf for PDF text extraction
from pathlib import Path
from a2a.server.agent_execution import AgentExecutor



class AssetHarvestingAgentExecutor(AgentExecutor):
    """Asset Harvesting AgentExecutor Example."""
    @override
    async def execute(self, task_input=None, **kwargs) -> None:
        """
        Extracts text from PDF, PPTX, TXT and Word documents in a specified directory and saves the extracted content to an output directory. 
        Expected task_input keys: 'source_folder' (required), 'output_folder' (optional).
        """
        # 1. Define paths as per requirements
        # self.source_folder = Path('/Users/Andy.Li/a2a_Asset_Strategy/demo/source_data_folder')  # Base directory for asset
    
        source_path_str = task_input.get("source_folder")
        output_path_str = task_input.get("output_folder")
        if not source_path_str:
            return {"status": "error", "message": "source_folder path is required in task_input"}

        source_folder = Path(source_path_str)

        if not output_path_str:
            output_folder = source_folder / "extract_contents"
        else:
            output_folder = Path(output_path_str)

        # 2. Execution Logic:
        if not source_folder.exists():
            return {"status": "error", "message": f"Source folder {source_folder} does not exist."}
        output_folder.mkdir(parents=True, exist_ok=True)
        harvested_files = []

        def extract_text_from_pdf(pdf_path):
            doc = fitz.open(pdf_path)
            full_text = ""
            for page_num, page in enumerate(doc):
                full_text += f"\n--- Page {page_num + 1} ---\n"
                full_text += page.get_text()
            return full_text

        try:
            for file_path in source_folder.glob("*.pdf"):
                extracted_text = extract_text_from_pdf(file_path)
                output_file = output_folder / f"{file_path.stem}_extracted.txt"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(extracted_text)
                
                harvested_files.append(str(output_file))
            return {
                "status": "success",
                "processed_count": len(harvested_files),
                "harvested_files": harvested_files,
                "output_location": str(output_folder)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @override
    async def cancel(self) -> None:
        """Implement cancellation logic if needed."""
        print("[!] Harvesting task was cancelled.")