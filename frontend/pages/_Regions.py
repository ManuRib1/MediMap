"""
Page Analyse par Région
"""

import streamlit as st
import pandas as pd
from utils.api_client import get_all_regions, get_region_stats
from utils.charts import format_number, format_currency

st.set_page_config(page_title="Régions - MediMap", page_icon="📊", layout="wide")

st.title("📊 Analyse par Région")
st.markdown("---")

# Récupérer toutes les régions
regions = get_all_regions()

if regions:
    # Créer un dictionnaire {nom: code}
    regions_dict = {r['nom_region']: r['code_region'] for r in regions}
    
    # Sélecteur de région
    region_selectionnee = st.selectbox(
        "Sélectionnez une région",
        options=sorted(regions_dict.keys())
    )
    
    code_region = regions_dict[region_selectionnee]
    
    # Sélecteur d'année
    annee = st.selectbox("Année", [2023], index=0)
    
    # Récupérer les stats
    stats = get_region_stats(code_region, annee)
    
    if stats and 'error' not in stats:
        st.markdown(f"## {stats['nom_region']}")
        st.markdown(f"**Code région :** {stats['code_region']}")
        st.markdown("---")
        
        # KPIs
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "💊 Total Boîtes",
                format_number(stats['total_boites'])
            )
        
        with col2:
            st.metric(
                "💰 Montant Remboursé",
                format_currency(stats['total_remb'])
            )
        
        st.markdown("---")
        
        # Comparaison avec la moyenne nationale
        st.markdown("### 📈 Comparaison nationale")
        
        # Récupérer toutes les régions pour calculer la moyenne
        from utils.api_client import get_regions_stats
        all_stats = get_regions_stats(annee)
        
        if all_stats:
            df_all = pd.DataFrame(all_stats)
            moyenne_nationale = df_all['total_remb'].astype(float).mean()
            remb_region = float(stats['total_remb'])
            
            diff = remb_region - moyenne_nationale
            pct_diff = (diff / moyenne_nationale) * 100
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Région",
                    format_currency(remb_region)
                )
            
            with col2:
                st.metric(
                    "Moyenne Nationale",
                    format_currency(moyenne_nationale)
                )
            
            with col3:
                st.metric(
                    "Écart",
                    f"{pct_diff:+.1f}%",
                    delta=format_currency(diff)
                )
            
            # Classement
            df_sorted = df_all.sort_values('total_remb', ascending=False).reset_index(drop=True)
            df_sorted.index = df_sorted.index + 1
            
            position = df_sorted[df_sorted['code_region'] == code_region].index[0]
            
            st.markdown(f"**Classement :** {position}ème région sur {len(df_sorted)}")
    
    else:
        st.warning("Aucune donnée disponible pour cette région")

else:
    st.error("Impossible de charger les régions")