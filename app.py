import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

st.set_page_config(page_title="Tartan Designer", layout="wide")
st.title("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Tartan Designer")

# Kleuren
color_map = {
    "K": "#000000", "R": "#C00000", "G": "#006000", "B": "#000080",
    "Y": "#FFC000", "W": "#FFFFFF", "P": "#800080", "O": "#FF8000",
    "A": "#808080", "Gold": "#D4AF37"
}

# Sidebar
st.sidebar.header("Threadcount")
default = "R8 G24 B8 K32 Y4 R8"
threadcount = st.sidebar.text_area("Threadcount", default, height=100)

if st.sidebar.button("🎲 Random tartan"):
    letters = "KRGBYWPOA"
    parts = [random.choice(letters) + str(random.randint(2, 36)) for _ in range(random.randint(5, 11))]
    threadcount = " ".join(parts)
    st.sidebar.code(threadcount)

symmetry = st.sidebar.selectbox("Symmetry", ["None", "Horizontal", "Vertical", "Both", "Rotational 180°"])
sett_cm = st.sidebar.slider("Sett grootte (cm)", 5, 60, 20)

# Parse
def parse_tc(tc):
    seq = []
    for part in tc.upper().split():
        if len(part) > 1 and part[0] in color_map and part[1:].isdigit():
            seq.extend([part[0]] * int(part[1:]))
    return seq

seq = parse_tc(threadcount)

# Symmetry
if symmetry == "Horizontal" or symmetry == "Rotational 180°":
    seq = seq + seq[::-1]
elif symmetry == "Vertical":
    seq = seq + seq
elif symmetry == "Both":
    half = seq + seq[::-1]
    seq = half + half

# Plot
fig, ax = plt.subplots(figsize=(16, 4))
x = 0
for letter in seq:
    ax.add_patch(patches.Rectangle((x, 0), 1, 1, color=color_map.get(letter, "#808080")))
    x += 1

ax.set_xlim(0, x)
ax.set_ylim(0, 1)
ax.axis("off")
ax.set_aspect("equal")
st.pyplot(fig)

# Download
if st.button("💾 Download als PNG"):
    fig.savefig("tartan.png", dpi=300, bbox_inches="tight", facecolor="#111")
    with open("tartan.png", "rb") as f:
        st.download_button("Download PNG", f, "tartan.png", "image/png")

st.caption(f"Sett: {sett_cm} cm | Symmetry: {symmetry} | Threads: {len(seq)}")
