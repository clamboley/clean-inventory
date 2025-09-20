from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings configuration.

    This class defines the configuration settings for the application,
    including both application settings and PostgreSQL database configuration.
    Settings can be loaded from environment variables or a .env file.

    Attributes:
        app_host (str): The host address for the application. Defaults to "localhost".
        app_port (int): The port number for the application. Defaults to 8000.
        postgre_host (str): The host address for the PostgreSQL database. Defaults to "localhost".
        postgre_port (int): The port number for the PostgreSQL database. Defaults to 5432.
        postgre_user (str): The username for the PostgreSQL database.
        postgre_db (str): The name of the PostgreSQL database.
        postgre_password (str): The password for the PostgreSQL database.
        database_url (str): The full database URL constructed from the PostgreSQL configuration.
    """
    app_host: str = "localhost"
    app_port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Postgre config
    postgre_host: str = "localhost"
    postgre_port: int = 5432
    postgre_user: str = "inventory_user"
    postgre_db: str = "inventory_db"
    postgre_password: str = "strong_password"  # noqa: S105
    database_url: str = (
        f"postgresql+asyncpg://{postgre_user}:{postgre_password}"
        f"@{postgre_host}:{postgre_port}/{postgre_db}"
    )


config = Settings()
