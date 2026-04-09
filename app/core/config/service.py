import os
from dotenv import load_dotenv

from .interface import PROVIDER_MAP, ModelConfig, RedisConfig, Environment

load_dotenv()

class Config:
    @staticmethod
    def get_model_config(model):
        provider = PROVIDER_MAP.get(model)
        if provider is None:
            raise ValueError(f"Unknown model: {model}")

        api_key = os.getenv(f"{provider.upper()}_API_KEY")

        if api_key is None:
            raise ValueError(f"Unknown model, api key not setted: {model}")

        return ModelConfig(api_key=api_key, provider=provider, model=model.value)

    @staticmethod
    def get_database_connection_url():
        user = os.getenv('SQL_USER')
        password = os.getenv('SQL_PASSWORD')
        db_name = os.getenv('SQL_DB_NAME')
        host = os.getenv('SQL_DB_HOST')

        if (user is None):
            raise ValueError('SQL_USER is not set')

        if (password is None):
            raise ValueError('SQL_PASSWORD is not set')

        if (db_name is None):
            raise ValueError('SQL_DB_NAME is not set')

        if (host is None):
            raise ValueError('SQL_DB_HOST is not set')


        return f"postgresql+asyncpg://{user}:{password}@{host}/{db_name}"

    @staticmethod
    def get_redis_config() -> RedisConfig:
        host = os.getenv('REDIS_HOST')
        port = os.getenv('REDIS_PORT')
        username = os.getenv('REDIS_USERNAME')
        password = os.getenv('REDIS_PASSWORD')
        max_connections = os.getenv('REDIS_MAX_CONNECTIONS', 20)

        if host is None:
            raise ValueError('REDIS_HOST is not set')

        if port is None:
            raise ValueError('REDIS_PORT is not set')

        if username is None:
            raise ValueError('REDIS_USERNAME is not set')

        if password is None:
            raise ValueError('REDIS_PASSWORD is not set')

        return RedisConfig(
            host=host,
            port=int(port),
            username=username,
            password=password,
            max_connections=int(max_connections),
        )

    @staticmethod
    def get_session_ttl():
        ttl = os.getenv('SESSION_TTL', 3600 * 12) # 12 hours
        return int(ttl)

    @staticmethod
    def get_environment() -> Environment:
        env = os.getenv('ENVIRONMENT', 'development').lower()

        try:
            return Environment(env)
        except ValueError:
            raise ValueError(
                f"Invalid ENVIRONMENT value: {env}. "
                f"Must be one of: {', '.join([e.value for e in Environment])}"
            )
