"""
Modeles SQLAlchemy pour les tables de la base de donnees
"""

from sqlalchemy import Column, Integer, String, BigInteger, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Region(Base):
    __tablename__ = "regions"
    
    id = Column(Integer, primary_key=True, index=True)
    code_region = Column(Integer, unique=True, nullable=False)
    nom_region = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relations
    consommations = relationship("Consommation", back_populates="region")

class Medicament(Base):
    __tablename__ = "medicaments"
    
    id = Column(Integer, primary_key=True, index=True)
    code_cip = Column(String(20), unique=True, nullable=False)
    nom_medicament = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relations
    consommations = relationship("Consommation", back_populates="medicament")

class ClasseTherapeutique(Base):
    __tablename__ = "classes_therapeutiques"
    
    id = Column(Integer, primary_key=True, index=True)
    code_atc = Column(String(10), unique=True, nullable=False)
    nom_classe = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Consommation(Base):
    __tablename__ = "consommation"
    
    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=True)
    medicament_id = Column(Integer, ForeignKey("medicaments.id"), nullable=True)
    annee = Column(Integer, nullable=False)
    total_boites = Column(BigInteger, nullable=False)
    total_remb = Column(Numeric(15, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relations
    region = relationship("Region", back_populates="consommations")
    medicament = relationship("Medicament", back_populates="consommations")