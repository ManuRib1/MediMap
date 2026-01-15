"""
Routes API pour les regions
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/regions",
    tags=["Régions"]
)

@router.get("/", response_model=List[schemas.Region])
def get_all_regions(db: Session = Depends(get_db)):
    """
    Récupère toutes les régions
    """
    regions = db.query(models.Region).all()
    return regions

@router.get("/{region_id}", response_model=schemas.Region)
def get_region(region_id: int, db: Session = Depends(get_db)):
    """
    Récupère une région par son ID
    """
    region = db.query(models.Region).filter(models.Region.id == region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Région non trouvée")
    return region

@router.get("/code/{code_region}", response_model=schemas.Region)
def get_region_by_code(code_region: int, db: Session = Depends(get_db)):
    """
    Récupère une région par son code (ex: 11 pour Île-de-France)
    """
    region = db.query(models.Region).filter(models.Region.code_region == code_region).first()
    if not region:
        raise HTTPException(status_code=404, detail="Région non trouvée")
    return region