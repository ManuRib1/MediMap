"""
Page Carte de France interactive avec Folium
"""

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from utils.api_client import get_regions_stats
from utils.charts import format_number, format_currency

st.set_page_config(page_title="Carte - MediMap", page_icon="🗺️", layout="wide")

st.title("🗺️ Carte de France - Consommation par Région")
st.markdown("---")

annee = st.selectbox("Année", [2023], index=0)

regions_stats = get_regions_stats(annee)

if regions_stats:
    df = pd.DataFrame(regions_stats)
    df['total_remb_float'] = df['total_remb'].astype(float)
    
    coords_regions = {
        "Ile-de-France": [48.8566, 2.3522],
        "Auvergne-Rhone-Alpes": [45.7640, 4.8357],
        "Nouvelle-Aquitaine": [44.8378, -0.5792],
        "Occitanie": [43.6047, 1.4442],
        "Hauts-de-France": [50.6292, 3.0573],
        "Provence-Alpes-Cote d'Azur": [43.2965, 5.3698],
        "Grand Est": [48.5734, 7.7521],
        "Pays de la Loire": [47.2184, -1.5536],
        "Normandie": [49.4432, 1.0993],
        "Bretagne": [48.1173, -1.6778],
        "Bourgogne-Franche-Comte": [47.2805, 5.0417],
        "Centre-Val de Loire": [47.9029, 1.9093]
    }
    
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles='OpenStreetMap')
    
    max_remb = df['total_remb_float'].max()
    min_remb = df['total_remb_float'].min()
    
    for idx, row in df.iterrows():
        if row['nom_region'] in coords_regions:
            coords = coords_regions[row['nom_region']]
            intensity = (row['total_remb_float'] - min_remb) / (max_remb - min_remb)
            red = int(255)
            green_blue = int(255 * (1 - intensity))
            color = f'#{red:02x}{green_blue:02x}{green_blue:02x}'
            radius = 10 + (intensity * 30)
            
            popup_html = f"""
            <div style="font-family: Arial; min-width: 200px;">
                <h4>{row['nom_region']}</h4>
                <p><b>Boîtes:</b> {format_number(row['total_boites'])}</p>
                <p><b>Remboursé:</b> {format_currency(row['total_remb_float'])}</p>
            </div>
            """
            
            folium.CircleMarker(
                location=coords, radius=radius, 
                popup=folium.Popup(popup_html, max_width=300),
                color=color, fill=True, fillColor=color, 
                fillOpacity=0.7, weight=2
            ).add_to(m)
    
    st_folium(m, width=None, height=600)
    
    st.markdown("---")
    st.markdown("### 🎨 Légende")
    st.markdown("""
    - **Taille des cercles** : Proportionnelle au montant
    - **Rouge foncé** : Montant élevé
    - **Cliquez** sur un cercle pour voir les détails
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Classement")
    
    df_display = df.sort_values('total_remb_float', ascending=False).copy()
    df_display['total_boites'] = df_display['total_boites'].apply(format_number)
    df_display['total_remb_float'] = df_display['total_remb_float'].apply(format_currency)
    df_display = df_display[['nom_region', 'total_boites', 'total_remb_float']]
    df_display.columns = ['Région', 'Total Boîtes', 'Montant Remboursé']
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)

else:
    st.error("Impossible de charger les données")