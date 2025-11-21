import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Tartan Designer – Graduated Sett", layout="wide")
st.title("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Tartan Designer – Graduated Sett Edition")

# === 5 tinten per kleur (dark → base → light → base → dark) ===
color_tones = {
    "K": ["#000000", "#111111", "#222222", "#111111", "#000000"],  # Black
    "R": ["#400000", "#800000", "#C00000", "#800000", "#400000"],  # Red
    "G": ["#003000", "#006000", "#008000", "#006000", "#003000"],  # Green
    "B": ["#000040", "#000080", "#0000C0", "#000080", "#000040"],  # Blue
    "Y": ["#806000", "#C0A000", "#FFC000", "#C0A000", "#806000"],  # Yellow
    "W": ["#CCCCCC", "#DDDDDD", "#FFFFFF", "#DDDDDD", "#CCCCCC"],  # White
    "P": ["#400040", "#800080", "#C000C0", "#800080", "#400040"],  # Purple
    "O": ["#803000", "#C06000", "#FF8000", "#C06000", "#803000"],  # Orange
    "A": ["#404040", "#606060", "#808080", "#606060", "#404040"],  # Grey
}

st.sidebar.header("Sett samenstellen")
threadcount = st.sidebar.text_area(
    "Threadcount (bijv. R8 G24 B8 K32 Y4)",
    "R8 G24 B8 K32 Y4 R8 G24 B8 K32 Y4",
    height=100
)

symmetry = st.sidebar.selectbox(
    "Symmetrie",
    ["Horizontal (reversed sett)", "Both (pmm)", "Rotational 180°", "None"]
)

graduated_mode = st.sidebar.checkbox("Graduated sett (tonal blend)", value=True,
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

# === Graduated sett (tonal blend) ===
if graduated_mode:
    graduated = []
    for letter in seq:
        graduated.extend(color_tones[letter])   # 5 tinten per originele thread
    seq = graduated
else:
    graduated = [color_tones[letter][2] for letter in seq]  # alleen basis-kleur

# === Tekening (altijd mooie verhouding) ===
total = len(graduated)
width_cm = max(sett_size, total / 50)  # voorkomt smalle streep
fig, ax = plt.subplots(figsize=(width_cm * 1.5, 8))

x = 0
for col in graduated:
    ax.add_patch(patches.Rectangle((x, 0), 1, 1, color=col))
    x += 1

ax.set_xlim(0, x)
ax.set_ylim(0, 1)
ax.axis("off")
ax.set_aspect("equal")
st.pyplot(fig)

# === Download ===
if st.button("Download als PNG (kilt-ready)"):
    fig.savefig("graduated_tartan.png", dpi=300, bbox_inches="tight", facecolor="#111111")
    with open("graduated_tartan.png", "rb") as f:
        st.download_button("Download PNG", f, "graduated_tartan.png", "image/png")

st.caption(f"Sett: {sett_size} cm | Symmetrie: {symmetry} | Graduated sett: {'Aan' if graduated_mode else 'Uit'} | Threads: {total}")
