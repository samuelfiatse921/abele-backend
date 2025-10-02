from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = ""
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = "9wVlFPJtS4jSn4Foe2NmSlWVtdfEeLq3"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    UPLOAD_FOLDER: str = "uploads"
    ALLOWED_EXTENSIONS: str = ""
    MAX_FILE_SIZE_MB: str = ""
    VERCEL_API: str = ""
    VERCEL_TOKEN: str = ""
    BRAINTREE_MERCHANT_ID: str = ""
    BRAINTREE_PUBLIC_KEY: str = ""
    BRAINTREE_PRIVATE_KEY: str = ""
    BRAINTREE_ENV: str = ""
    HTTPX_TIMEOUT: str = ""
    DEFAULT_IMAGES_LIST: list[dict] = [
        {
            "fileName": "Filiprankovic Grobgaard",
            "filePath": "https://images.unsplash.com/photo-1737994872587-bf30f6e48049?q=80&w=987&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "fileName": "tommaowang",
            "filePath": "https://images.unsplash.com/photo-1758762641372-e3b52bf061d4?q=80&w=987&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "fileName": "Vitalygariev",
            "filePath": "https://images.unsplash.com/photo-1758613655882-d38d9bd2db94?q=80&w=2232&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "fileName": "kianzhang",
            "filePath": "https://images.unsplash.com/photo-1757413186849-7b13fe9e4e6d?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "fileName": "Vivianmarley",
            "filePath": "https://images.unsplash.com/photo-1756142006790-82ebc921ebea?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "fileName": "Sharleybeau",
            "filePath": "https://images.unsplash.com/photo-1756142007501-f5446097dfcc?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
        {
            "fileName": "Helenalopes",
            "filePath": "https://images.unsplash.com/photo-1584021756961-b5e21a1274a6?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
    ]
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
