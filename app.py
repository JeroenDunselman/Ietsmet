import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Tartan Designer Pro", layout="wide")
st.title("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Tartan Designer – Shadow & Tonal Edition")

# === Professionele kleurdefinities met 5 tinten (dark → light → dark) ===
color_tones = {
    "K": ["#000000", "#111111", "#222222", "#111111", "#000000"],  # Black
    "R": ["#400000", "#800000", "#C00000", "#800000", "#400000"],  # Red
    "G": ["#003000", "#006000", "#008000", "#006000", "#003000"],  # Green
    "B": ["#000040", "#000080", "#0000C0", "#000080", "#000040"],  # Blue
    "Y": ["#806000", "#C0A000", "#FFC000", "#C0A000", "#806000"],  # Yellow
    "W": ["#DDDDDD", "#EEEEEE", "#FFFFFF", "#EEEEEE", "#DDDDDD"],  # White
    "P": ["#400040", "#800080", "#C000C0", "#800080", "#400040"],  # Purple
    "O": ["#803000", "#C06000", "#FF8000", "#C06000", "#803000"],  # Orange
    "A": ["#404040", "#606060", "#808080", "#606060", "#404040"],  # Grey
}

# Sidebar – prof-termen
st.sidebar.header("Sett samenstellen")
threadcount = st.sidebar.text_area(
    "Threadcount", 
    "R8 G24 B8 K32 Y4 R8 G24 B8 K32 Y4",
    help="Bijv. R8 G24 B8 K32 Y4 (R=rood, G=groen, etc.)"
)

symmetry = st.sidebar.selectbox(
    "Symmetrie",
    ["None", "Horizontal (reversed sett)", "Both (pmm)", "Rotational 180°"],
    help="Horizontal = klassieke tartan met pivot in het midden"
)

shadow_mode = st.sidebar.checkbox("Shadow tartan mode (tonal blend)", value=False,
    help="Vervangt elke kleur door 5 tinten (dark → base → light → base → dark)"
)

sett_size = st.sidebar.slider("Sett-grootte (cm)", 5, 60, 20)

# === Parse threadcount ===
def parse_tc(tc):
    parts = tc.upper().split()
    seq = []
    for part in parts:
        if len(part) > 1 and part[0] in color_tones and part[1:].isdigit():
            seq.extend([part[0]] * int(part[1:]))
    return seq

seq = parse_tc(threadcount)

# === Symmetry toepassen ===
if "Horizontal" in symmetry or symmetry == "Rotational 180°":
    seq = seq + seq[::-1]
elif symmetry == "Both (pmm)":
    half = seq + seq[::-1]
    seq = half + half

# === Shadow mode: elke kleur → 5 tinten ===
if shadow_mode:
    toned_seq = []
    for letter in seq:
        tones = color_tones[letter]
        toned_seq.extend([tones[0], tones[1], tones[2], tones[3], tones[4]])
    seq = toned_seq
else:
    toned_seq = seq  # voor tekening

# === Tekening ===
fig, ax = plt.subplots(figsize=(18, 5))
x = 0
for letter in toned_seq:
    if shadow_mode:
        col = letter  # letter is al een hex-kleur
    else:
        col = color_tones[letter][2]  # middelste (basis) tint
    ax.add_patch(patches.Rectangle((x, 0), 1, 1, color=col))
    x += 1

ax.set_xlim(0, x)
ax.set_ylim(0, 1)
ax.axis('off')
ax.set_aspect('equal')
st.pyplot(fig)

# === Download ===
if st.button("Download als PNG (kilt-ready)"):
    fig.savefig("shadow_tartan.png", dpi=300, bbox_inches="tight", facecolor="#111111")
    with open("shadow_tartan.png", "rb") as f:
        st.download_button("Download PNG", f, "shadow_tartan.png", "image/png")

st.caption(f"Sett: {sett_size} cm | Symmetrie: {symmetry} | Shadow mode: {'Aan' if shadow_mode else 'Uit'} | Threads: {len(toned_seq)}")
