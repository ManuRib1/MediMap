"""
MediMap - Dashboard principal
Analyse territoriale de la consommation de médicaments en France
"""

import streamlit as st
from utils.api_client import get_overview, get_regions_stats
from utils.charts import format_number, format_currency, create_bar_chart
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="MediMap - Analyse Médicaments France",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("🏥 MediMap")
st.markdown("### Analyse territoriale de la consommation de médicaments en France")
st.markdown("---")

# Vérifier la connexion API
try:
    overview = get_overview(2023)
    
    if overview:
        # KPIs en haut
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💊 Total Boîtes",
                format_number(overview['total_boites'])
            )
        
        with col2:
            st.metric(
                "💰 Montant Remboursé",
                format_currency(overview['total_remb'])
            )
        
        with col3:
            st.metric(
                "🗺️ Régions",
                overview['nb_regions']
            )
        
        with col4:
            st.metric(
                "🔬 Médicaments",
                format_number(overview['nb_medicaments'])
            )
        
        st.markdown("---")
        
        # Graphique Top Régions
        st.subheader("🏆 Top Régions par Montant Remboursé (2023)")
        
        regions_stats = get_regions_stats(2023)
        if regions_stats:
            df = pd.DataFrame(regions_stats)
            
            # Top 10
            df_top = df.head(10).copy()
            df_top['total_remb_formatted'] = df_top['total_remb'].apply(lambda x: float(x))
            
            fig = create_bar_chart(
                df_top,
                x='total_remb_formatted',
                y='nom_region',
                title='',
                color='total_remb_formatted'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tableau des données
            st.markdown("#### 📋 Données détaillées")
            
            df_display = df.copy()
            df_display['total_boites'] = df_display['total_boites'].apply(format_number)
            df_display['total_remb'] = df_display['total_remb'].apply(lambda x: format_currency(x))
            df_display.columns = ['Code', 'Région', 'Total Boîtes', 'Montant Remboursé']
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    else:
        st.error("❌ Impossible de récupérer les données de l'API")
        
except Exception as e:
    st.error(f"❌ Erreur de connexion à l'API: {e}")
    st.info("💡 Assurez-vous que l'API FastAPI est bien lancée sur http://127.0.0.1:8000")

# Sidebar
with st.sidebar:
    st.header("ℹ️ À propos")
    st.markdown("""
    **MediMap** est un projet d'analyse de données qui visualise la consommation 
    de médicaments en France par région.
    
    **Source des données :**  
    OpenMedic (Assurance Maladie)
    
    **Année :** 2023
    
    **Technologies :**
    - FastAPI (Backend)
    - Streamlit (Frontend)
    - PostgreSQL (Base de données)
    - Plotly (Visualisations)
    """)
    
    st.markdown("---")
    st.markdown("🔗 **Navigation**")
    st.markdown("Utilisez le menu à gauche pour explorer les différentes pages.")