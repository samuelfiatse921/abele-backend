from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = ""
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = "9wVlFPJtS4jSn4Foe2NmSlWVtdfEeLq3"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    BRAINTREE_MERCHANT_ID: str = ""
    BRAINTREE_PUBLIC_KEY: str = ""
    BRAINTREE_PRIVATE_KEY: str = ""
    BRAINTREE_ENV: str = ""
    HTTPX_TIMEOUT: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
