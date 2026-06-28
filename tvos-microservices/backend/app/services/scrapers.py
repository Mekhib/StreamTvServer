import httpx
from moviebox_api.v2.core import Search
from app.config import settings

class MovieBoxService:
    def __init__(self):
        # We initialize the session here, but NOT the Search class yet
        self.session = httpx.AsyncClient(timeout=15.0)

    async def search(self, query: str):
        try:
            # Instantiate Search per-request, passing session and query
            search_worker = Search(self.session, query)
            # The library v0.5.4+ uses .search()
            results = await search_worker.search()
            return [{"id": r.id, "title": r.title, "type": getattr(r, 'release_date', 'Unknown Year')} for r in results]
        except Exception as e:
            print(f"MovieBox Search Error: {e}")
            return []

    async def get_streams(self, media_id: int):
        try:
            # We must still pass a dummy query to satisfy the __init__ requirements
            search_worker = Search(self.session, "")
            stream_data = await search_worker.get_stream_urls(media_id)
            url = getattr(stream_data, 'best_quality_url', None) or stream_data.get('url')
            return [{"server": "MovieBox Server 1", "sources": [{"url": url, "quality": "auto"}]}]
        except Exception as e:
            print(f"MovieBox Stream Error: {e}")
            return []

class FlixHQService:
    def __init__(self):
        self.base_url = settings.FLIXHQ_SERVICE_URL

    async def search(self, query: str):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/search", params={"query": query})
            return resp.json().get("results", []) if resp.status_code == 200 else []

    async def get_info(self, media_id: str):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/info", params={"mediaId": media_id})
            return resp.json()

    async def get_streams(self, media_id: str, episode_id: str):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/sources", params={"mediaId": media_id, "episodeId": episode_id})
            return resp.json().get("sources", [])

# Ensure these are initialized properly
moviebox_client = MovieBoxService()
flixhq_client = FlixHQService()
