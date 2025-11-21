import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

st.set_page_config(page_title="Tartan Designer", layout="wide")
st.title("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Design Your Own Tartan")

# Kleurenpalet (klassieke tartan-kleuren + hex)
colors = {
    "Black (K)": "#000000",
    "Red (R)": "#C00000",
    "Green (G)": "#006000",
    "Blue (B)": "#000080",
    "Yellow (Y)": "#FFC000",
    "White (W)": "#FFFFFF",
    "Purple (P)": "#800080",
    "Orange (O)": "#FF8000",
    "Grey (A)": "#808080",
    "Gold (Gold)": "#D4AF37"
}

# Sidebar – bouw je threadcount
st.sidebar.header("Threadcount bouwen")
threadcount = st.sidebar.text_area(
    "Threadcount (bijv. R8 G24 B8 K32 Y4)", 
    value="R8 G24 B8 K32 Y4"
)

# Symmetry opties
symmetry = st.sidebar.selectbox("Symmetry", ["None", "Horizontal", "Vertical", "Both", "Rotational 180°"])
sett_size = st.sidebar.slider("Sett grootte (cm)", 5, 50, 20)

# Parse threadcount
def parse_threadcount(tc):
    parts = tc.upper().split()
    sequence = []
    for part in parts:
        if part[0] in "KRGBYWPOA" and part[1:].isdigit():
            sequence.extend([part[0]] * int(part[1:]))
    return sequence

sequence = parse_threadcount(threadcount)

# Symmetry toepassen
def apply_symmetry(seq, mode):
    if mode == "Horizontal":
        return seq + seq[::-1]
    elif mode == "Vertical":
        return seq + seq
    elif mode == "Both":
        half = seq + seq[::-1]
        return half + half
    elif mode == "Rotational 180°":
        return seq + seq[::-1]
    return seq

final_seq = apply_symmetry(sequence, symmetry)

# Kleurenmap
color_map = {k.split()[0]: v for k, v in colors.items()}

# Tekenen
fig, ax = plt.subplots(figsize=(12, 6))
x = 0
for letter in final_seq:
    color = color_map.get(letter, "#808080")
    ax.add_patch(patches.Rectangle((x, 0), 1, 1, color=color))
    x += 1

ax.set_xlim(0, len(final_seq))
ax.set_ylim(0, 1)
ax.axis('off')
ax.set_aspect('equal')
st.pyplot(fig)

# Export
if st.button("Download als PNG (kilt-ready)"):
    fig.savefig("my_tartan.png", dpi=300, bbox_inches='tight')
    with open("my_tartan.png", "rb") as f:
        st.download_button("Download PNG", f, "my_tartan.png")

st.caption(f"Sett: {sett_size} cm | Symmetry: {symmetry} | Threads: {len(final_seq)}")