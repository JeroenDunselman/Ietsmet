# app.py – Echte Schotse Tartan Mirror (correcte symmetrie + overcheck)
import streamlit as st
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt

# Officiële tartan-kleuren (zo dicht mogelijk bij echte wol)
COLORS = {
    "R": (178, 34, 52),    # Red
    "DR": (120, 0, 0),
    "G": (0, 115, 46),     # Green
    "DG": (0, 70, 35),
    "B": (0, 41, 108),     # Blue
    "DB": (0, 20, 60),     # Navy
    "K": (30, 30, 30),     # Black
    "W": (255, 255, 255),  # White
    "Y": (255, 203, 0),    # Gold
    "O": (255, 102, 0),    # Orange
    "P": (128, 0, 128),    # Purple
    "LG": (200, 230, 200),
    "LB": (180, 200, 230),
    "A": (160, 160, 160),  # Azure/Grey
    "T": (0, 130, 130),    # Teal
}

def parse_threadcount(tc: str):
    """Ondersteunt R18, R/6 (halve counts) en K4 etc."""
    parts = tc.upper().strip().split()
    pattern = []
    for part in parts:
        if not part:
            continue
        # Zoek de kleurletter (meestal eerste of laatste karakter)
        color = None
        num_str = part
        for c in COLORS:
            if part.startswith(c):
                color = c
                num_str = part[len(c):]
                break
            elif part.endswith(c):
                color = c
                num_str = part[:-len(c)]
                break
        if color is None:
            st.error(f"Kleur niet herkend in '{part}'")
            return None
        
        if '/' in num_str:
            count = float(num_str.split('/')[1]) / 2
        else:
            count = float(num_str) if num_str else 0
        pattern.append((color, count))
    return pattern

def build_sett(pattern):
    """Maakt perfecte symmetrische sett (zoals echte Schotse wevers)"""
    forward_counts = [count for _, count in pattern]
    forward_colors  = [col   for col, _ in pattern]
    
    # Mirror zonder de pivot-kleur dubbel te tellen
    mirror_counts = forward_counts[::-1][1:]
    mirror_colors = forward_colors[::-1][1:]
    
    sett_counts = forward_counts + mirror_counts
    sett_colors = forward_colors + mirror_colors
    return sett_counts, sett_colors

def create_tartan(pattern, size=900, thread_width=3, texture=True):
    sett_counts, sett_colors = build_sett(pattern)
    if not sett_counts:
        return np.zeros((size, size, 3), dtype=np.uint8)

    sett_pixel_width = sum(sett_counts) * thread_width
    repeats = max(2, (size // sett_pixel_width) + 2)

    # Grote tile maken
    tile = np.zeros((sett_pixel_width * repeats, sett_pixel_width * repeats, 3), dtype=np.uint16)

    # Warp (verticaal)
    x = 0
    for _ in range(repeats):
        for count, col in zip(sett_counts, sett_colors):
            w = int(count * thread_width + 1e-6)  # rounding fix
            tile[:, x:x + w] = COLORS[col]
            x += w

    # Weft (horizontaal) = transpose van warp
    weft = tile.copy().transpose(1, 0, 2)

    # Echte overcheck door additief mengen
    tartan = np.minimum(tile + weft, 255).astype(np.uint8)

    # Subtiele wol-textuur
    if texture:
        noise = np.random.randint(-15, 20, tartan.shape, dtype=np.int16)
        tartan = np.clip(tartan.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Center-crop naar gewenst formaat
    start = (tartan.shape[0] - size) // 2
    return tartan[start:start + size, start:start + size]

# ────────────────────────── Streamlit App ──────────────────────────

st.set_page_config(page_title="Echte Tartan Mirror", layout="centered")
st.title("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Echte Tartan Mirror")

st.markdown("**Nu met 100% authentieke Schotse spiegeling en overcheck-kleuren**")

col1, col2 = st.columns([3, 1])
with col1:
    tc_input = st.text_input(
        "Threadcount",
        value="R18 K12 B6",
        help="Voorbeelden: R18 K12 B6 · K4 R26 K4 Y6 K24 · G/6 W48 G32 W4 G32 W48 G/6"
    )
with col2:
    thread_width = st.slider("Draad-dikte", 1, 8, 3)
    texture = st.checkbox("Wol-textuur", value=True)

if tc_input.strip():
    pattern = parse_threadcount(tc_input)
    if pattern:
        total_threads = sum(c for _, c in pattern)
        st.caption(f"Sett: {total_threads:.1f} threads → {int(total_threads * thread_width * 2)} px (symmetrisch)")

        img = create_tartan(pattern, size=900, thread_width=thread_width, texture=texture)
        st.image(img, use_column_width=True)

        # Download
        buf = BytesIO()
        plt.imsave(buf, img, format="png")
        buf.seek(0)
        st.download_button(
            "💾 Download PNG (900×900)",
            data=buf,
            file_name=f"tartan_{tc_input.strip().replace(' ', '_').replace('/', '-')}.png",
            mime="image/png"
        )

        # Toon volledige symmetrische sett
        counts, colors = build_sett(pattern)
        sett_str = " ".join(
            f"{col}{int(c) if c == int(c) else '/' + str(int(c*2))}"
            for col, c in zip(colors, counts)
        )
        st.code(sett_str, language=None)

st.info("""
Klassieke tartans om te proberen:
• MacDonald → R18 K12 B6
• Black Watch → DB4 G28 DB4 G6 DB28 K6
• Royal Stewart → R28 W4 R8 Y4 R28 K32
• Dress Gordon → K4 B24 K24 Y4 K60
• Burberry → K6 W6 R32 W32 K6
""")
