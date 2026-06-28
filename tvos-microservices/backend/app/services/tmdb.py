import httpx
from app.config import settings

class TMDBService:
    def __init__(self):
      
        self.api_key = settings.TMDB_API_KEY 
        self.params = {"api_key": self.api_key, "language": "en-US"}
        self.client = httpx.AsyncClient(base_url=settings.TMDB_BASE_URL, timeout=10.0)

    async def get_trending(self, media_type: str):
        url = f"/trending/{media_type}/day"
        # Pass the params here
        resp = await self.client.get(url, params=self.params)
        resp.raise_for_status()
        return resp.json()
    async def get_details(self, media_type, item_id):
        resp = await self.client.get(f"/{media_type}/{item_id}")
        resp.raise_for_status()
        return resp.json()

tmdb_client = TMDBService()
