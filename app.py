import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random  

st.set_page_config(page_title="Tartan Designer", layout="wide")
st.title("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Design Your Own Tartan")

# Kleurenpalet (letter → hex)
color_map = {
    "K": "#000000",  # Black
    "R": "#C00000",  # Red
    "G": "#006000",  # Green
    "B": "#000080",  # Blue
    "Y": "#FFC000",  # Yellow
    "W": "#FFFFFF",  # White
    "P": "#800080",  # Purple
    "O": "#FF8000",  # Orange
    "A": "#808080",  # Grey
    "Gold": "#D4AF37"
}

st.sidebar.header("Threadcount bouwen")
threadcount = st.sidebar.text_area("Threadcount", "R8 G24 B8 K32 Y4", height=100)

if st.sidebar.button("🎲 Random tartan"):
    letters = "KRGBYWPOA"
    parts = []
    for _ in range(random.randint(5, 12)):
        letter = random.choice(letters)
        count = random.randint(2, 40)
        parts.append(f"{letter}{count}")
    new_threadcount = " ".join(parts)
    st.sidebar.code(new_threadcount)  # toont de nieuwe threadcount
    threadcount = new_threadcount  # update het invoerveld

symmetry = st.sidebar.selectbox("Symmetry", ["None", "Horizontal", "Vertical", "Both", "Rotational 180°"])
sett_size = st.sidebar.slider("Sett grootte (cm)", 5, 50, 20)

# Parse threadcount
def parse_threadcount(tc):
    parts = tc.upper().split()
    seq = []
    for part in parts:
        if len(part) > 1 and part[0] in color_map and part[1:].isdigit():
            seq.extend([part[0]] * int(part[1:]))
    return seq

seq = parse_threadcount(threadcount)

# Symmetry toepassen
if symmetry == "Horizontal":
    seq = seq + seq[::-1]
elif symmetry == "Vertical":
    seq = seq + seq
elif symmetry == "Both":
    half = seq + seq[::-1]
    seq = half + half
elif symmetry == "Rotational 180°":
    seq = seq + seq[::-1]

# Tekening
fig, ax = plt.subplots(figsize=(14, 4))
x = 0
for letter in seq:
    col = color_map.get(letter, "#808080")
    ax.add_patch(patches.Rectangle((x, 0), 1, 1, color=col))
    x += 1

ax.set_xlim(0, x)
ax.set_ylim(0, 1)
ax.axis('off')
st.pyplot(fig)
if st.checkbox("Toon schaal (met poppetje van 1,80 m)"):
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    scale = sett_size / len(seq) * 100  # pixels per cm
    person_height_px = 180 * scale
    
    # Tartan als achtergrond
    x = 0
    for letter in seq:
        ax2.add_patch(patches.Rectangle((x, 0), 1, 100, color=color_map.get(letter, "#808080")))
        x += 1
    
    # Poppetje
    ax2.add_patch(patches.Rectangle((50, 0), 20, person_height_px, color="#FFDBA8", alpha=0.8))
    ax2.text(60, person_height_px + 10, "jij (1,80 m)", ha="center", fontsize=12)
    
    ax2.set_xlim(0, len(seq))
    ax2.set_ylim(0, max(100, person_height_px + 50))
    ax2.axis("off")
    st.pyplot(fig2)
if st.button("Download als PNG"):
    fig.savefig("my_tartan.png", dpi=300, bbox_inches='tight')
    with open("my_tartan.png", "rb") as f:
        st.download_button("Download PNG", f, "my_tartan.png", "image/png")

st.caption(f"Sett: {sett_size} cm | Symmetry: {symmetry} | Threads: {len(seq)}")



