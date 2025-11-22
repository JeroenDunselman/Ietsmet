# app.py
# Streamlit app voor Tartan zoekmachine + visualisatie
# Run met: streamlit run app.py

import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Bron: officiële tartan register data (Scottish Register of Tartans API of CSV)
# Voor dit voorbeeld gebruiken we een kleine ingebouwde lijst + fallback naar API
TARTANS_CSV_URL = "https://www.tartanregister.gov.uk/csvExport.ashx"

@st.cache_data
# Vervang de load_tartans() functie tijdelijk door puur fallback:
@st.cache_data
def load_tartans():
    data = { ... }  # Je bestaande fallback data
    return pd.DataFrame(data)
df_tartans = load_tartans()

st.set_page_config(page_title="Tartan Finder", layout="centered")
st.title("Tartan Zoeken & Visualiseren")

# Zoekveld
search = st.text_input("Zoek tartan naam (begint met…)", "", placeholder="bijv. mac, stew, black")

if search:
    search_clean = search.strip().title()
    # Filter op beginswith
    matches = df_tartans[df_tartans["TartanName"].str.startswith(search_clean)]
    
    if not matches.empty:
        # Automatisch eerste resultaat selecteren
        default_idx = 0
        selected_name = st.selectbox(
            "Gevonden tartans",
            matches["TartanName"],
            index=default_idx,
            key="tartan_select"
        )
    else:
        st.info("Geen tartan gevonden die begint met deze naam.")
        selected_name = None
else:
    selected_name = None
    matches = pd.DataFrame()

# Geselecteerde tartan tonen
if selected_name:
    row = df_tartans[df_tartans["TartanName"] == selected_name].iloc[0]
    
    # Beschrijving
    description = st.text_area(
        "Tartan definitie / beschrijving",
        value=row.get("TartanDescription", "Geen beschrijving beschikbaar."),
        height=120
    )
    
    # Threadcount = row["Threadcount"]
    
    # Simpele visualisatie van threadcount
    def draw_tartan(threadcount):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis("off")
        
        colors = {
            "R": "#C00000", "G": "#008000", "B": "#000080", "K": "#000000",
            "W": "#FFFFFF", "Y": "#FFFF00", "O": "#FFA500", "P": "#800080",
            "A": "#808080"  # Azure/grijs
        }
        
        x = 0
        for part in threadcount.replace(" ", "").split():
            if len(part) < 2:
                continue
            color_code = part[0]
            try:
                width = int(part[1:])
            except:
                width = 4
            color = colors.get(color_code.upper(), "#808080")
            rect = patches.Rectangle((x, 0), width*2, 100, linewidth=0, facecolor=color)
            ax.add_patch(rect)
            x += width*2
            
            # Mirror voor symmetrie
            if x > 0:
                rect = patches.Rectangle((x, 0), width*2, 100, linewidth=0, facecolor=color)
                ax.add_patch(rect)
                x += width*2
        
        plt.tight_layout()
        return fig
    
    st.pyplot(draw_tartan(Threadcount))
    
    # Optioneel PNG download
    buf = BytesIO()
    draw_tartan(Threadcount).savefig(buf, format="png", bbox_inches="tight", dpi=150)
    buf.seek(0)
    st.download_button(
        label="Download tartan als PNG",
        data=buf,
        file_name=f"{selected_name.replace(' ', '_')}.png",
        mime="image/png"
    )

