from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define uma variável para a url do banco de dados
DATABASE_url = 'postgresql://postgres:postgres@localhost:5432/db_rf'

# Cria a comunicação do banco de dados com a api
engine = create_engine(DATABASE_url)

# Cria conexões temporárias com o banco de dados
SessionLocal = sessionmaker(bind=engine)

#A Base Declarativa é a base para criar as suas tabelas usando classes Python.
Base = declarative_base()
