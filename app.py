# app.py – Definitieve Echte Tartan Mirror (nov 2025 – werkt gegarandeerd)
import streamlit as st
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt

# Authentieke tartan-kleuren
COLORS = {
    "R": (178, 34, 52), "DR": (120, 0, 0), "G": (0, 115, 46), "DG": (0, 70, 35),
    "B": (0, 41, 108), "DB": (0, 20, 60), "K": (30, 30, 30), "W": (255, 255, 255),
    "Y": (255, 203, 0), "O": (255, 102, 0), "P": (128, 0, 128), "LG": (200, 230, 200),
    "LB": (180, 200, 230), "A": (160, 160, 160), "T": (0, 130, 130),
}

def parse_threadcount(tc: str):
    parts = tc.upper().strip().split()
    pattern = []
    for part in parts:
        if not part:
            continue
        color = None
        num_str = part
        for c in sorted(COLORS.keys(), key=len, reverse=True):
            if part.startswith(c):
                color = c
                num_str = part[len(c):]
                break
            if part.endswith(c):
                color = c
                num_str = part[:-len(c)]
                break
        if color is None:
            st.error(f"Kleur niet herkend in '{part}'")
            return None
        if not num_str:
            count = 1.0
        elif '/' in num_str:
            count = int(num_str.split('/')[1]) / 2
        else:
            count = float(num_str)
        pattern.append((color, count))
    return pattern

def build_sett(pattern):
    forward_counts = [c for _, c in pattern]
    forward_colors  = [col for col, _ in pattern]
    mirror_counts = forward_counts[::-1][1:]
    mirror_colors = forward_colors[::-1][1:]
    return forward_counts + mirror_counts, forward_colors + mirror_colors

def create_tartan(pattern, size=900, thread_width=4, texture=True):
    sett_counts, sett_colors = build_sett(pattern)
    if not sett_counts:
        return np.zeros((size, size, 3), dtype=np.uint8)

    widths = [int(round(c * thread_width)) for c in sett_counts]
    for w in widths:
        if w <= 0:
            return np.zeros((size, size, 3), dtype=np.uint8)  # voorkom lege breedtes

    sett_pixel_width = sum(widths)
    repeats = max(2, (size // sett_pixel_width) + 2)

    tile = np.zeros((sett_pixel_width * repeats, sett_pixel_width * repeats, 3), dtype=np.uint16)

    # Warp (verticaal)
    x = 0
    for _ in range(repeats):
        for w, col in zip(widths, sett_colors):
            tile[:, x:x + w] = COLORS[col]
            x += w

    # Weft (horizontaal)
    weft = tile.copy().transpose(1, 0, 2)

    # Overcheck + textuur
    tartan = np.minimum(tile + weft, 255).astype(np.uint8)
    
    if texture:
        noise = np.random.randint(-18, 22, tartan.shape, dtype=np.int16)
        tartan = np.clip(tartan.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Center crop
    start = (tartan.shape[0] - size) // 2
    return tartan[start:start + size, start:start + size]

# ────────────────────────── Streamlit App ──────────────────────────

st.set_page_config(page_title="Echte Tartan Mirror", layout="centered")
st.title("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Tartan ")

st.markdown("**100% authentiek**")

c1, c2 = st.columns([3, 1])
with c1:
    tc = st.text_input("Threadcount", value="DB4 G28 DB4 G6 DB28 K6", help="bijv. R28 W4 R8 Y4 R28 K32")
with c2:
    tw = st.slider("Draad-dikte", 1, 10, 4)
    tex = st.checkbox("Wol-textuur", True)

if tc.strip():
    pattern = parse_threadcount(tc)
    if pattern:
        half_sett = sum(c for _, c in pattern)
        st.caption(f"Half-sett: {half_sett:.1f} threads → volledige sett: {2*half_sett - pattern[-1][1]:.1f} threads")

        img = create_tartan(pattern, size=900, thread_width=tw, texture=tex)
        st.image(img, use_column_width=True)

        # Download
        buf = BytesIO()
        plt.imsave(buf, img, format="png")
        buf.seek(0)
        st.download_button(
            "💾 Download PNG (900×900)",
            buf,
            file_name=f"tartan_{tc.strip().replace(' ', '_').replace('/', '-')}.png",
            mime="image/png"
        )

        # Toon volledige symmetrische sett
        counts, colors = build_sett(pattern)
        sett_str = " ".join(f"{col}{int(round(c))}" for col, c in zip(colors, counts))
        st.code(sett_str, language=None)

st.info("""
Klassieke tartans (kopieer-plak):
• MacDonald → R18 K12 B6
• Royal Stewart → R28 W4 R8 Y4 R28 K32
• Black Watch → DB4 G28 DB4 G6 DB28 K6
• Dress Gordon → K4 B24 K24 Y4 K60
• Burberry → K6 W6 R32 W32 K6
""")


