import httpx
from fastapi import HTTPException
from async_lru import alru_cache
from app.config import settings

class TMDBService:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {settings.TMDB_API_TOKEN}", "accept": "application/json"}
        self.client = httpx.AsyncClient(base_url=settings.TMDB_BASE_URL, headers=self.headers, timeout=10.0)

    async def get_trending(self, media_type: str):
        headers = {
            "Authorization": f"Bearer {settings.TMDB_API_TOKEN}",
            "Accept": "application/json"
        }
        url = f"https://api.themoviedb.org/3/trending/{media_type}/day"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            # Add this print to verify what's being sent if it still fails
            if resp.status_code == 401:
                print(f"DEBUG: Failed with headers: {headers}")
            resp.raise_for_status()
            return resp.json()

    async def get_details(self, media_type, item_id):
        resp = await self.client.get(f"/{media_type}/{item_id}")
        resp.raise_for_status()
        return resp.json()

tmdb_client = TMDBService()
