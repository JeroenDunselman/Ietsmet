# app.py  ← nieuwe versie, klaar voor nieuwe release

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO

CSV_URL = "https://www.tartanregister.gov.uk/csvExport.ashx"

@st.cache_data(ttl=3600)  # 1 uur cache, voorkomt timeout
def load_tartans():
    try:
        df = pd.read_csv(CSV_URL, encoding="utf-8")
        df = df[['TartanName', 'Threadcount', 'TartanDescription']].dropna(subset=['TartanName', 'Threadcount'])
        df['TartanName'] = df['TartanName'].str.strip().str.title()
        return df
    except:
        st.error("Kon officiële tartan-database niet laden – fallback actief.")
        fallback = pd.DataFrame({
            "TartanName": ["Black Watch", "Royal Stewart", "Campbell"],
            "Threadcount": ["K8 R4 K24 B24 K24 G32", "R8 B4 R4 W4 R4 Y4 R32", "B4 G32 K4 B32 G32 K32"],
            "TartanDescription": ["Regimental tartan", "Famous Stewart tartan", "Clan Campbell"]
        })
        return fallback

df = load_tartans()

st.set_page_config(page_title="Tartan Finder", layout="centered")
st.title("Tartan Finder – Officiële Schotse Register")

search = st.text_input("Begin met typen…", "", placeholder="bijv. mac, stew, black, dress")

if search:
    search = search.strip().title()
    results = df[df["TartanName"].str.startswith(search, na=False)]
    
    if not results.empty:
        selected = st.selectbox("Gevonden tartans", results["TartanName"], index=0)
    else:
        st.info("Geen tartan gevonden die hiermee begint")
        selected = None
else:
    selected = None

if selected:
    row = df[df["TartanName"] == selected].iloc[0]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(selected)
        st.write(row["TartanDescription"])
    
    with col2:
        st.subheader("Threadcount")
        st.code(row["Threadcount"], language=None)

    # ——— Visualisatie met juiste breedtes + hover zoom ———
    threadcount = row["Threadcount"].replace(" ", "")

    colors = {
        "R": "#C00000", "G": "#008000", "B": "#000080", "K": "#000000",
        "W": "#FFFFFF", "Y": "#FFFF00", "O": "#FF8000", "P": "#800080",
        "A": "#964B00", "L": "#ADD8E6", "N": "#808080"
    }

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 300)
    ax.set_ylim(0, 150)
    ax.axis("off")

    x = 0
    parts = []
    for part in threadcount.split():
        if len_part = len(part)
        if len_part < 2: continue
        color_code = part[0].upper()
        try:
            width = int(part[1
