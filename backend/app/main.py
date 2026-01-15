"""
API FastAPI pour MediMap
Analyse territoriale de la consommation de medicaments en France
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import regions, medicaments, stats

# Créer l'application FastAPI
app = FastAPI(
    title="MediMap API",
    description="API d'analyse territoriale de la consommation de médicaments en France (données OpenMedic)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS (pour autoriser les requêtes depuis le frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(regions.router)
app.include_router(medicaments.router)
app.include_router(stats.router)

# Route racine
@app.get("/")
def root():
    """
    Endpoint racine - Informations sur l'API
    """
    return {
        "message": "Bienvenue sur MediMap API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "regions": "/regions",
            "medicaments": "/medicaments",
            "stats": "/stats"
        }
    }

# Health check
@app.get("/health")
def health_check():
    """
    Vérification de l'état de l'API
    """
    return {"status": "ok", "service": "MediMap API"}