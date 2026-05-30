import os


class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/one_a_two_b_game_dev",
    )
    API_PREFIX: str = "/api"


settings = Settings()
