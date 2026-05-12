import asyncio
# 确保文件名匹配
from agent_asset_harvesting_executor import AssetHarvestingAgentExecutor

async def test_dynamic_paths():
    executor = AssetHarvestingAgentExecutor()

    user_input = {
        "source_folder": "/Users/Andy.Li/Asset_Strategy/Asset Harvesting/source_data_folder",
        "output_folder": "/Users/Andy.Li/Asset_Strategy/Asset Harvesting/source_data_folder/extract_contents"
    }

    print("[*] Starting extraction test...")
    # 必须 await 异步方法
    result = await executor.execute(task_input=user_input)
    print("\n--- Test Result ---")
    print(result)

if __name__ == "__main__":
    # Python 异步运行的正确方式
    try:
        asyncio.run(test_dynamic_paths())
    except KeyboardInterrupt:
        pass
