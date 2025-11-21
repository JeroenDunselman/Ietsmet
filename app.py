import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Tartan Designer", layout="wide")
st.title("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Design Your Own Tartan")

colors = {
    "Black (K)": "#000000", "Red (R)": "#C00000", "Green (G)": "#006000",
    "Blue (B)": "#000080", "Yellow (Y)": "#FFC000", "White (W)": "#FFFFFF",
    "Purple (P)": "#800080", "Orange (O)": "#FF8000", "Grey (A)": "#808080",
    "Gold": "#D4AF37"
}

st.sidebar.header("Threadcount bouwen")
threadcount = st.sidebar.text_area("Threadcount", "R8 G24 B8 K32 Y4", height=100)

symmetry = st.sidebar.selectbox("Symmetry", ["None", "Horizontal", "Vertical", "Both", "Rotational 180°"])
sett_size = st.sidebar.slider("Sett grootte (cm)", 5, 50, 20)

def parse_threadcount(tc):
    parts = tc.upper().split()
    seq = []
    for p in parts:
        if p[0] in "KRGBYWPOA" and p[1:].isdigit():
            seq.extend([p[0]] * int(p[1:]))
    return seq

seq = parse_threadcount(threadcount)
if symmetry == "Horizontal": seq = seq + seq[::-1]
elif symmetry == "Vertical": seq = seq + seq
elif symmetry == "Both": half = seq + seq[::-1]; seq = half + half
elif symmetry == "Rotational 180°": seq = seq + seq[::-1]

fig, ax = plt.subplots(figsize=(14, 4))
x = 0
for letter in seq:
    color = colors.get([k for k, v in colors.items() if k[0] == letter][0], "#808080")
    ax.add_patch(patches.Rectangle((x, 0), 1, 1, color=color))
    x += 1

ax.set_xlim(0, x)
ax.set_ylim(0, 1)
ax.axis('off')
st.pyplot(fig)

if st.button("Download PNG"):
    fig.savefig("tartan.png", dpi=300, bbox_inches='tight')
    with open("tartan.png", "rb") as f:
        st.download_button("Download", f, "my_tartan.png")
