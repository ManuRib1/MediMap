"""
Page Statistiques avancées
"""

import streamlit as st
import pandas as pd
from utils.api_client import get_overview, get_regions_stats
from utils.charts import create_pie_chart, format_number, format_currency

st.set_page_config(page_title="Stats - MediMap", page_icon="📈", layout="wide")

st.title("📈 Statistiques Avancées")
st.markdown("---")

# Vue d'ensemble
st.subheader("🌍 Vue d'ensemble nationale")

overview = get_overview(2023)

if overview:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Boîtes", format_number(overview['total_boites']))
    
    with col2:
        st.metric("Montant Remboursé", format_currency(overview['total_remb']))
    
    with col3:
        st.metric("Régions", overview['nb_regions'])
    
    with col4:
        st.metric("Médicaments", format_number(overview['nb_medicaments']))

st.markdown("---")

# Répartition par région
st.subheader("🥧 Répartition des remboursements par région")

regions_stats = get_regions_stats(2023)

if regions_stats:
    df = pd.DataFrame(regions_stats)
    df['total_remb_float'] = df['total_remb'].astype(float)
    
    # Camembert
    fig = create_pie_chart(
        df,
        values='total_remb_float',
        names='nom_region',
        title=''
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tableau avec pourcentages
    st.markdown("### 📊 Détails par région")
    
    total = df['total_remb_float'].sum()
    df['pourcentage'] = (df['total_remb_float'] / total * 100).round(2)
    
    df_display = df[['nom_region', 'total_boites', 'total_remb_float', 'pourcentage']].copy()
    df_display['total_boites'] = df_display['total_boites'].apply(format_number)
    df_display['total_remb_float'] = df_display['total_remb_float'].apply(format_currency)
    df_display['pourcentage'] = df_display['pourcentage'].apply(lambda x: f"{x}%")
    
    df_display.columns = ['Région', 'Total Boîtes', 'Montant Remboursé', '% du Total']
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)