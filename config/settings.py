"""
Settings

Para produccion, configure los siguientes secretos en Google Cloud Secret Manager:

- pjecz_can_mayor_flask_expediente_virtual_api_key
- pjecz_can_mayor_flask_expediente_virtual_api_url
- pjecz_can_mayor_flask_host
- pjecz_can_mayor_flask_redis_url
- pjecz_can_mayor_flask_salt
- pjecz_can_mayor_flask_secret_key
- pjecz_can_mayor_flask_sqlalchemy_database_uri
- pjecz_can_mayor_flask_task_queue

Para desarrollo, debe crear un archivo .env con las variables de entorno:

- EXPEDIENTE_VIRTUAL_API_KEY
- EXPEDIENTE_VIRTUAL_API_URL
- HOST
- REDIS_URL
- SALT
- SECRET_KEY
- SQLALCHEMY_DATABASE_URI
- TASK_QUEUE
"""

import os
from functools import lru_cache

from dotenv import load_dotenv
from google.cloud import secretmanager
from pydantic_settings import BaseSettings

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID", "")  # Por defecto esta vacio, esto significa estamos en modo local
SERVICE_PREFIX = os.getenv("SERVICE_PREFIX", "pjecz_can_mayor_flask")


def get_secret(secret_id: str) -> str:
    """Get secret from google cloud secret manager"""

    # If not in google cloud, return environment variable
    if PROJECT_ID == "":
        return os.getenv(secret_id.upper(), "")

    # Create the secret manager client
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    secret = f"{SERVICE_PREFIX}_{secret_id}"
    name = client.secret_version_path(PROJECT_ID, secret, "latest")

    # Access the secret version
    response = client.access_secret_version(name=name)

    # Return the decoded payload
    return response.payload.data.decode("UTF-8")


class Settings(BaseSettings):
    """Settings"""

    EXPEDIENTE_VIRTUAL_API_KEY: str = get_secret("expediente_virtual_api_key")
    EXPEDIENTE_VIRTUAL_API_URL: str = get_secret("expediente_virtual_api_url")
    HOST: str = get_secret("host")
    REDIS_URL: str = get_secret("redis_url")
    SALT: str = get_secret("salt")
    SECRET_KEY: str = get_secret("secret_key")
    SQLALCHEMY_DATABASE_URI: str = get_secret("sqlalchemy_database_uri")
    TASK_QUEUE: str = get_secret("task_queue")

    class Config:
        """Load configuration"""

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            """Customise sources, first environment variables, then .env file, then google cloud secret manager"""
            return env_settings, file_secret_settings, init_settings


@lru_cache()
def get_settings() -> Settings:
    """Get Settings"""
    return Settings()
