import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Tartan Designer", layout="wide")
st.title("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Tartan Designer – Shadow & Tonal Edition")

# === Kleuren + 5 tinten ===
color_tones = {
    "K": ["#000000", "#111111", "#222222", "#111111", "#000000"],
    "R": ["#400000", "#800000", "#C00000", "#800000", "#400000"],
    "G": ["#003000", "#006000", "#008000", "#006000", "#003000"],
    "B": ["#000040", "#000080", "#0000C0", "#000080", "#000040"],
    "Y": ["#806000", "#C0A000", "#FFC000", "#C0A000", "#806000"],
    "W": ["#DDDDDD", "#EEEEEE", "#FFFFFF", "#EEEEEE", "#DDDDDD"],
    "P": ["#400040", "#800080", "#C000C0", "#800080", "#400040"],
    "O": ["#803000", "#C06000", "#FF8000", "#C06000", "#803000"],
    "A": ["#404040", "#606060", "#808080", "#606060", "#404040"],
}

st.sidebar.header("Sett samenstellen")
threadcount = st.sidebar.text_area("Threadcount", "R8 G24 B8 K32 Y4 R8 G24 B8 K32 Y4", height=100)

symmetry = st.sidebar.selectbox("Symmetrie", ["None", "Horizontal (reversed sett)", "Both (pmm)", "Rotational 180°"])
shadow_mode = st.sidebar.checkbox("Shadow tartan mode (tonal blend)", value=False)
sett_size = st.sidebar.slider("Sett-grootte (cm)", 5, 60, 20)

# Parse
def parse_tc(tc):
    parts = tc.upper().split()
    seq = []
    for part in parts:
        if len(part) > 1 and part[0] in color_tones and part[1:].isdigit():
            seq.extend([part[0]] * int(part[1:]))
    return seq

seq = parse_tc(threadcount)

# Symmetry
if "Horizontal" in symmetry or symmetry == "Rotational 180°":
    seq = seq + seq[::-1]
elif symmetry == "Both (pmm)":
    half = seq + seq[::-1]
    seq = half + half

# Shadow mode
if shadow_mode:
    toned = []
    for letter in seq:
        toned.extend(color_tones[letter])
    seq = toned
else:
    toned = [color_tones[letter][2] for letter in seq]

# === Dynamische grootte + nooit meer smalle streep ===
total_threads = len(toned)
width_cm = max(sett_size, total_threads / 40)  # zorgt voor breedte bij lange tartans
fig, ax = plt.subplots(figsize=(width_cm * 1.2, 9))  # mooie verhouding

x = 0
for col in toned:
    ax.add_patch(patches.Rectangle((x, 0), 1, 1, color=col))
    x += 1

ax.set_xlim(0, total_threads)
ax.set_ylim(0, 1)
ax.set_aspect('auto')   # ← dit is de cruciale fix
ax.axis('off')
st.pyplot(fig)

if st.button("Download als PNG (kilt-ready)"):
    fig.savefig("tartan.png", dpi=300, bbox_inches='tight', facecolor="#111111")
    with open("tartan.png", "rb") as f:
        st.download_button("Download PNG", f, "tartan.png", "image/png")

st.caption(f"Sett: {sett_size} cm | Symmetrie: {symmetry} | Shadow mode: {'Aan' if shadow_mode else 'Uit'} | Threads: {total_threads}")
