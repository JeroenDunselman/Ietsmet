# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# Kleuren map
COLORS = {
    "R": (200, 16, 46),    # Classic red
    "G": (0, 128, 27),     # Dark green
    "B": (0, 0, 139),      # Navy blue
    "K": (35, 35, 35),     # Black
    "Y": (255, 215, 0),    # Gold
    "W": (255, 255, 255),  # White
    "O": (255, 140, 0),    # Orange
    "P": (128, 0, 128),    # Purple
    "A": (180, 180, 180),  # Grey / Azure
    "N": (0, 51, 102),     # Dark blue (Navy)
    "T": (0, 128, 128),    # Teal
}

def parse_threadcount(tc: str):
    parts = tc.upper().strip().split()
    pattern = []
    for p in parts:
        if not p:
            continue
        color = p[0]
        count = int(p[1:])
        if color not in COLORS:
            st.error(f"Onbekende kleur: {color}")
            return None
        pattern.append((color, count))
    return pattern

def mirror_pattern(pattern):
    forward = [count for _, count in pattern]
    backward = forward[::-1][1:]          # zonder de laatste van de originele (die wordt dubbel)
    mirrored_counts = forward + backward
    colors = [col for col, _ in pattern]
    mirrored_colors = colors + colors[::-1][1:]
    return mirrored_counts, mirrored_colors

def create_tartan(pattern, size=800, thread_width=4):
    mirrored_counts, mirrored_colors = mirror_pattern(pattern)
    
    img = np.zeros((size, size, 3), dtype=np.uint8)
    
    # Verticaal (warp)
    pos = 0
    for count, col in zip(mirrored_counts, mirrored_colors):
        threads = count * thread_width
        if pos + threads > size:
            threads = size - pos
        img[:, pos:pos + threads] = COLORS[col]
        pos += threads
        if pos >= size:
            break
    
    # Horizontaal (weft)
    pos = 0
    for count, col in zip(mirrored_counts, mirrored_colors):
        threads = count * thread_width
        if pos + threads > size:
            threads = size - pos
        img[pos:pos + threads, :] = COLORS[col]
        pos += threads
        if pos >= size:
            break
    
    # Overcheck door simpele add (met clip op 255)
    result = np.minimum(img.astype(np.uint16) + img.astype(np.uint16), 255).astype(np.uint8)
    return result

# ────────────────────────── Streamlit UI ──────────────────────────

st.set_page_config(page_title="Tartan Mirror", layout="centered")
st.title("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Tartan Mirror")

st.markdown("""
Voer een threadcount in (bijv. `R12 G32 B12 K48 Y6`) en zie direct een echte, correct gespiegelde Schotse ruit.
""")

example = st.checkbox("Voorbeeld laden (MacDonald of the Isles)", value=True)

if example:
    default_tc = "R18 K12 B6"          # <-- Hier zat het probleem eerder!
else:
    default_tc = ""

tc_input = st.text_input(
    "Threadcount (bijv. R12 G32 B12 K48 Y6)",
    value=default_tc,
    help="Formaat: Kleurletter + aantal, spaties ertussen. Beschikbare kleuren: " + ", ".join(COLORS.keys())
)

if tc_input.strip():
    pattern = parse_threadcount(tc_input)
    if pattern:
        tartan_img = create_tartan(pattern, size=800, thread_width=4)
        
        st.subheader("Jouw tartan")
        st.image(tartan_img, use_column_width=True)
        
        # Download knop
        buf = BytesIO()
        plt.imsave(buf, tartan_img, format="png")
        buf.seek(0)
        st.download_button(
            label="Download als PNG (800×800)",
            data=buf.getvalue(),
            file_name=f"tartan_{tc_input.strip().replace(' ', '_')}.png",
            mime="image/png"
        )
        
        # Gespiegelde threadcount tonen
        mirrored_counts, mirrored_colors = mirror_pattern(pattern)
        seq = " ".join(f"{col}{cnt}" for col, cnt in zip(mirrored_colors, mirrored_counts))
        st.caption(f"Gespiegelde threadcount: `{seq}`")
