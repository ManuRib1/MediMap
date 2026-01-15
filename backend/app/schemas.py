"""
Schemas Pydantic pour la validation et serialisation des donnees
"""

from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

# ============================================================
# REGIONS
# ============================================================

class RegionBase(BaseModel):
    code_region: int
    nom_region: str

class RegionCreate(RegionBase):
    pass

class Region(RegionBase):
    id: int
    
    class Config:
        from_attributes = True

# ============================================================
# MEDICAMENTS
# ============================================================

class MedicamentBase(BaseModel):
    code_cip: str
    nom_medicament: str

class MedicamentCreate(MedicamentBase):
    pass

class Medicament(MedicamentBase):
    id: int
    
    class Config:
        from_attributes = True

# ============================================================
# CLASSES THERAPEUTIQUES
# ============================================================

class ClasseTherapeutiqueBase(BaseModel):
    code_atc: str
    nom_classe: str

class ClasseTherapeutique(ClasseTherapeutiqueBase):
    id: int
    
    class Config:
        from_attributes = True

# ============================================================
# CONSOMMATION
# ============================================================

class ConsommationBase(BaseModel):
    region_id: Optional[int] = None
    medicament_id: Optional[int] = None
    annee: int
    total_boites: int
    total_remb: Decimal

class Consommation(ConsommationBase):
    id: int
    
    class Config:
        from_attributes = True

# ============================================================
# SCHEMAS PERSONNALISES (pour les stats)
# ============================================================

class RegionStats(BaseModel):
    """Stats d'une region"""
    code_region: int
    nom_region: str
    total_boites: int
    total_remb: Decimal
    
    class Config:
        from_attributes = True

class MedicamentTop(BaseModel):
    """Top medicaments"""
    code_cip: str
    nom_medicament: str
    total_boites: int
    total_remb: Decimal
    
    class Config:
        from_attributes = True