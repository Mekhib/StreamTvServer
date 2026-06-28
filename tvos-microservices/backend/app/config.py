from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    TMDB_API_TOKEN: str = "placeholder"
    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"
    FLIXHQ_SERVICE_URL: str = "http://localhost:3000"
settings = Settings()
