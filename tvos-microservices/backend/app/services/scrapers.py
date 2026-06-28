import httpx
from moviebox_api.v2.core import Search
from app.config import settings

class MovieBoxService:
    def __init__(self):
        # 1. Create a persistent session for the moviebox library to use
        self.session = httpx.AsyncClient(timeout=15.0)

    async def search(self, query: str):
        try:
            # 2. Instantiate Search with the required session and query per request
            search_worker = Search(self.session, query)
            
            # The library likely returns the results via a property or a fetch/search method
            # We use a safe fallback to catch how the new version returns data
            if hasattr(search_worker, 'search'):
                results = await search_worker.search()
            elif hasattr(search_worker, 'fetch'):
                results = await search_worker.fetch()
            else:
                results = await search_worker.get_results()

            return [{"id": r.id, "title": getattr(r, 'title', 'Unknown'), "type": getattr(r, 'release_date', 'Unknown Year')} for r in results]
        except Exception as e:
            print(f"MovieBox Search Error: {e}")
            return []

    async def get_streams(self, media_id: int):
        try:
            # Pass a dummy query to satisfy the __init__ requirement so we can access the stream methods
            search_worker = Search(self.session, "")
            stream_data = await search_worker.get_stream_urls(media_id)
            
            url = getattr(stream_data, 'best_quality_url', None) or stream_data.get('url')
            if not url:
                return []
                
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

moviebox_client = MovieBoxService()
flixhq_client = FlixHQService()
