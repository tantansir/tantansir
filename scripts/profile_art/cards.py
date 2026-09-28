"""Static cards for the README body: education drawn as a transit line, research interests as a map legend.
Same night palette as the header; no animation, so they cost nothing after the first paint."""
from common import P, font_face, n

W = 1200
CARD_BG = ("#0C1329", "#090E1F")
EDGE = "#1D2849"
LINE = "#8EA3CC"
MUTE = "#AAB7CF"


def card_open(h, title, desc, fonts, extra_css=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-labelledby="t d">'
        f'<title id="t">{title}</title><desc id="d">{desc}</desc>'
        f"<style>{fonts}"
        ".eyebrow{font-family:'KT Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-weight:500;font-size:15px;letter-spacing:3px;fill:" + P["amber"] + "}"
        ".aside{font-family:'KT Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-weight:500;font-size:13px;letter-spacing:2px;fill:#6F82AA}"
        f"{extra_css}</style>"
        "<defs>"
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CARD_BG[0]}"/><stop offset="1" stop-color="{CARD_BG[1]}"/></linearGradient>'
        f'<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="12" cy="12" r="1" fill="#8EA3CC" fill-opacity="0.09"/></pattern>'
        f'<radialGradient id="warm" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{P["amber"]}" stop-opacity="0.35"/><stop offset="1" stop-color="{P["amber"]}" stop-opacity="0"/></radialGradient>'
        "</defs>"
        f'<rect x="0.75" y="0.75" width="{W-1.5}" height="{h-1.5}" rx="18" fill="url(#bg)" stroke="{EDGE}" stroke-width="1.5"/>'
        f'<rect x="0.75" y="0.75" width="{W-1.5}" height="{h-1.5}" rx="18" fill="url(#dots)"/>'
    )


def eyebrow(label, aside=None):
    s = f'<path d="M48 45h26" stroke="{P["amber"]}" stroke-width="4" stroke-linecap="round"/>'
    s += f'<text class="eyebrow" x="88" y="50.5">{label}</text>'
    if aside:
        s += f'<text class="aside" x="{W-48}" y="50.5" text-anchor="end">{aside}</text>'
    return s


# ---------------------------------------------------------------- education: a transit line
STOPS = [
    dict(x=215, school="Tongji University", degree="B.Mgt. in Information Systems", years="2021 – 2025", city="SHANGHAI", icon="pearl"),
    dict(x=600, school="Carnegie Mellon University", degree="M.S. in Artificial Intelligence", years="2025 – 2026", city="PITTSBURGH", icon="bridge"),
    dict(x=985, school="New York University", degree="Ph.D. in Urban Science", years="2026 – 2031", city="NEW YORK", icon="arch", now=True),
]


def icon_pearl(cx, base):
    lw = f'stroke="{LINE}" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    s = [
        f'<path d="M{cx-16},{base} L{cx-4},{base-24} M{cx+16},{base} L{cx+4},{base-24} M{cx},{base} L{cx},{base-26}" {lw}/>',
        f'<circle cx="{cx}" cy="{base-35}" r="11" {lw}/>',
        f'<path d="M{cx-3},{base-46} L{cx-3},{base-58} M{cx+3},{base-46} L{cx+3},{base-58}" {lw}/>',
        f'<circle cx="{cx}" cy="{base-64}" r="6.5" {lw}/>',
        f'<path d="M{cx},{base-70.5} L{cx},{base-86}" {lw}/>',
        "".join(f'<circle cx="{n(cx + dx)}" cy="{base-35}" r="1.5" fill="{P["rose"]}"/>' for dx in (-6, -2, 2, 6)),
        f'<circle cx="{cx}" cy="{base-87.5}" r="2" fill="{P["red"]}"/>',
    ]
    return "".join(s)


def icon_bridge(cx, base):
    lw = f'stroke="{LINE}" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    y = base - 18
    s = [
        f'<path d="M{cx-52},{y} L{cx+52},{y}" {lw}/>',
        f'<path d="M{cx-26},{base} L{cx-26},{y-34} M{cx+26},{base} L{cx+26},{y-34}" {lw}/>',
        f'<path d="M{cx-52},{y-3} Q{cx-39},{y-4} {cx-26},{y-34} Q{cx},{y+2} {cx+26},{y-34} Q{cx+39},{y-4} {cx+52},{y-3}" stroke="{P["amber"]}" stroke-width="2.2" fill="none" stroke-linecap="round"/>',
    ]
    # hangers between the main cable and the deck
    hangers = []
    for i in range(1, 8):
        x = cx - 26 + i * 52 / 8
        t = (x - cx) / 26
        yy = y - 34 * (t * t) - 2
        hangers.append(f"M{n(x)},{n(yy)} L{n(x)},{y}")
    s.append(f'<path d="{" ".join(hangers)}" stroke="{LINE}" stroke-width="1.2" stroke-opacity="0.7"/>')
    s.append(f'<path d="M{cx-60},{base} Q{cx},{base-6} {cx+60},{base}" stroke="{LINE}" stroke-width="1.4" stroke-opacity="0.35" fill="none"/>')
    return "".join(s)


def icon_arch(cx, base):
    lw = f'stroke="{LINE}" stroke-width="2.2" fill="none" stroke-linejoin="round"'
    top = base - 70
    s = [
        f'<path d="M{cx-30},{base} L{cx-30},{top+14} L{cx+30},{top+14} L{cx+30},{base}" {lw}/>',
        f'<path d="M{cx-34},{top+14} L{cx+34},{top+14} M{cx-32},{top+7} L{cx+32},{top+7} M{cx-30},{top} L{cx+30},{top} M{cx-32},{top+7} L{cx-30},{top} M{cx+32},{top+7} L{cx+30},{top}" {lw}/>',
        f'<path d="M{cx-14},{base} L{cx-14},{top+36} A14 14 0 0 1 {cx+14},{top+36} L{cx+14},{base}" {lw}/>',
        f'<path d="M{cx-14},{base} L{cx-14},{top+36} A14 14 0 0 1 {cx+14},{top+36} L{cx+14},{base} Z" fill="url(#warm)"/>',
        f'<path d="M{cx-22},{top+26} L{cx-22},{top+50} M{cx+22},{top+26} L{cx+22},{top+50}" stroke="{LINE}" stroke-width="1.2" stroke-opacity="0.6"/>',
    ]
    return "".join(s)


ICONS = {"pearl": icon_pearl, "bridge": icon_bridge, "arch": icon_arch}


def education():
    H = 340
    ly = 176
    parts = []
    parts.append(eyebrow("EDUCATION", "SHANGHAI → PITTSBURGH → NEW YORK"))
    first, last = STOPS[0]["x"], STOPS[-1]["x"]
    # the line: travelled part solid, the road ahead dashed
    parts.append(f'<path d="M{first},{ly} L{last},{ly}" stroke="{P["amber"]}" stroke-width="8" stroke-linecap="round"/>')
    parts.append(f'<path d="M{last+22},{ly} L{W-70},{ly}" stroke="{P["amber"]}" stroke-width="8" stroke-linecap="round" stroke-dasharray="0.1 16" stroke-opacity="0.55"/>')
    parts.append(f'<path d="M{W-78},{ly-9} L{W-66},{ly} L{W-78},{ly+9}" stroke="{P["amber"]}" stroke-opacity="0.55" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    for s in STOPS:
        x = s["x"]
        parts.append(ICONS[s["icon"]](x, ly - 30))
        if s.get("now"):
            parts.append(f'<circle cx="{x}" cy="{ly}" r="40" fill="url(#warm)"/>')
            parts.append(f'<circle cx="{x}" cy="{ly}" r="22" fill="none" stroke="{P["amber"]}" stroke-opacity="0.45" stroke-width="2"/>')
            parts.append(f'<circle cx="{x}" cy="{ly}" r="14" fill="{CARD_BG[0]}" stroke="{P["amber"]}" stroke-width="5"/>')
            parts.append(f'<circle cx="{x}" cy="{ly}" r="6" fill="{P["amber"]}"/>')
        else:
            parts.append(f'<circle cx="{x}" cy="{ly}" r="13" fill="{CARD_BG[0]}" stroke="{P["amber"]}" stroke-width="5"/>')
        parts.append(f'<text class="school" x="{x}" y="{ly+64}">{s["school"]}</text>')
        parts.append(f'<text class="degree" x="{x}" y="{ly+98}">{s["degree"]}</text>')
        parts.append(f'<text class="years" x="{x}" y="{ly+132}">{s["years"]} <tspan class="dot">·</tspan> {s["city"]}</text>')
    css = (
        ".school{font-family:'KT Sans',Inter,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;font-weight:600;font-size:29px;fill:" + P["ink"] + ";text-anchor:middle}"
        ".degree{font-family:'KT Sans',Inter,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;font-weight:400;font-size:21.5px;fill:" + MUTE + ";text-anchor:middle}"
        ".years{font-family:'KT Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-weight:500;font-size:16px;letter-spacing:1.6px;fill:" + P["amber"] + ";text-anchor:middle}"
        ".years .dot{fill:#6F82AA}"
    )
    text_600 = "".join(s["school"] for s in STOPS)
    text_400 = "".join(s["degree"] for s in STOPS)
    text_mono = "EDUCATION SHANGHAI → PITTSBURGH → NEW YORK" + "".join(s["years"] + " · " + s["city"] for s in STOPS)
    fonts = (
        font_face("KT Sans", "Inter-600.ttf", text_600, 600)
        + font_face("KT Sans", "Inter-400.ttf", text_400, 400)
        + font_face("KT Mono", "JetBrainsMono-500.ttf", text_mono, 500)
    )
    desc = "; ".join(f'{s["school"]}, {s["degree"]}, {s["years"]}, {s["city"].title()}' for s in STOPS)
    return card_open(H, "Education", desc, fonts, css) + "".join(parts) + "</svg>\n"


# ---------------------------------------------------------------- research: a map legend
def g_icon(body, x, y):
    return f'<g transform="translate({n(x)} {n(y)})" stroke-linecap="round" stroke-linejoin="round" fill="none">{body}</g>'


def icon_urban():
    L, A = LINE, P["amber"]
    return (
        f'<rect x="4" y="4" width="56" height="56" rx="6" stroke="{L}" stroke-width="2.2"/>'
        f'<path d="M4 23 H60 M4 41 H60 M23 4 V60 M42 4 V60" stroke="{L}" stroke-width="1.6" stroke-opacity="0.7"/>'
        f'<rect x="25.5" y="25.5" width="14" height="13" rx="1.5" fill="{A}" fill-opacity="0.9" stroke="none"/>'
        f'<rect x="6.5" y="43.5" width="14" height="14" rx="1.5" fill="{A}" fill-opacity="0.35" stroke="none"/>'
        f'<rect x="44.5" y="6.5" width="13" height="14" rx="1.5" fill="{A}" fill-opacity="0.55" stroke="none"/>'
    )


def icon_embodied():
    L, C = LINE, P["cyan"]
    return (
        f'<path d="M32 4 V11" stroke="{L}" stroke-width="2.2"/><circle cx="32" cy="3.5" r="2.6" fill="{C}" stroke="none"/>'
        f'<rect x="12" y="11" width="40" height="30" rx="11" stroke="{L}" stroke-width="2.2"/>'
        f'<path d="M19 25 H45" stroke="{C}" stroke-width="7" stroke-opacity="0.25"/>'
        f'<circle cx="24" cy="25" r="3" fill="{C}" stroke="none"/><circle cx="40" cy="25" r="3" fill="{C}" stroke="none"/>'
        f'<path d="M27 41 V46 H37 V41" stroke="{L}" stroke-width="2.2"/>'
        f'<path d="M10 62 C10 52 18 46 32 46 C46 46 54 52 54 62" stroke="{L}" stroke-width="2.2"/>'
    )


def icon_robotic_urban():
    L, A, C = LINE, P["amber"], P["cyan"]
    wins = "".join(f'<rect x="{9+c*9}" y="{12+r*10}" width="4.5" height="5" rx="0.8" fill="{A}" fill-opacity="{0.9 if (r+c)%3 else 0.3}" stroke="none"/>' for r in range(4) for c in range(3))
    return (
        f'<path d="M4 60 H62" stroke="{L}" stroke-width="2.2"/>'
        f'<rect x="4" y="5" width="34" height="55" rx="2" stroke="{L}" stroke-width="2.2"/>{wins}'
        f'<rect x="40" y="40" width="20" height="13" rx="4" stroke="{C}" stroke-width="2.2"/>'
        f'<circle cx="45" cy="57" r="3" stroke="{C}" stroke-width="2"/><circle cx="55" cy="57" r="3" stroke="{C}" stroke-width="2"/>'
        f'<path d="M56 40 V30" stroke="{C}" stroke-width="1.8"/><path d="M56 30 L62 32.5 L56 35" fill="{A}" stroke="none"/>'
    )


def icon_sensing():
    L, C, A = LINE, P["cyan"], P["amber"]
    pts = [(44, 14), (50, 20), (56, 12), (48, 30), (58, 28), (52, 38), (60, 44), (46, 48), (54, 54), (40, 40)]
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="{1.9 if i%3 else 2.4}" fill="{A if i%4==0 else C}" fill-opacity="{0.95 if i%2 else 0.6}" stroke="none"/>' for i, (x, y) in enumerate(pts))
    return (
        f'<circle cx="10" cy="32" r="5" fill="{C}" stroke="none"/>'
        f'<path d="M19 22 A14 14 0 0 1 19 42" stroke="{L}" stroke-width="2.2"/>'
        f'<path d="M25 15 A23 23 0 0 1 25 49" stroke="{L}" stroke-width="2.2" stroke-opacity="0.75"/>'
        f'<path d="M31 8 A32 32 0 0 1 31 56" stroke="{L}" stroke-width="2.2" stroke-opacity="0.5"/>{dots}'
    )


def icon_twins():
    L, C, A = LINE, P["cyan"], P["amber"]
    wins = "".join(f'<rect x="{8+c*8}" y="{18+r*9}" width="4" height="4.5" rx="0.7" fill="{A}" fill-opacity="0.85" stroke="none"/>' for r in range(4) for c in range(2))
    return (
        f'<path d="M4 60 H28 V14 L16 6 L4 14 Z" stroke="{L}" stroke-width="2.2"/>{wins}'
        f'<path d="M36 60 H60 V14 L48 6 L36 14 Z" stroke="{C}" stroke-width="2" stroke-dasharray="3 3.5"/>'
        f'<path d="M36 22 H60 M36 31 H60 M36 40 H60 M36 49 H60 M44 14 V60 M52 14 V60" stroke="{C}" stroke-width="1" stroke-opacity="0.45"/>'
        f'<path d="M27 3 C31 0 33 0 37 3" stroke="{L}" stroke-width="1.6"/><path d="M35 1 L37.4 3.2 L34.6 4.4" stroke="{L}" stroke-width="1.6"/>'
    )


INTERESTS = [
    ("Urban Science", None, icon_urban),
    ("Embodied AI", None, icon_embodied),
    ("Robotic", "Urbanization", icon_robotic_urban),
    ("Multimodal", "Urban Sensing", icon_sensing),
    ("Digital Twins", None, icon_twins),
]


def research():
    H = 282
    parts = [eyebrow("RESEARCH INTERESTS", "LEGEND")]
    step = (W - 96) / len(INTERESTS)
    for i, (a, b, icon) in enumerate(INTERESTS):
        cx = 48 + step * (i + 0.5)
        parts.append(f'<circle cx="{n(cx)}" cy="116" r="50" fill="#121B38" stroke="{EDGE}" stroke-width="1.5"/>')
        parts.append(f'<g transform="translate({n(cx)} 116) scale(1.18) translate(-32 -32)">{g_icon(icon(), 0, 0)}</g>')
        parts.append(f'<text class="num" x="{n(cx)}" y="192">{i+1:02d}</text>')
        parts.append(f'<text class="label" x="{n(cx)}" y="222">{a}</text>')
        if b:
            parts.append(f'<text class="label" x="{n(cx)}" y="250">{b}</text>')
    css = (
        ".label{font-family:'KT Sans',Inter,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;font-weight:600;font-size:23px;fill:" + P["ink"] + ";text-anchor:middle}"
        ".num{font-family:'KT Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-weight:500;font-size:13px;letter-spacing:2px;fill:#6F82AA;text-anchor:middle}"
    )
    text_600 = "".join(f"{a} {b or ''}" for a, b, _ in INTERESTS)
    fonts = font_face("KT Sans", "Inter-600.ttf", text_600, 600) + font_face("KT Mono", "JetBrainsMono-500.ttf", "RESEARCH INTERESTS LEGEND 0123456789", 500)
    desc = "Research interests: " + ", ".join(f"{a} {b}" if b else a for a, b, _ in INTERESTS)
    return card_open(H, "Research interests", desc, fonts, css) + "".join(parts) + "</svg>\n"
