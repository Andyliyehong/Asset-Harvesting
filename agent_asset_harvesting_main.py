from a2a.server.app import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from asset_harvesting_executor import AssetHarvestingExecutor

    
if __name__ == '__main__':
    # 1. Define the skill that the agent will perform
    skill = AgentSkill(
        id='asset_harvesting',
        name='Asset Harvesting Agent',
        description='Specialized in scanning directories and extracting asset data from PDF, PPTX, TXT and Word documents using generative AI.',
        tags=['asset harvesting', 'document processing', 'data extraction', 'asset collection'],
        examples=[
            'Harvest assets from directory: /path/to/directory',
            'Extract data from PDF: /path/to/document.pdf',
            'Scan PPTX for assets: /path/to/presentation.pptx',
            'Process Word document for asset data: /path/to/document.docx'
            ],
    )

    # 2.Define the agent card with metadata and capabilities
    agent_card = AgentCard(
        name='Asset Harvesting Agent',
        description='Converts unstructured data from various document formats into structured asset information, enabling efficient asset management and utilization.',
        url='http://localhost:10001/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    # 3. Request handler: links the A2A interface to your python logic
    request_handler = DefaultRequestHandler(
        agent_executor=AssetHarvestingExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )
    import uvicorn

    uvicorn.run(server.build(), host='0.0.0.0', port=10001)
