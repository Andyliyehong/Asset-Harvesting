from agent_asset_harvesting_executor import AssetHarvestingAgentExecutor

async def test_dynamic_paths():
    executor = AssetHarvestingAgentExecutor()

    user_input = {
        "source_folder": "/Users/Andy.Li/Asset_Strategy/Asset Harvesting/source_data_folder",
        "output_folder": "/Users/Andy.Li/Asset_Strategy/Asset Harvesting/source_data_folder/extract_contents"
    }

    result = await executor.execute(task_input=user_input)
    print(result)

if __name__ == "__main__":
    test_dynamic_paths()