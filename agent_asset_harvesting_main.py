import sys
import uvicorn
from typing import Any, Dict

# --- 1. RPC Patch (Keep at the top) ---
try:
    import a2a_json_rpc.spec
    if not hasattr(a2a_json_rpc.spec, 'TaskSendParams'):
        for alt in ['ExecuteTaskParams', 'TaskParams']:
            if hasattr(a2a_json_rpc.spec, alt):
                a2a_json_rpc.spec.TaskSendParams = getattr(a2a_json_rpc.spec, alt)
                break
except ImportError:
    pass

# --- 2. Imports ---
from a2a_server.app import create_app
from a2a_server.tasks.handlers.task_handler import TaskHandler
from agent_asset_harvesting_executor import AssetHarvestingAgentExecutor

# --- 3. Corrected Subclass ---
class AssetHarvestingHandler(TaskHandler):
    def __init__(self, executor: Any):
        super().__init__()
        self.executor = executor
        # Implementation for the abstract 'name' attribute
        self._name = "asset_harvesting"

    @property
    def name(self) -> str:
        return self._name

    # Implementation for the abstract method 'process_task'
    async def process_task(self, params: Any) -> Any:
        """
        The framework calls this method when a task is received.
        """
        # Ensure your executor has an 'execute' or similar method
        return await self.executor.execute(params)

if __name__ == '__main__':
    # Configuration
    handler_cfg = {
        "agent_card": {
            "name": "Asset Harvesting Agent",
            "description": "Extracts asset data from documents.",
            "version": "1.0.0",
            "capabilities": {"streaming": True},
            "skills": [{
                "id": "asset_harvesting",
                "name": "Asset Harvesting",
                "description": "Scan directories for asset data."
            }]
        }
    }

    # Initialize
    executor = AssetHarvestingAgentExecutor()
    request_handler = AssetHarvestingHandler(executor=executor)

    # App setup
    app = create_app(
        handlers=[request_handler],
        handlers_config={"asset_harvesting": handler_cfg}
    )

    uvicorn.run(app, host='0.0.0.0', port=10001)
