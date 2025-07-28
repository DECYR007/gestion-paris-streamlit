
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gestion Paris Sportifs", layout="wide")

st.title("📊 Gestion des Paris Sportifs")

st.sidebar.header("🔁 Paramètres")
date = st.sidebar.date_input("📅 Date", datetime.today())
mise_depart = st.sidebar.number_input("💸 Mise de départ", min_value=0.0, step=1.0)

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Date", "Mise départ", "Mise", "Cote", "Gain", "Perte",
        "Épargne", "Nouvelle mise", "Retenu sur épargne", "Statut (G/P)"
    ])

st.markdown("## 📥 Saisir un nouveau pari")
col1, col2, col3, col4 = st.columns(4)
with col1:
    mise = st.number_input("Mise", min_value=0.0, step=1.0)
with col2:
    cote = st.number_input("Cote", min_value=0.1, step=0.1)
with col3:
    statut = st.selectbox("Statut du pari", ["Gagné", "Perdu"])
with col4:
    bouton_valider = st.button("✅ Valider le pari")

if bouton_valider:
    if statut == "Gagné":
        gain = mise * cote
        perte = 0
        nouvelle_mise = gain * 19 / 20
        epargne = gain - nouvelle_mise
        retenu = 0
    else:
        gain = 0
        perte = mise
        epargne = 0
        nouvelle_mise = mise_depart if epargne == 0 else perte
        retenu = perte if epargne >= perte else 0

    nouvelle_ligne = pd.DataFrame([{
        "Date": date.strftime("%d/%m/%Y"),
        "Mise départ": mise_depart,
        "Mise": mise,
        "Cote": cote,
        "Gain": gain,
        "Perte": perte,
        "Épargne": epargne,
        "Nouvelle mise": nouvelle_mise,
        "Retenu sur épargne": retenu,
        "Statut (G/P)": statut
    }])

    st.session_state.data = pd.concat([st.session_state.data, nouvelle_ligne], ignore_index=True)
    st.success("Pari ajouté avec succès ✅")

st.markdown("## 📊 Tableau de suivi")
st.dataframe(st.session_state.data, use_container_width=True)

if not st.session_state.data.empty:
    st.markdown("## 📈 Graphique de progression des gains")
    chart_data = st.session_state.data.copy()
    chart_data["Date"] = pd.to_datetime(chart_data["Date"], format="%d/%m/%Y")
    chart_data = chart_data.sort_values("Date")
    st.line_chart(chart_data[["Date", "Gain"]].set_index("Date"))
