import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Tartan Designer – Graduated Sett", layout="wide")
st.title("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Tartan Designer – Graduated Sett Edition")

# === 5 tinten per kleur (dark → base → light → base → dark) ===
color_tones = {
    "K": ["#000000", "#111111", "#222222", "#111111", "#000000"],
    "R": ["#400000", "#800000", "#C00000", "#800000", "#400000"],
    "G": ["#003000", "#006000", "#008000", "#006000", "#003000"],
    "B": ["#000040", "#000080", "#0000C0", "#000080", "#000040"],
    "Y": ["#806000", "#C0A000", "#FFC000", "#C0A000", "#806000"],
    "W": ["#CCCCCC", "#DDDDDD", "#FFFFFF", "#DDDDDD", "#CCCCCC"],
    "P": ["#400040", "#800080", "#C000C0", "#800080", "#400040"],
    "O": ["#803000", "#C06000", "#FF8000", "#C06000", "#803000"],
    "A": ["#404040", "#606060", "#808080", "#606060", "#404040"],
}

st.sidebar.header("Sett samenstellen")
threadcount = st.sidebar.text_area("Threadcount", "R8 G24 B8 K32 Y4 R8 G24 B8 K32 Y4", height=100)

symmetry = st.sidebar.selectbox("Symmetrie", ["Horizontal (reversed sett)", "Both (pmm)", "Rotational 180°", "None"])

graduated = st.sidebar.checkbox("Graduated sett (tonal blend)", value=True,
    help="Elke kleur wordt 5 tinten: donker → basis → licht → basis → donker"
)

sett_size = st.sidebar.slider("Sett-grootte (cm)", 5, 60, 20)

# === Parse ===
def parse_tc(tc):
    parts = tc.upper().split()
    seq = []
    for part in parts:
        if len(part) > 1 and part[0] in color_tones and part[1:].isdigit():
            seq.extend([part[0]] * int(part[1:]))
    return seq

seq = parse_tc(threadcount)

# === Symmetry ===
if "Horizontal" in symmetry or symmetry == "Rotational 180°":
    seq = seq + seq[::-1]
elif symmetry == "Both (pmm)":
    half = seq + seq[::-1]
    seq = half + half

# === Graduated sett ===
if graduated:
    final_seq = []
    for letter in seq:
        final_seq.extend(color_tones[letter])   # 5 tinten per originele thread
else:
    final_seq = [color_tones[letter][2] for letter in seq]  # alleen basis-kleur

total = len(final_seq)

# === Altijd brede rechthoek (nooit meer streep!) ===
width_cm = max(sett_size, total / 50)   # schaal met aantal threads
fig, ax = plt.subplots(figsize=(width_cm * 1.4, 9))

x = 0
for col in final_seq:
    ax.add_patch(patches.Rectangle((x, 0), 1, 1, color=col))
    x += 1

ax.set_xlim(0, total)
ax.set_ylim(0, 1)
ax.set_aspect('auto')      # ← cruciale fix
ax.axis('off')
st.pyplot(fig)

# === Download ===
if st.button("Download als PNG (kilt-ready)"):
    fig.savefig("graduated_tartan.png", dpi=300, bbox_inches='tight', facecolor="#111111")
    with open("graduated_tartan.png", "rb") as f:
        st.download_button("Download PNG", f, "graduated_tartan.png", "image/png")

st.caption(f"Sett: {sett_size} cm | Symmetrie: {symmetry} | Graduated sett: {'Aan' if graduated else 'Uit'} | Threads: {total}")
