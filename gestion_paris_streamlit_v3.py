
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Gestion des Paris Sportifs", layout="wide")
st.title("📊 Application de Gestion des Paris Sportifs")

# --- Initialisation de la session ---
if "data" not in st.session_state:
    st.session_state.data = []

# --- Saisie utilisateur ---
st.sidebar.header("🎯 Paramètres du Pari")
date = st.sidebar.date_input("Date du pari", datetime.date.today())
mise_depart = st.sidebar.number_input("💶 Mise de départ (€)", min_value=0.0, step=0.5)
nombre_cotes = st.sidebar.number_input("🎲 Nombre de cotes", min_value=1, step=1)
cote = st.sidebar.number_input("📈 Valeur de la cote", min_value=1.0, step=0.1)
pari_gagne = st.sidebar.checkbox("✅ Pari gagné ?", value=False)

# --- Calculs ---
gain = mise_depart * cote if pari_gagne else 0.0
perte = 0.0 if pari_gagne else mise_depart
epargne = (gain * 1/20) if pari_gagne else 0.0
nouvelle_mise = (gain * 19/20) if pari_gagne else 0.0
retour_sur_epargne = nouvelle_mise if not pari_gagne else 0.0

# --- Enregistrement ---
if st.sidebar.button("💾 Enregistrer le pari"):
    st.session_state.data.append({
        "Date": date,
        "Mise": mise_depart,
        "Cote": cote,
        "Gain": gain,
        "Perte": perte,
        "Épargne": epargne,
        "Nouvelle Mise": nouvelle_mise,
        "Retrait Épargne (si perte)": retour_sur_epargne
    })
    st.success("Pari enregistré !")

# --- Affichage du tableau ---
df = pd.DataFrame(st.session_state.data)
if not df.empty:
    st.subheader("📋 Historique des Paris")
    st.dataframe(df, use_container_width=True)

    total_gain = df["Gain"].sum()
    total_perte = df["Perte"].sum()
    total_epargne = df["Épargne"].sum()

    st.subheader("📊 Résumé Financier")
    duree = st.slider("Durée (jours)", 1, 31, 7)
    benef_brut = total_epargne / duree if duree else 0.0
    prime_gerant = 0.07 * benef_brut
    taxe_dim = 0.10 * benef_brut
    profit_net = benef_brut - prime_gerant - taxe_dim

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("💰 Bénéfice brut", f"{benef_brut:.2f} €")
    col2.metric("👤 Prime gérant (7%)", f"{prime_gerant:.2f} €")
    col3.metric("🏛️ Taxe DIM (10%)", f"{taxe_dim:.2f} €")
    col4.metric("💵 Profit net TTC", f"{profit_net:.2f} €")
    col5.metric("📦 Total Épargne", f"{total_epargne:.2f} €")

    st.markdown("---")
else:
    st.info("Ajoutez un pari pour voir les résultats.")
