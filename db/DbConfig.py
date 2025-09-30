from config.settings import Settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

settings = Settings()

# Postgres engine creation
def get_db_url():
    host = "voting_db"  # Use the service name defined in docker-compose.yml
    "postgresql://<username>:<password>@<host>:<port>/<database_name>"
    return f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD.get_secret_value()}@{host}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

Engine = create_engine(
    get_db_url(),
)

SessionLocal = sessionmaker(bind=Engine)

Base = declarative_base()