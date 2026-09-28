"""Shared pieces for the profile artwork: palette, number formatting and font embedding.

Fonts come from Google Fonts on first use and are cached in .fonts/. Each SVG embeds only
the glyphs it draws, as a WOFF2 data URI, because an SVG shown through <img> (which is
how GitHub renders README images) cannot load external fonts.
"""
import base64
import io
import os
import re
import urllib.parse
import urllib.request

from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_CACHE = os.path.join(HERE, ".fonts")

# One palette for every asset so the page reads as a single piece.
P = {
    # blue hour: cobalt overhead, a peach glow on the horizon, never black
    "sky0": "#14224E",
    "sky1": "#22387A",
    "sky2": "#3E4C92",
    "sky3": "#9A6C98",
    "sky4": "#E9A07C",
    "far": "#3A3D70",
    "mid": "#171C3D",
    "near": "#0B0E22",
    "unlit": "#2B3263",
    "amber": "#FFB54D",
    "warm": "#FFD27A",
    "warmwhite": "#FFE9BD",
    "orange": "#FF9A55",
    "cool": "#D6E6FF",
    "tv": "#86CCFF",
    "cyan": "#63E6F2",
    "rose": "#FF7EB0",
    "red": "#FF5A48",
    "ink": "#FBF6EC",
    "mute": "#D5DDF5",
}

RADIUS = 18

# cache file name -> Google Fonts css2 family spec
FONT_SOURCES = {
    "InstrumentSerif-Regular.ttf": "Instrument Serif",
    "JetBrainsMono-500.ttf": "JetBrains Mono:wght@500",
    "Inter-400.ttf": "Inter:wght@400",
    "Inter-600.ttf": "Inter:wght@600",
}


def n(v):
    """Compact number for SVG attributes (2 decimals)."""
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def n1(v):
    """Compact number for path data (1 decimal)."""
    s = f"{v:.1f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def rect_d(x, y, w, h):
    """A rectangle as a path fragment, so many of them can share one <path>."""
    return f"M{n1(x)} {n1(y)}h{n1(w)}v{n1(h)}h{n1(-w)}z"


def font_path(name):
    query = "family=" + urllib.parse.quote(FONT_SOURCES[name], safe=":@;,")
    path = os.path.join(FONT_CACHE, name)
    if not os.path.exists(path):
        os.makedirs(FONT_CACHE, exist_ok=True)
        # a non-browser client gets TrueType URLs back from the CSS API
        css = urllib.request.urlopen(f"https://fonts.googleapis.com/css2?{query}").read().decode()
        url = re.search(r"url\((https://[^)]+)\)", css).group(1)
        data = urllib.request.urlopen(url).read()
        with open(path, "wb") as f:
            f.write(data)
    return path


def font_face(family, name, text, weight=400):
    """@font-face rule carrying a WOFF2 subset with only the glyphs in `text`."""
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.notdef_outline = False
    font = TTFont(font_path(name), recalcTimestamp=False)  # keep output byte-stable
    sub = subset.Subsetter(opts)
    sub.populate(text="".join(sorted(set(text))))
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"@font-face{{font-family:'{family}';font-weight:{weight};src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
