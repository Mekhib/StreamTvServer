import traceback
import httpx
from moviebox_api.v2.core import Search
from moviebox_api.v1.requests import Session 
from app.config import settings

class MovieBoxService:
    def __init__(self):
        self.session = Session()

    async def search(self, query: str):
        try:
            search_worker = Search(self.session, query)
            results = await search_worker.search()
            return [{"id": r.id, "title": r.title, "type": "movie"} for r in results]
        except Exception as e:
            print("--- MOVIEBOX ERROR ---")
            traceback.print_exc() 
            return []

    async def get_streams(self, media_id: int):
        try:
            # We must still pass a dummy query to satisfy the requirements
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
            try:
                resp = await client.get(f"{self.base_url}/search", params={"query": query})
                if resp.status_code != 200:
                    print(f"--- FLIXHQ ERROR: Status {resp.status_code} ---")
                    print(f"Response: {resp.text}")
                    return []
                return resp.json().get("results", [])
            except Exception as e:
                print("--- FLIXHQ CONNECTION ERROR ---")
                traceback.print_exc()
                return []

    async def get_info(self, media_id: str):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/info", params={"mediaId": media_id})
            return resp.json()

    async def get_streams(self, media_id: str, episode_id: str):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/sources", params={"mediaId": media_id, "episodeId": episode_id})
            return resp.json().get("sources", [])

# Initialize clients
moviebox_client = MovieBoxService()
flixhq_client = FlixHQService()
