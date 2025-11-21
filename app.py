import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import to_rgb

st.set_page_config(page_title="Tartan – Adjacent Element Blending", layout="wide")
st.title("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Tartan Designer – Adjacent Element Blending")

# Basis kleuren
base_colors = {
    "K": "#000000", "R": "#C00000", "G": "#006000", "B": "#000080",
    "Y": "#FFC000", "W": "#FFFFFF", "P": "#800080", "O": "#FF8000",
    "A": "#808080", "Gold": "#D4AF37"
}

st.sidebar.header("Sett samenstellen")
threadcount = st.sidebar.text_area("Threadcount", "K4 R28 K4 Y4 K24 R8 G24 B24 R8 K24 Y4", height=100)

symmetry = st.sidebar.selectbox("Symmetrie", ["Horizontal (reversed sett)", "Both (pmm)", "Rotational 180°", "None"])
blend_strength = st.sidebar.slider("Adjacent element blend strength", 0.0, 1.0, 0.6, 0.05,
    help="0 = harde overgangen, 1 = maximale blending tussen aangrenzende elementen")
blend_steps = st.sidebar.slider("Aantal tussenpallets per blend", 2, 12, 6)

sett_size = st.sidebar.slider("Sett-grootte (cm)", 5, 60, 20)

# Parse tot elementen (list van tuples: (letter, count))
def parse_elements(tc):
    parts = tc.upper().split()
    elements = []
    for part in parts:
        if len(part) > 1 and part[0] in base_colors and part[1:].isdigit():
            elements.append((part[0], int(part[1:])))
    return elements

elements = parse_elements(threadcount)

# Symmetry toepassen op element-niveau
if "Horizontal" in symmetry or symmetry == "Rotational 180°":
    elements = elements + elements[::-1]
elif symmetry == "Both (pmm)":
    half = elements + elements[::-1]
    elements = half + half

# Adjacent element blending
final_seq = []
for i, (letter, count) in enumerate(elements):
    color = base_colors[letter]
    # Voeg het originele element toe
    final_seq.extend([color] * count)
    
    # Blend met het volgende element (behalve bij laatste)
    if i < len(elements) - 1 and blend_strength > 0:
        next_letter = elements[i+1][0]
        next_color = base_colors[next_letter]
        c1 = to_rgb(color)
        c2 = to_rgb(next_color)
        for step in range(1, blend_steps + 1):
            t = step / (blend_steps + 1) * blend_strength
            blended = tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))
            hex_blended = "#{:02x}{:02x}{:02x}".format(*blended)
            final_seq.append(hex_blended)

# Tekening
total = len(final_seq)
width = max(sett_size, total / 40)
fig, ax = plt.subplots(figsize=(width * 1.4, 9))

x = 0
for col in final_seq:
    ax.add_patch(patches.Rectangle((x, 0), 1, 1, color=col))
    x += 1

ax.set_xlim(0, total)
ax.set_ylim(0, 1)
ax.set_aspect('auto')
ax.axis('off')
st.pyplot(fig)

if st.button("Download als PNG"):
    fig.savefig("blended_tartan.png", dpi=300, bbox_inches="tight", facecolor="#111111")
    with open("blended_tartan.png", "rb") as f:
        st.download_button("Download PNG", f, "blended_tartan.png", "image/png")

st.caption(f"Sett: {sett_size} cm | Symmetrie: {symmetry} | Blend strength: {blend_strength:.2f} | Tussenpallets: {blend_steps} | Threads: {total}")
