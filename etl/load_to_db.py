"""
Script pour charger les donnees agregees dans PostgreSQL (Supabase)
"""

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# URL de connexion PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("DATABASE_URL non trouvee dans le fichier .env")

print("=" * 60)
print("CHARGEMENT DES DONNEES DANS POSTGRESQL")
print("=" * 60)

# Creer la connexion
engine = create_engine(DATABASE_URL)

# Test de connexion
print("\n1. Test de connexion...")
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"   ✅ Connexion reussie !")
        print(f"   PostgreSQL version: {version[:50]}...")
except Exception as e:
    print(f"   ❌ Erreur de connexion: {e}")
    exit(1)

# ============================================================
# CHARGER LES REGIONS
# ============================================================
print("\n2. Chargement des regions...")

# Charger le CSV
agg_region = pd.read_csv('../data/processed/agregation_regions_2023.csv')

# Preparer les donnees regions (sans doublons)
df_regions = agg_region[['code_region', 'nom_region']].drop_duplicates()

print(f"   {len(df_regions)} regions a charger")

# Charger dans PostgreSQL
df_regions.to_sql('regions', engine, if_exists='append', index=False)

print("   ✅ Regions chargees")

# ============================================================
# CHARGER LES MEDICAMENTS
# ============================================================
print("\n3. Chargement des medicaments...")

# Charger le CSV
agg_medic = pd.read_csv('../data/processed/agregation_medicaments_2023.csv')

# Preparer les donnees medicaments
df_medicaments = agg_medic[['code_cip', 'nom_medicament']].drop_duplicates()

print(f"   {len(df_medicaments)} medicaments a charger")

# Charger dans PostgreSQL
df_medicaments.to_sql('medicaments', engine, if_exists='append', index=False)

print("   ✅ Medicaments charges")

# ============================================================
# CHARGER LES CLASSES THERAPEUTIQUES
# ============================================================
print("\n4. Chargement des classes therapeutiques...")

# Charger le CSV
agg_atc = pd.read_csv('../data/processed/agregation_classes_2023.csv')

# Preparer les donnees
df_classes = agg_atc[['code_atc', 'classe_therapeutique']].drop_duplicates()
df_classes.columns = ['code_atc', 'nom_classe']

print(f"   {len(df_classes)} classes a charger")

# Charger dans PostgreSQL
df_classes.to_sql('classes_therapeutiques', engine, if_exists='append', index=False)

print("   ✅ Classes therapeutiques chargees")

# ============================================================
# CHARGER LA CONSOMMATION PAR REGION
# ============================================================
print("\n5. Chargement de la consommation par region...")

# Recuperer les ID des regions depuis la DB
with engine.connect() as conn:
    regions_db = pd.read_sql("SELECT id, code_region FROM regions", conn)

# Merge pour obtenir les region_id
consommation_data = agg_region.merge(regions_db, on='code_region')

# Preparer le DataFrame pour la table consommation
# On utilise medicament_id = NULL pour indiquer que c'est un agrege total par region
df_consommation = pd.DataFrame({
    'region_id': consommation_data['id'],
    'medicament_id': None,  # Pas de medicament specifique (agrege total)
    'annee': 2023,
    'total_boites': consommation_data['total_boites'],
    'total_remb': consommation_data['total_remb']
})

print(f"   {len(df_consommation)} lignes de consommation a charger")

# Charger dans PostgreSQL
df_consommation.to_sql('consommation', engine, if_exists='append', index=False)

print("   ✅ Consommation chargee")

# ============================================================
# VERIFICATION
# ============================================================
print("\n6. Verification des donnees chargees...")

with engine.connect() as conn:
    # Compter les lignes
    count_regions = conn.execute(text("SELECT COUNT(*) FROM regions")).fetchone()[0]
    count_medic = conn.execute(text("SELECT COUNT(*) FROM medicaments")).fetchone()[0]
    count_classes = conn.execute(text("SELECT COUNT(*) FROM classes_therapeutiques")).fetchone()[0]
    count_conso = conn.execute(text("SELECT COUNT(*) FROM consommation")).fetchone()[0]
    
    print(f"\n   📊 Regions: {count_regions}")
    print(f"   📊 Medicaments: {count_medic}")
    print(f"   📊 Classes therapeutiques: {count_classes}")
    print(f"   📊 Consommation: {count_conso}")

print("\n" + "=" * 60)
print("✅ CHARGEMENT TERMINE AVEC SUCCES !")
print("=" * 60)

# ============================================================
# REQUETES DE TEST
# ============================================================
print("\n7. Test de quelques requetes...")

with engine.connect() as conn:
    # Top 3 regions par montant rembourse
    query = """
    SELECT r.nom_region, c.total_boites, c.total_remb
    FROM consommation c
    JOIN regions r ON c.region_id = r.id
    WHERE c.annee = 2023
    ORDER BY c.total_remb DESC
    LIMIT 3
    """
    
    result = pd.read_sql(query, conn)
    print("\n   🏆 TOP 3 REGIONS (2023) :")
    for idx, row in result.iterrows():
        print(f"      {row['nom_region']:30s} {int(row['total_boites']):15,} boites  {float(row['total_remb']):15,.2f} EUR".replace(',', ' '))

print("\n✅ Tout fonctionne correctement !")