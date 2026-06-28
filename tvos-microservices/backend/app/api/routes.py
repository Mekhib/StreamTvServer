from fastapi import APIRouter
from app.services.tmdb import tmdb_client
from app.services.scrapers import moviebox_client, flixhq_client

router = APIRouter(prefix="/api/v1")

# --- 1. TMDB UI Layouts ---
@router.get("/ui/home")
async def get_home():
    return {
        "movies": await tmdb_client.get_trending("movie"),
        "shows": await tmdb_client.get_trending("tv")
    }

# --- 2. Master Search (Searches both networks simultaneously) ---
@router.get("/sources/search")
async def search_all_sources(query: str):
    return {
        "moviebox": await moviebox_client.search(query),
        "flixhq": await flixhq_client.search(query)
    }

# --- 3. FlixHQ Information & Episode List ---
@router.get("/sources/flixhq/info")
async def flixhq_info(media_id: str):
    return await flixhq_client.get_info(media_id)

# --- 4. Stream Link Extraction ---
@router.get("/sources/flixhq/stream")
async def stream_flixhq(media_id: str, episode_id: str):
    return {"links": await flixhq_client.get_streams(media_id, episode_id)}

@router.get("/sources/moviebox/stream")
async def stream_moviebox(media_id: int):
    return {"links": await moviebox_client.get_streams(media_id)}
