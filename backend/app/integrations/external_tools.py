from typing import List, Dict, Any
import httpx
from app.core.config import settings

class TrelloIntegration:
    def __init__(self):
        self.api_key = settings.TRELLO_API_KEY
        self.token = settings.TRELLO_TOKEN
        self.base_url = "https://api.trello.com/1"

    async def create_card(self, list_id: str, name: str, desc: str = ""):
        print(f"Mock: Creating Trello card '{name}' in list {list_id}")
        return {"id": "mock_card_id", "name": name}

    async def get_lists(self, board_id: str):
        print(f"Mock: Getting lists for board {board_id}")
        return []

class NotionIntegration:
    def __init__(self):
        self.api_key = settings.NOTION_API_KEY
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

    async def create_page(self, database_id: str, properties: Dict[str, Any]):
        print(f"Mock: Creating Notion page in database {database_id}")
        return {"id": "mock_page_id"}

    async def query_database(self, database_id: str, filter: Dict[str, Any] = None):
        print(f"Mock: Querying Notion database {database_id}")
        return {"results": []}
