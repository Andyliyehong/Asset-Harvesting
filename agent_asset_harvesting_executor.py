import os
from typing import override, Any, Dict, Optional
import fitz  # PyMuPDF
from pathlib import Path
from a2a.server.agent_execution import AgentExecutor

class AssetHarvestingAgentExecutor(AgentExecutor):
    """Asset Harvesting AgentExecutor."""

    @override
    async def execute(self, task_input: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        Extracts text from PDF documents in a specified directory.
        """
        # 1. Validate Input
        if not task_input:
            return {"status": "error", "message": "No task_input provided."}
            
        source_path_str = task_input.get("source_folder")
        output_path_str = task_input.get("output_folder")
        
        if not source_path_str:
            return {"status": "error", "message": "source_folder path is required in task_input"}

        source_folder = Path(source_path_str)
        output_folder = Path(output_path_str) if output_path_str else source_folder / "extract_contents"

        # 2. Execution Logic
        if not source_folder.exists():
            return {"status": "error", "message": f"Source folder {source_folder} does not exist."}
        
        output_folder.mkdir(parents=True, exist_ok=True)
        harvested_files = []

        def extract_text_from_pdf(pdf_path):
            # 使用 context manager 确保文档关闭
            with fitz.open(pdf_path) as doc:
                full_text = ""
                for page_num, page in enumerate(doc):
                    full_text += f"\n--- Page {page_num + 1} ---\n"
                    full_text += page.get_text()
                return full_text

        try:
            # 查找所有 PDF
            pdf_files = list(source_folder.glob("*.pdf"))
            if not pdf_files:
                 return {"status": "success", "message": "No PDF files found.", "processed_count": 0}

            for file_path in pdf_files:
                extracted_text = extract_text_from_pdf(file_path)
                output_file = output_folder / f"{file_path.stem}_extracted.txt"
                
                # 写入提取的内容
                output_file.write_text(extracted_text, encoding="utf-8")
                harvested_files.append(str(output_file))
            
            return {
                "status": "success",
                "processed_count": len(harvested_files),
                "harvested_files": harvested_files,
                "output_location": str(output_folder)
            }
        except Exception as e:
            return {"status": "error", "message": f"Unexpected error: {str(e)}"}

    @override
    async def cancel(self) -> None:
        """Implement cancellation logic."""
        print("[!] Asset Harvesting task was cancelled.")
