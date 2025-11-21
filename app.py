# app.py – Echte Tartan Mirror (correcte Schotse weefsimulatie)
import streamlit as st
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt

# ≈ Officiële tartan-kleuren (RGB, zo dicht mogelijk bij wol)
COLORS = {
    "R": (178, 34, 52),   # Red
    "DR": (120, 0, 0),     # Dark Red
    "G": (0, 115, 46),     # Green
    "DG": (0, 70, 35),     # Dark Green
    "B": (0, 41, 108),     # Blue
    "DB": (0, 20, 60),     # Dark Blue / Navy
    "K": (30, 30, 30),     # Black
    "W": (255, 255, 255),  # White
    "Y": (255, 203, 0),    # Yellow / Gold
    "O": (255, 102, 0),    # Orange
    "P": (128, 0, 128),    # Purple
    "LG": (200, 230, 200), # Light Green
    "LB": (180, 200, 230), # Light Blue
    "A": (160, 160, 160),  # Azure / Grey
    "T": (0, 130, 130),    # Teal
}

def parse_threadcount(tc: str):
    """Ondersteunt halve counts (R/6) en normale (R18)"""
    parts = tc.upper().strip().split()
    pattern = []
    for p in parts:
        if not p: continue
        if p[0] in COLORS:
            color = p[0]
            num_str = p[1:]
        else:
            color = p[-1] if p[-1] in COLORS else p[0]
            num_str = p.replace(color, "")
        if '/' in num_str:
            count = float(num_str.split('/')[1]) / 2   # halve count
        else:
            count = int(num_str)
        pattern.append((color, count))
    return pattern

def build_sett(pattern):
    """Maakt de volledige symmetrische sett (warp = weft)"""
    if not pattern:
        return [], []
    # Forward deel
    forward_counts = [c for _, c in pattern]
    forward_colors = [col for col
