import sys

# ── 1. 解决 TaskSendParams 导入失败的“补丁” (必须放在最前面) ──────
try:
    import a2a_json_rpc.spec
    if not hasattr(a2a_json_rpc.spec, 'TaskSendParams'):
        # 尝试映射新版名称
        for alt in ['ExecuteTaskParams', 'TaskParams']:
            if hasattr(a2a_json_rpc.spec, alt):
                a2a_json_rpc.spec.TaskSendParams = getattr(a2a_json_rpc.spec, alt)
                break
        else:
            # 如果都没找到，伪造一个，防止程序崩溃
            class Dummy: pass
            a2a_json_rpc.spec.TaskSendParams = Dummy
except ImportError:
    pass

# ── 2. 正确的导入路径 ──────────────────────────────────────────────────
from a2a_server.app import create_app
from a2a_server.request_handlers import DefaultRequestHandler
from a2a_server.tasks import InMemoryTaskStore
# 根据之前的路径推测，这里可能也需要下划线
from a2a_types import AgentCapabilities, AgentCard, AgentSkill 
from asset_harvesting_executor import AssetHarvestingExecutor

if __name__ == '__main__':
    # 1. 定义 Skill
    skill = AgentSkill(
        id='asset_harvesting',
        name='Asset Harvesting Agent',
        description='Specialized in scanning directories and extracting asset data from documents.',
        tags=['asset harvesting', 'document processing'],
        examples=['Harvest assets from directory: /path/to/data'],
    )

    # 2. 定义 Agent Card
    agent_card = AgentCard(
        name='Asset Harvesting Agent',
        description='Converts unstructured data into structured asset information.',
        url='http://localhost:10001/',
        version='1.0.0',
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    # 3. 初始化 Executor 和 Handler
    # 注意：这里的 DefaultRequestHandler 必须符合 a2a_server 的要求
    executor = AssetHarvestingExecutor()
    request_handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=InMemoryTaskStore(),
    )

    # 4. 使用工厂函数创建 app (这是最重要的改变)
    # create_app 接受一个 handlers 列表
    app = create_app(
        handlers=[request_handler]
    )

    # 5. 启动服务器
    import uvicorn
    # 注意：不再调用 server.build()，因为 create_app 返回的就是 FastAPI 实例
    uvicorn.run(app, host='0.0.0.0', port=10001)
