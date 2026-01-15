"""
Routes API pour les statistiques
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List
from app import models, schemas
from app.database import get_db
from decimal import Decimal

router = APIRouter(
    prefix="/stats",
    tags=["Statistiques"]
)

@router.get("/regions", response_model=List[schemas.RegionStats])
def get_regions_stats(
    annee: int = Query(2023, description="Année"),
    db: Session = Depends(get_db)
):
    """
    Statistiques par région pour une année donnée
    """
    stats = db.query(
        models.Region.code_region,
        models.Region.nom_region,
        func.sum(models.Consommation.total_boites).label('total_boites'),
        func.sum(models.Consommation.total_remb).label('total_remb')
    ).join(
        models.Consommation, models.Region.id == models.Consommation.region_id
    ).filter(
        models.Consommation.annee == annee
    ).group_by(
        models.Region.code_region, models.Region.nom_region
    ).order_by(
        desc('total_remb')
    ).all()
    
    return [
        {
            "code_region": s.code_region,
            "nom_region": s.nom_region,
            "total_boites": s.total_boites,
            "total_remb": s.total_remb
        }
        for s in stats
    ]

@router.get("/region/{code_region}")
def get_region_stats(code_region: int, annee: int = 2023, db: Session = Depends(get_db)):
    """
    Statistiques détaillées d'une région
    """
    region = db.query(models.Region).filter(models.Region.code_region == code_region).first()
    if not region:
        return {"error": "Région non trouvée"}
    
    stats = db.query(
        func.sum(models.Consommation.total_boites).label('total_boites'),
        func.sum(models.Consommation.total_remb).label('total_remb')
    ).filter(
        models.Consommation.region_id == region.id,
        models.Consommation.annee == annee
    ).first()
    
    return {
        "code_region": region.code_region,
        "nom_region": region.nom_region,
        "annee": annee,
        "total_boites": int(stats.total_boites or 0),
        "total_remb": float(stats.total_remb or 0)
    }

@router.get("/overview")
def get_overview(annee: int = 2023, db: Session = Depends(get_db)):
    """
    Vue d'ensemble des statistiques nationales
    """
    total = db.query(
        func.sum(models.Consommation.total_boites).label('total_boites'),
        func.sum(models.Consommation.total_remb).label('total_remb'),
        func.count(func.distinct(models.Consommation.region_id)).label('nb_regions')
    ).filter(
        models.Consommation.annee == annee
    ).first()
    
    nb_medicaments = db.query(func.count(models.Medicament.id)).scalar()
    
    return {
        "annee": annee,
        "total_boites": int(total.total_boites or 0),
        "total_remb": float(total.total_remb or 0),
        "nb_regions": int(total.nb_regions or 0),
        "nb_medicaments": nb_medicaments
    }