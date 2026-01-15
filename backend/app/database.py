"""
Configuration de la connexion a la base de donnees PostgreSQL
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL non trouvee dans le fichier .env")

# Creer le moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Creer une session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modeles
Base = declarative_base()

# Dependency pour obtenir une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()