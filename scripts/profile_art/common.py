"""Shared pieces for the profile artwork: palette, number formatting and font embedding.

Fonts come from Google Fonts on first use and are cached in .fonts/. Each SVG embeds only
the glyphs it draws, as a WOFF2 data URI, because an SVG shown through <img> (which is
how GitHub renders README images) cannot load external fonts.
"""
import base64
import hashlib
import io
import os
import re
import urllib.parse
import urllib.request
from functools import lru_cache

from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_CACHE = os.path.join(HERE, ".fonts")

# One palette for every asset so the page reads as a single piece.
P = {
    "sky0": "#03060E",
    "sky1": "#0A1230",
    "sky2": "#1C1B40",
    "sky3": "#3A2645",
    "sky4": "#5C3447",
    "far": "#191D3C",
    "mid": "#0B1024",
    "near": "#05070F",
    "unlit": "#1B2244",
    "amber": "#FFB54D",
    "warm": "#FFD27A",
    "warmwhite": "#FFE9BD",
    "orange": "#FF9A55",
    "cool": "#D6E6FF",
    "tv": "#86CCFF",
    "cyan": "#63E6F2",
    "rose": "#FF7EB0",
    "red": "#FF5A48",
    "ink": "#F6EFE2",
    "mute": "#9DB0CB",
    "seal": "#C8412D",
}

# cache file name -> Google Fonts css2 family spec
FONT_SOURCES = {
    "InstrumentSerif-Regular.ttf": "Instrument Serif",
    "JetBrainsMono-500.ttf": "JetBrains Mono:wght@500",
    "Inter-400.ttf": "Inter:wght@400",
    "Inter-600.ttf": "Inter:wght@600",
    "NotoSerifSC-900.ttf": "Noto Serif SC:wght@900",
}
# CJK fonts are ~15 MB; ask Google for just the characters we draw instead.
SUBSET_ON_SERVER = {"NotoSerifSC-900.ttf"}


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


def font_path(name, text=""):
    spec = FONT_SOURCES[name]
    query = "family=" + urllib.parse.quote(spec, safe=":@;,")
    key = name
    if name in SUBSET_ON_SERVER:
        chars = "".join(sorted(set(text)))
        key = f"{name[:-4]}-{hashlib.sha1(chars.encode()).hexdigest()[:8]}.ttf"
        query += "&text=" + urllib.parse.quote(chars)
    path = os.path.join(FONT_CACHE, key)
    if not os.path.exists(path):
        os.makedirs(FONT_CACHE, exist_ok=True)
        # a non-browser client gets TrueType URLs back from the CSS API
        css = urllib.request.urlopen(f"https://fonts.googleapis.com/css2?{query}").read().decode()
        url = re.search(r"url\((https://[^)]+)\)", css).group(1)
        data = urllib.request.urlopen(url).read()
        with open(path, "wb") as f:
            f.write(data)
    return path


@lru_cache(maxsize=None)
def _metrics(name):
    f = TTFont(font_path(name), recalcTimestamp=False)
    return f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm


def text_width(name, text, size, tracking=0.0):
    cmap, hmtx, upm = _metrics(name)
    w = sum(hmtx[cmap[ord(c)]][0] for c in text if ord(c) in cmap)
    return w / upm * size + tracking * max(len(text) - 1, 0)


def font_face(family, name, text, weight=400):
    """@font-face rule carrying a WOFF2 subset with only the glyphs in `text`."""
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.notdef_outline = False
    font = TTFont(font_path(name, text), recalcTimestamp=False)  # keep output byte-stable
    sub = subset.Subsetter(opts)
    sub.populate(text="".join(sorted(set(text))))
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"@font-face{{font-family:'{family}';font-weight:{weight};src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
