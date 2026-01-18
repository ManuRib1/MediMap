import streamlit as st
import pandas as pd
from utils.api_client import search_medicaments, get_medicaments

st.set_page_config(page_title="Médicaments - MediMap", page_icon="💊", layout="wide")

st.title("💊 Recherche de Médicaments")
st.markdown("---")

# Barre de recherche
query = st.text_input(
    "Rechercher un médicament",
    placeholder="Entrez au moins 3 caractères...",
    help="Recherche par nom de médicament"
)

if query and len(query) >= 3:
    # Recherche avec spinner
    with st.spinner("⏳ Recherche en cours..."):
        results = search_medicaments(query)
    
    if results:
        st.success(f"✅ {len(results)} résultat(s) trouvé(s)")
        df = pd.DataFrame(results)
        df = df[['code_cip', 'nom_medicament']]
        df.columns = ['Code CIP', 'Nom du médicament']
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("Aucun résultat trouvé")

elif query and len(query) < 3:
    st.info("Entrez au moins 3 caractères pour lancer la recherche")

else:
    # Afficher quelques médicaments par défaut
    st.markdown("### 📋 Liste des médicaments (100 premiers)")
    
    # AVEC SPINNER - BIEN INDENTÉ
    with st.spinner("⏳ Chargement des médicaments (l'API peut prendre 30s à se réveiller)..."):
        medicaments = get_medicaments(skip=0, limit=100)
    
    if medicaments:
        df = pd.DataFrame(medicaments)
        df = df[['code_cip', 'nom_medicament']]
        df.columns = ['Code CIP', 'Nom du médicament']
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.info(f"💡 {len(medicaments)} médicaments affichés. Utilisez la recherche ci-dessus pour trouver un médicament spécifique.")