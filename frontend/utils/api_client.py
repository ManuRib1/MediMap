"""
Client pour interroger l'API FastAPI
"""

import requests
import streamlit as st

# URL de base de l'API
API_BASE_URL = "https://medimap-api.onrender.com"

@st.cache_data(ttl=300)  # Cache pendant 5 minutes
def get_overview(annee=2023):
    """Récupère la vue d'ensemble"""
    try:
        response = requests.get(f"{API_BASE_URL}/stats/overview?annee={annee}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur API: {e}")
        return None

@st.cache_data(ttl=300)
def get_all_regions():
    """Récupère toutes les régions"""
    try:
        response = requests.get(f"{API_BASE_URL}/regions")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur API: {e}")
        return []

@st.cache_data(ttl=300)
def get_regions_stats(annee=2023):
    """Récupère les stats de toutes les régions"""
    try:
        response = requests.get(f"{API_BASE_URL}/stats/regions?annee={annee}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur API: {e}")
        return []

@st.cache_data(ttl=300)
def get_region_stats(code_region, annee=2023):
    """Récupère les stats d'une région spécifique"""
    try:
        response = requests.get(f"{API_BASE_URL}/stats/region/{code_region}?annee={annee}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur API: {e}")
        return None

@st.cache_data(ttl=300)
def search_medicaments(query):
    """Recherche de médicaments"""
    try:
        response = requests.get(f"{API_BASE_URL}/medicaments/search?q={query}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur API: {e}")
        return []

@st.cache_data(ttl=300)
def get_medicaments(skip=0, limit=100):
    """Récupère la liste des médicaments"""
    try:
        response = requests.get(f"{API_BASE_URL}/medicaments?skip={skip}&limit={limit}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur API: {e}")
        return []