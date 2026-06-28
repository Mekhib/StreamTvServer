import httpx
from fastapi import HTTPException
from async_lru import alru_cache
from app.config import settings

class TMDBService:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {settings.TMDB_API_TOKEN}", "accept": "application/json"}
        self.client = httpx.AsyncClient(base_url=settings.TMDB_BASE_URL, headers=self.headers, timeout=10.0)

    async def get_trending(self, media_type="movie", time_window="day"):
        resp = await self.client.get(f"/trending/{media_type}/{time_window}")
        resp.raise_for_status()
        data = resp.json().get("results", [])
        for i in data:
            i["poster_url"] = f"https://image.tmdb.org/t/p/w500{i.get('poster_path')}" if i.get('poster_path') else None
        return data

    async def get_details(self, media_type, item_id):
        resp = await self.client.get(f"/{media_type}/{item_id}")
        resp.raise_for_status()
        return resp.json()

tmdb_client = TMDBService()
