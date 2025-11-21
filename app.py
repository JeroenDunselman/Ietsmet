import streamlit as st

st.set_page_config(page_title="Tartan Weaving Sim – 2D Safe", layout="wide")
st.title("🧵 Tartan Weaving Simulator – 2D (no crash edition)")

color_map = {
    "K": "black", "R": "red", "G": "green", "B": "blue",
    "Y": "yellow", "W": "white", "P": "purple", "O": "orange",
    "A": "gray", "Gold": "gold"
}

st.sidebar.header("Warp (staand)")
warp_tc = st.sidebar.text_area("Warp", "K4 R28 K4 Y4 K24 R8 G24 B24 R8 K24 Y4", height=100)

st.sidebar.header("Weft (liggend)")
weft_tc = st.sidebar.text_area("Weft", "K4 R28 K4 Y4 K24 R8 G24 B24 R8 K24 Y4", height=100)

width = st.sidebar.slider("Breedte (sett-repeats)", 10, 100, 40)
height = st.sidebar.slider("Hoogte (sett-repeats)", 10, 80, 30)

# Parse
def tc_to_seq(tc):
    seq = []
    for part in tc.upper().split():
        if len(part) > 1 and part[0] in color_map and part[1:].isdigit():
            seq.extend([color_map[part[0]]] * int(part[1:]))
    return seq

warp = tc_to_seq(warp_tc)
weft = tc_to_seq(weft_tc)

if not warp or not weft:
    st.error("Vul beide threadcounts in!")
    st.stop()

# Maak HTML-grid (superlicht, nooit crash)
html = "<div style='line-height:1px; font-size:0;'>"
for y in range(height * len(weft)):
    for x in range(width * len(warp)):
        if (x + y) % 2 == 0:
            col = warp[x % len(warp)]
        else:
            col = weft[y % len(weft)]
        html += f"<div style='display:inline-block; width:4px; height:4px; background:{col};'></div>"
    html += "<br>"
html += "</div>"

st.components.v1.html(html, height=height*len(weft)*4 + 50, scrolling=True)

st.caption(f"Sett-repeats: {width} × {height} | Warp threads: {len(warp)} | Weft threads: {len(weft)}")
