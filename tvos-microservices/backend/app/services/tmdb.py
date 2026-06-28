import httpx
from app.config import settings

class TMDBService:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {settings.TMDB_API_TOKEN}", "accept": "application/json"}
        self.client = httpx.AsyncClient(base_url=settings.TMDB_BASE_URL, headers=self.headers, timeout=10.0)

    # Indent this method inside the class!
    async def get_trending(self, media_type: str):
        url = f"https://api.themoviedb.org/3/trending/{media_type}/day"
        resp = await self.client.get(url) # Use self.client already defined in __init__
        resp.raise_for_status()
        return resp.json()

    async def get_details(self, media_type, item_id):
        resp = await self.client.get(f"/{media_type}/{item_id}")
        resp.raise_for_status()
        return resp.json()

tmdb_client = TMDBService()
