"""
Routes API pour les medicaments
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/medicaments",
    tags=["Médicaments"]
)

@router.get("/", response_model=List[schemas.Medicament])
def get_all_medicaments(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupère tous les médicaments (paginés)
    """
    medicaments = db.query(models.Medicament).offset(skip).limit(limit).all()
    return medicaments

@router.get("/search", response_model=List[schemas.Medicament])
def search_medicaments(
    q: str = Query(..., min_length=3, description="Terme de recherche (min 3 caractères)"),
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Recherche de médicaments par nom
    """
    medicaments = db.query(models.Medicament)\
        .filter(models.Medicament.nom_medicament.ilike(f"%{q}%"))\
        .limit(limit)\
        .all()
    return medicaments

@router.get("/{medicament_id}", response_model=schemas.Medicament)
def get_medicament(medicament_id: int, db: Session = Depends(get_db)):
    """
    Récupère un médicament par son ID
    """
    medicament = db.query(models.Medicament).filter(models.Medicament.id == medicament_id).first()
    if not medicament:
        raise HTTPException(status_code=404, detail="Médicament non trouvé")
    return medicament