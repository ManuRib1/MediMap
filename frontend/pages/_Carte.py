"""
Page Carte de France interactive
"""

import streamlit as st
import pandas as pd
from utils.api_client import get_regions_stats
from utils.charts import create_map_france

st.set_page_config(page_title="Carte - MediMap", page_icon="🗺️", layout="wide")

st.title("🗺️ Carte de France - Consommation par Région")
st.markdown("---")

# Sélecteur d'année
annee = st.selectbox("Année", [2023], index=0)

# Récupérer les données
regions_stats = get_regions_stats(annee)

if regions_stats:
    df = pd.DataFrame(regions_stats)
    
    # Mapping codes régions vers codes ISO
    code_iso_regions = {
        11: "FR-IDF", 24: "FR-CVL", 27: "FR-BFC", 28: "FR-NOR",
        32: "FR-HDF", 44: "FR-GES", 52: "FR-PDL", 53: "FR-BRE",
        75: "FR-NAQ", 76: "FR-OCC", 84: "FR-ARA", 93: "FR-PAC", 94: "FR-COR"
    }
    
    df['code_iso'] = df['code_region'].map(code_iso_regions)
    df['total_remb_float'] = df['total_remb'].astype(float)
    
    # Choix de la métrique
    metrique = st.radio(
        "Métrique à afficher",
        ["Montant remboursé (€)", "Nombre de boîtes"],
        horizontal=True
    )
    
    if metrique == "Montant remboursé (€)":
        color_col = 'total_remb_float'
        hover_data = ['total_boites', 'total_remb_float']
    else:
        color_col = 'total_boites'
        hover_data = ['total_boites', 'total_remb_float']
    
    # Créer la carte
    fig = create_map_france(
        df,
        locations='code_iso',
        color=color_col,
        hover_name='nom_region',
        title=f'Consommation de médicaments par région ({annee})'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistiques
    st.markdown("### 📊 Statistiques")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        max_region = df.loc[df['total_remb_float'].idxmax()]
        st.metric(
            "🥇 Région la plus élevée",
            max_region['nom_region'],
            f"{max_region['total_remb_float']:,.2f} €".replace(',', ' ')
        )
    
    with col2:
        min_region = df.loc[df['total_remb_float'].idxmin()]
        st.metric(
            "🥉 Région la plus basse",
            min_region['nom_region'],
            f"{min_region['total_remb_float']:,.2f} €".replace(',', ' ')
        )
    
    with col3:
        moyenne = df['total_remb_float'].mean()
        st.metric(
            "📈 Moyenne nationale",
            f"{moyenne:,.2f} €".replace(',', ' ')
        )

else:
    st.error("Impossible de charger les données")