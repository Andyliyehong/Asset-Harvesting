import sys
import uvicorn

# --- 1. RPC 补丁 (保持不变) ---
import a2a_json_rpc.spec
if not hasattr(a2a_json_rpc.spec, 'TaskSendParams'):
    for alt in ['ExecuteTaskParams', 'TaskParams']:
        if hasattr(a2a_json_rpc.spec, alt):
            a2a_json_rpc.spec.TaskSendParams = getattr(a2a_json_rpc.spec, alt)
            break

# --- 2. 修正后的导入 (根据 app.py 源码推断) ---
from a2a_server.app import create_app
from a2a_server.tasks.task_manager import TaskManager
from a2a_server.tasks.handlers.task_handler import TaskHandler # 核心改变
from a2a_server.tasks import InMemoryTaskStore

# 这里的 types 如果还报错，尝试 a2a_types 或 a2a.types
try:
    from a2a_types import AgentCard, AgentSkill, AgentCapabilities
except ImportError:
    from a2a.types import AgentCard, AgentSkill, AgentCapabilities

from asset_harvesting_executor import AssetHarvestingExecutor

if __name__ == '__main__':
    # 1. 配置 Skill 和 Card (同前)
    skill = AgentSkill(id='asset_harvesting', name='Asset Harvesting', description='...', tags=[], examples=[])
    agent_card = AgentCard(name='Asset Harvesting Agent', description='...', url='http://localhost:10001/', version='1.0.0', capabilities=AgentCapabilities(streaming=True), skills=[skill])

    # 2. 初始化 Executor
    executor = AssetHarvestingExecutor()

    # 3. 如果找不到 DefaultRequestHandler，我们直接用 TaskHandler 包装
    # TaskHandler 通常接受 name 和 executor
    request_handler = TaskHandler(
        name="asset_harvesting", # 这里的名字最好和 skill id 一致
        agent_executor=executor
    )

    # 4. 创建 App
    # 根据 app.py: def create_app(handlers: Optional[List[TaskHandler]] = None, ...)
    app = create_app(
        handlers=[request_handler]
    )

    # 5. 启动
    uvicorn.run(app, host='0.0.0.0', port=10001)
