from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "LocumMap Chennai API"
    environment: str = "development"
    database_url: str = "postgresql+psycopg2://locum:locum@localhost:5432/locum"
    jwt_secret: str = "change-me"
    google_maps_api_key: str = ""
    razorpay_key_id: str = ""
    razorpay_key_secret: str = ""

    service_area_min_lat: float = 12.82
    service_area_max_lat: float = 13.15
    service_area_min_lng: float = 80.1
    service_area_max_lng: float = 80.35


settings = Settings()
