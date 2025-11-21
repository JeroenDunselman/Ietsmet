# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# Kleuren map (je kunt dit makkelijk uitbreiden)
COLORS = {
    "R": (200, 16, 46),    # Classic red
    "G": (0, 128,27),      # Dark green
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
    """Converteert bijv. 'R12 G32 B12 K48 Y6' naar lijst van (kleurletter, count)"""
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
    """Maakt de klassieke tartan spiegeling: vooruit + achteruit - laatste kleur"""
    forward = [count for color, count in pattern]
    backward = forward[::-1][1:]  # zonder de eerste van de omgekeerde (die is dubbel)
    mirrored = forward + backward
    colors = [color for color, count in pattern]
    mirrored_colors = colors + colors[::-1][1:]
    return mirrored, mirrored_colors

def create_tartan(pattern, size=800, thread_width=4):
    forward_counts = [c for col, c in pattern]
    total_threads = sum(forward_counts) * 2 - forward_counts[-1]  # door spiegeling
    
    img = np.zeros((size, size, 3), dtype=np.uint8)
    
    # Verticaal (warp)
    pos = 0
    mirrored_counts, mirrored_colors = mirror_pattern(pattern)
    for count, color_key in zip(mirrored_counts, mirrored_colors):
        threads = count * thread_width
        img[:, pos:pos+threads] = COLORS[color_key]
        pos += threads
        if pos >= size:
            break
    
    # Horizontaal (weft) - zelfde patroon maar getransponeerd
    img2 = np.zeros_like(img)
    pos = 0
    for count, color_key in zip(mirrored_counts, mirrored_colors):
        threads = count * thread_width
        img2[pos:pos+threads, :] = COLORS[color_key]
        pos += threads
        if pos >= size:
            break
    
    # Overlay: waar beide kleuren samenkomen krijg je een mengkleur (simpele add)
    # Dit geeft het echte tartan "overcheck" effect
    result = np.minimum(img + img2, 255).astype(np.uint8)
    return result

# ────────────────────────── Streamlit app ──────────────────────────

st.set_page_config(page_title="Tartan Mirror", layout="centered")
st.title("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Tartan Mirror")

st.markdown("""
Voer een threadcount in (bijvoorbeeld `R12 G32 B12 K48 Y6`) en zie direct een echte, correct gespiegelde tartan.
De app spiegelt zowel warp als weft precies zoals het hoort.
""")

example = st.checkbox("Voorbeeld laden (MacDonald of the Isles)", value=True)

if example:
    default_tc = "R18 K12 B6
