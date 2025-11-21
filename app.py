# app.py – 100% werkende Echte Tartan Mirror (nov 2025)
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
        # Zoek de kleur (kan 1 of 2 letters zijn)
        color = None
        num_str = part
        for c in sorted(COLORS, key=len, reverse=True):  # langste eerst (DR voor R)
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
        # Parse getal (ondersteunt /6 voor halve counts)
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

def create_tartan(pattern, size=900, thread_width=3, texture=True):
    sett_counts, sett_colors = build_sett(pattern)
    if not sett_counts:
        return np.zeros((size, size, 3), dtype=np.uint8)

    # Belangrijk: rounden i.p.v. int() op floats
    widths = [int(round(c * thread_width)) for c in sett_counts]
    sett_pixel_width = sum(widths)
    repeats = max(2, (size // sett_pixel_width) + 2)

    tile = np.zeros((sett_pixel_width * repeats, sett_pixel_width * repeats, 3), dtype=np.uint16)

    # Warp (verticaal)
    x = 0
    for _ in range(repeats):
        for w, col in zip(widths, sett_colors):
            tile[:, x:x+w] = COLORS[col]
            x += w

    # Weft (horizontaal)
    weft = tile.copy().transpose(1, 0, 2)

    # Overcheck + textuur
    tartan = np.minimum(tile + weft, 255).astype(np.uint8)
    if texture:
        noise =
