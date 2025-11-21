import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Tartan Weaving Simulator", layout="wide")
st.title("🧵 Tartan Weaving Simulator – Echte stofsimulatie")

color_map = {
    "K": "#000000", "R": "#C00000", "G": "#006000", "B": "#000080",
    "Y": "#FFC000", "W": "#FFFFFF", "P": "#800080", "O": "#FF8000",
    "A": "#808080", "Gold": "#D4AF37"
}

st.sidebar.header("Warp (staand)")
warp_tc = st.sidebar.text_area("Warp threadcount", "K4 R28 K4 Y4 K24 R8 G24 B24 R8 K24 Y4", height=100)

st.sidebar.header("Weft (liggend)")
weft_tc = st.sidebar.text_area("Weft threadcount", "K4 R28 K4 Y4 K24 R8 G24 B24 R8 K24 Y4", height=100)

sett_size = st.sidebar.slider("Sett-grootte (cm)", 5, 60, 20)
dpi = st.sidebar.slider("Resolutie (DPI)", 100, 600, 300)

# === ALLEEN HIER WORDT ER IETS BEREKEND (na de sliders) ===
def tc_to_colors(tc):
    parts = tc.upper().split()
    colors = []
    for part in parts:
        if len(part) > 1 and part[0] in color_map and part[1:].isdigit():
            colors.extend([color_map[part[0]]] * int(part[1:]))
    return colors

warp_colors = tc_to_colors(warp_tc)
weft_colors = tc_to_colors(weft_tc)

if not warp_colors or not weft_colors:
    st.error("Vul beide threadcounts in!")
    st.stop()

# Schaal pas hier, nádat sliders bestaan
scale = sett_size * dpi // 100
warp_grid = np.repeat(warp_colors, scale)
weft_grid = np.repeat(weft_colors, scale)

height, width = len(weft_grid), len(warp_grid)
fabric = np.zeros((height, width, 3))

for y in range(height):
    for x in range(width):
        if (x + y) % 2 == 0:
            fabric[y, x] = plt.cm.colors.to_rgb(warp_grid[x])
        else:
            fabric[y, x] = plt.cm.colors.to_rgb(weft_grid[y])

fig, ax = plt.subplots(figsize=(width / dpi * 1.5, height / dpi * 1.5), dpi=dpi)
ax.imshow(fabric)
ax.axis('off')
st.pyplot(fig)

if st.button("Download als PNG"):
    fig.savefig("woven_tartan.png", dpi=dpi, bbox_inches='tight')
    with open("woven_tartan.png", "rb") as f:
        st.download_button("Download PNG", f, "woven_tartan.png", "image/png")
