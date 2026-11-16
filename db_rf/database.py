import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/db_rf")
# alguns provedores entregam "postgres://", que o SQLAlchemy não aceita
if DATABASE_url.startswith("postgres://"):
    DATABASE_url = DATABASE_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
