import os
from dotenv import load_dotenv
from pydantic import BaseSettings, BaseModel

load_dotenv()


class Settings(BaseSettings):
    # SMTP settings
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    EMAILS_FROM_NAME: str = "PHP Tutor Ivan"
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_PORT: int = os.getenv("MAIL_PORT")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS")
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS")
    USE_CREDENTIALS: bool = os.getenv("USE_CREDENTIALS")
    VALIDATE_CERTS: bool = os.getenv("VALIDATE_CERTS")

    # Swagger
    SWAGGER_URL: str = os.getenv("SWAGGER_URL")

    # Domain
    DOMAIN: str = os.getenv("DOMAIN")

    # DB Connection
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    # Bucket Connection
    BUCKET_DOMAIN = os.getenv('BUCKET_DOMAIN')
    AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
    AWS_BUCKET_REGION = os.getenv('AWS_BUCKET_REGION')
    AWS_BUCKET_KEY_ID = os.getenv('AWS_BUCKET_KEY_ID')
    AWS_BUCKET_SECRET_KEY = os.getenv('AWS_BUCKET_SECRET_KEY')

    # Third party API's
    LEAFLET = os.getenv('LEAFLET_DOMAIN')

    # Allowed hosts
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080",
    ]


settings = Settings()



class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "ivans_lesson"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }
