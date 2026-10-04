"""Education drawn as a transit line, research interests as a map legend.

These sections have no background of their own. They sit on the page itself, so on GitHub's white
theme they read as part of the page instead of dark boxes separated by white gaps. Their colours
switch with the theme through a prefers-color-scheme block: browsers resolve that query for an
<img> from the colour scheme of the page around it, which GitHub sets from the viewer's theme.
No animation, so they cost nothing after the first paint.
"""
from common import P, font_face, n

W = 1200
MONO = "'KT Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "'KT Sans',Inter,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
SERIF = "'KT Serif','Iowan Old Style','Palatino Linotype',Georgia,serif"

# class -> (property, light theme, dark theme)
THEME = {
    "f-ink": ("fill", "#1C2440", "#F3EEE4"),
    "f-mute": ("fill", "#59647F", "#A9B4C8"),
    "f-dim": ("fill", "#8993AB", "#6F82AA"),
    "f-amt": ("fill", "#B8680F", "#FFB54D"),  # amber for text: darker on white to stay legible
    "f-am": ("fill", "#E39A2F", "#FFB54D"),
    "f-cy": ("fill", "#0F8F9E", "#63E6F2"),
    "f-ro": ("fill", "#D9578A", "#FF7EB0"),
    "f-rd": ("fill", "#E0483A", "#FF5A48"),
    "s-ln": ("stroke", "#56668F", "#8EA3CC"),
    "s-am": ("stroke", "#E39A2F", "#FFB54D"),
    "s-cy": ("stroke", "#0F8F9E", "#63E6F2"),
    "well": ("fill", "#EEF2F9", "#131C3A"),
    "well-e": ("stroke", "#D8E0EE", "#233056"),
}


def theme_css():
    light = "".join(f".{c}{{{prop}:{lo}}}" for c, (prop, lo, _) in THEME.items())
    dark = "".join(f".{c}{{{prop}:{hi}}}" for c, (prop, _, hi) in THEME.items())
    return light + "@media (prefers-color-scheme:dark){" + dark + "}"


def section_open(h, title, desc, fonts, extra_css=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-labelledby="t d">'
        f'<title id="t">{title}</title><desc id="d">{desc}</desc>'
        f"<style>{fonts}{theme_css()}"
        f".eyebrow{{font-family:{MONO};font-weight:500;font-size:15px;letter-spacing:3px}}"
        f"{extra_css}</style>"
        "<defs>"
        f'<radialGradient id="warm" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{P["amber"]}" stop-opacity="0.35"/><stop offset="1" stop-color="{P["amber"]}" stop-opacity="0"/></radialGradient>'
        "</defs>"
    )


def eyebrow(label):
    return (
        '<path class="s-am" d="M48 45h26" stroke-width="4" stroke-linecap="round"/>'
        f'<text class="eyebrow f-amt" x="88" y="50.5">{label}</text>'
    )


# ---------------------------------------------------------------- education: a transit line
STOPS = [
    dict(x=215, school="Tongji University", degree="B.Mgt. in Information Systems", years="2021 – 2025", city="SHANGHAI", icon="pearl"),
    dict(x=600, school="Carnegie Mellon University", degree="M.S. in Artificial Intelligence", years="2025 – 2026", city="PITTSBURGH", icon="bridge"),
    dict(x=985, school="New York University", degree="Ph.D. in Urban Science", years="2026 – 2031", city="NEW YORK", icon="arch", now=True),
]
LW = 'class="s-ln" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"'


def icon_pearl(cx, base):
    return "".join([
        f'<path d="M{cx-16},{base} L{cx-4},{base-24} M{cx+16},{base} L{cx+4},{base-24} M{cx},{base} L{cx},{base-26}" {LW}/>',
        f'<circle cx="{cx}" cy="{base-35}" r="11" {LW}/>',
        f'<path d="M{cx-3},{base-46} L{cx-3},{base-58} M{cx+3},{base-46} L{cx+3},{base-58}" {LW}/>',
        f'<circle cx="{cx}" cy="{base-64}" r="6.5" {LW}/>',
        f'<path d="M{cx},{base-70.5} L{cx},{base-86}" {LW}/>',
        "".join(f'<circle class="f-ro" cx="{n(cx + dx)}" cy="{base-35}" r="1.5"/>' for dx in (-6, -2, 2, 6)),
        f'<circle class="f-rd" cx="{cx}" cy="{base-87.5}" r="2"/>',
    ])


def icon_bridge(cx, base):
    y = base - 18
    hangers = []
    for i in range(1, 8):  # hangers between the main cable and the deck
        x = cx - 26 + i * 52 / 8
        t = (x - cx) / 26
        hangers.append(f"M{n(x)},{n(y - 34 * t * t - 2)} L{n(x)},{y}")
    return "".join([
        f'<path d="M{cx-52},{y} L{cx+52},{y}" {LW}/>',
        f'<path d="M{cx-26},{base} L{cx-26},{y-34} M{cx+26},{base} L{cx+26},{y-34}" {LW}/>',
        f'<path class="s-am" d="M{cx-52},{y-3} Q{cx-39},{y-4} {cx-26},{y-34} Q{cx},{y+2} {cx+26},{y-34} Q{cx+39},{y-4} {cx+52},{y-3}" stroke-width="2.2" fill="none" stroke-linecap="round"/>',
        f'<path class="s-ln" d="{" ".join(hangers)}" stroke-width="1.2" stroke-opacity="0.7"/>',
        f'<path class="s-ln" d="M{cx-60},{base} Q{cx},{base-6} {cx+60},{base}" stroke-width="1.4" stroke-opacity="0.35" fill="none"/>',
    ])


def icon_arch(cx, base):
    top = base - 70
    lw = 'class="s-ln" stroke-width="2.2" fill="none" stroke-linejoin="round"'
    return "".join([
        f'<path d="M{cx-14},{base} L{cx-14},{top+36} A14 14 0 0 1 {cx+14},{top+36} L{cx+14},{base} Z" fill="url(#warm)"/>',
        f'<path d="M{cx-30},{base} L{cx-30},{top+14} L{cx+30},{top+14} L{cx+30},{base}" {lw}/>',
        f'<path d="M{cx-34},{top+14} L{cx+34},{top+14} M{cx-32},{top+7} L{cx+32},{top+7} M{cx-30},{top} L{cx+30},{top} M{cx-32},{top+7} L{cx-30},{top} M{cx+32},{top+7} L{cx+30},{top}" {lw}/>',
        f'<path d="M{cx-14},{base} L{cx-14},{top+36} A14 14 0 0 1 {cx+14},{top+36} L{cx+14},{base}" {lw}/>',
        f'<path class="s-ln" d="M{cx-22},{top+26} L{cx-22},{top+50} M{cx+22},{top+26} L{cx+22},{top+50}" stroke-width="1.2" stroke-opacity="0.6"/>',
    ])


ICONS = {"pearl": icon_pearl, "bridge": icon_bridge, "arch": icon_arch}


def education():
    H = 358
    ly = 200
    parts = [eyebrow("EDUCATION")]
    # the travelled line runs between the stations, whose hollow rings show the page through them
    xs = [s["x"] for s in STOPS]
    ring = [14 if s.get("now") else 13 for s in STOPS]
    segs = "".join(f"M{a + ra},{ly} L{b - rb},{ly} " for a, b, ra, rb in zip(xs, xs[1:], ring, ring[1:]))
    parts.append(f'<path class="s-am" d="{segs}" stroke-width="8" fill="none"/>')
    last = xs[-1]
    parts.append(f'<path class="s-am" d="M{last+30},{ly} L{W-70},{ly}" stroke-width="8" stroke-linecap="round" stroke-dasharray="0.1 16" stroke-opacity="0.55"/>')
    parts.append(f'<path class="s-am" d="M{W-78},{ly-9} L{W-66},{ly} L{W-78},{ly+9}" stroke-opacity="0.55" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    for s in STOPS:
        x = s["x"]
        parts.append(ICONS[s["icon"]](x, ly - 30))
        if s.get("now"):
            parts.append(f'<circle cx="{x}" cy="{ly}" r="40" fill="url(#warm)"/>')
            parts.append(f'<circle class="s-am" cx="{x}" cy="{ly}" r="22" fill="none" stroke-opacity="0.45" stroke-width="2"/>')
            parts.append(f'<circle class="s-am" cx="{x}" cy="{ly}" r="14" fill="none" stroke-width="5"/>')
            parts.append(f'<circle class="f-am" cx="{x}" cy="{ly}" r="6"/>')
        else:
            parts.append(f'<circle class="s-am" cx="{x}" cy="{ly}" r="13" fill="none" stroke-width="5"/>')
        parts.append(f'<text class="school f-ink" x="{x}" y="{ly+64}">{s["school"]}</text>')
        parts.append(f'<text class="degree f-mute" x="{x}" y="{ly+98}">{s["degree"]}</text>')
        parts.append(f'<text class="years f-amt" x="{x}" y="{ly+132}">{s["years"]} <tspan class="f-dim">·</tspan> {s["city"]}</text>')
    css = (
        f".school{{font-family:{SANS};font-weight:600;font-size:29px;text-anchor:middle}}"
        f".degree{{font-family:{SANS};font-weight:400;font-size:21.5px;text-anchor:middle}}"
        f".years{{font-family:{MONO};font-weight:500;font-size:16px;letter-spacing:1.6px;text-anchor:middle}}"
    )
    text_mono = "EDUCATION" + "".join(s["years"] + " · " + s["city"] for s in STOPS)
    fonts = (
        font_face("KT Sans", "Inter-600.ttf", "".join(s["school"] for s in STOPS), 600)
        + font_face("KT Sans", "Inter-400.ttf", "".join(s["degree"] for s in STOPS), 400)
        + font_face("KT Mono", "JetBrainsMono-500.ttf", text_mono, 500)
    )
    desc = "; ".join(f'{s["school"]}, {s["degree"]}, {s["years"]}, {s["city"].title()}' for s in STOPS)
    return section_open(H, "Education", desc, fonts, css) + "".join(parts) + "</svg>\n"


# ---------------------------------------------------------------- research: a map legend
def g_icon(body):
    return f'<g stroke-linecap="round" stroke-linejoin="round" fill="none">{body}</g>'


def icon_urban():
    return (
        '<rect class="s-ln" x="4" y="4" width="56" height="56" rx="6" stroke-width="2.2"/>'
        '<path class="s-ln" d="M4 23 H60 M4 41 H60 M23 4 V60 M42 4 V60" stroke-width="1.6" stroke-opacity="0.7"/>'
        '<rect class="f-am" x="25.5" y="25.5" width="14" height="13" rx="1.5" fill-opacity="0.9"/>'
        '<rect class="f-am" x="6.5" y="43.5" width="14" height="14" rx="1.5" fill-opacity="0.35"/>'
        '<rect class="f-am" x="44.5" y="6.5" width="13" height="14" rx="1.5" fill-opacity="0.55"/>'
    )


def icon_embodied():
    return (
        '<path class="s-ln" d="M32 4 V11" stroke-width="2.2"/><circle class="f-cy" cx="32" cy="3.5" r="2.6"/>'
        '<rect class="s-ln" x="12" y="11" width="40" height="30" rx="11" stroke-width="2.2"/>'
        '<path class="s-cy" d="M19 25 H45" stroke-width="7" stroke-opacity="0.25"/>'
        '<circle class="f-cy" cx="24" cy="25" r="3"/><circle class="f-cy" cx="40" cy="25" r="3"/>'
        '<path class="s-ln" d="M27 41 V46 H37 V41" stroke-width="2.2"/>'
        '<path class="s-ln" d="M10 62 C10 52 18 46 32 46 C46 46 54 52 54 62" stroke-width="2.2"/>'
    )


def icon_robotic_urban():
    wins = "".join(
        f'<rect class="f-am" x="{9+c*9}" y="{12+r*10}" width="4.5" height="5" rx="0.8" fill-opacity="{0.9 if (r+c) % 3 else 0.3}"/>'
        for r in range(4) for c in range(3)
    )
    return (
        '<path class="s-ln" d="M4 60 H62" stroke-width="2.2"/>'
        f'<rect class="s-ln" x="4" y="5" width="34" height="55" rx="2" stroke-width="2.2"/>{wins}'
        '<rect class="s-cy" x="40" y="40" width="20" height="13" rx="4" stroke-width="2.2"/>'
        '<circle class="s-cy" cx="45" cy="57" r="3" stroke-width="2"/><circle class="s-cy" cx="55" cy="57" r="3" stroke-width="2"/>'
        '<path class="s-cy" d="M56 40 V30" stroke-width="1.8"/><path class="f-am" d="M56 30 L62 32.5 L56 35"/>'
    )


def icon_sensing():
    pts = [(44, 14), (50, 20), (56, 12), (48, 30), (58, 28), (52, 38), (60, 44), (46, 48), (54, 54), (40, 40)]
    dots = "".join(
        f'<circle class="{"f-am" if i % 4 == 0 else "f-cy"}" cx="{x}" cy="{y}" r="{1.9 if i % 3 else 2.4}" fill-opacity="{0.95 if i % 2 else 0.6}"/>'
        for i, (x, y) in enumerate(pts)
    )
    return (
        '<circle class="f-cy" cx="10" cy="32" r="5"/>'
        '<path class="s-ln" d="M19 22 A14 14 0 0 1 19 42" stroke-width="2.2"/>'
        '<path class="s-ln" d="M25 15 A23 23 0 0 1 25 49" stroke-width="2.2" stroke-opacity="0.75"/>'
        f'<path class="s-ln" d="M31 8 A32 32 0 0 1 31 56" stroke-width="2.2" stroke-opacity="0.5"/>{dots}'
    )


def icon_twins():
    wins = "".join(f'<rect class="f-am" x="{8+c*8}" y="{18+r*9}" width="4" height="4.5" rx="0.7" fill-opacity="0.85"/>' for r in range(4) for c in range(2))
    return (
        f'<path class="s-ln" d="M4 60 H28 V14 L16 6 L4 14 Z" stroke-width="2.2"/>{wins}'
        '<path class="s-cy" d="M36 60 H60 V14 L48 6 L36 14 Z" stroke-width="2" stroke-dasharray="3 3.5"/>'
        '<path class="s-cy" d="M36 22 H60 M36 31 H60 M36 40 H60 M36 49 H60 M44 14 V60 M52 14 V60" stroke-width="1" stroke-opacity="0.45"/>'
        '<path class="s-ln" d="M27 3 C31 0 33 0 37 3" stroke-width="1.6"/><path class="s-ln" d="M35 1 L37.4 3.2 L34.6 4.4" stroke-width="1.6"/>'
    )


INTERESTS = [
    ("Urban Science", None, icon_urban),
    ("Embodied AI", None, icon_embodied),
    ("Robotic", "Urbanization", icon_robotic_urban),
    ("Multimodal", "Urban Sensing", icon_sensing),
    ("Digital Twins", None, icon_twins),
]

STATEMENT = (
    "I study embodied intelligence in urban systems, with a focus on human-robot interaction,",
    "spatial intelligence, and the urban deployment and governance of robots.",
)


def research():
    H = 420
    dy = 28  # space between the section title and the legend
    parts = [eyebrow("RESEARCH INTERESTS")]
    step = (W - 96) / len(INTERESTS)
    for i, (a, b, icon) in enumerate(INTERESTS):
        cx = 48 + step * (i + 0.5)
        parts.append(f'<circle class="well well-e" cx="{n(cx)}" cy="{116 + dy}" r="50" stroke-width="1.5"/>')
        parts.append(f'<g transform="translate({n(cx)} {116 + dy}) scale(1.18) translate(-32 -32)">{g_icon(icon())}</g>')
        parts.append(f'<text class="num f-dim" x="{n(cx)}" y="{192 + dy}">{i+1:02d}</text>')
        parts.append(f'<text class="label f-ink" x="{n(cx)}" y="{222 + dy}">{a}</text>')
        if b:
            parts.append(f'<text class="label f-ink" x="{n(cx)}" y="{250 + dy}">{b}</text>')
    parts.append(f'<path class="s-am" d="M{W/2-14} {292 + dy}h28" stroke-width="3" stroke-linecap="round" stroke-opacity="0.8"/>')
    for i, line in enumerate(STATEMENT):
        parts.append(f'<text class="statement f-ink" x="{W/2}" y="{338 + dy + i * 38}">{line}</text>')
    css = (
        f".label{{font-family:{SANS};font-weight:600;font-size:23px;text-anchor:middle}}"
        f".num{{font-family:{MONO};font-weight:500;font-size:13px;letter-spacing:2px;text-anchor:middle}}"
        f".statement{{font-family:{SERIF};font-size:30px;fill-opacity:.92;text-anchor:middle}}"
    )
    fonts = (
        font_face("KT Sans", "Inter-600.ttf", "".join(f"{a} {b or ''}" for a, b, _ in INTERESTS), 600)
        + font_face("KT Mono", "JetBrainsMono-500.ttf", "RESEARCH INTERESTS 0123456789", 500)
        + font_face("KT Serif", "InstrumentSerif-Regular.ttf", "".join(STATEMENT))
    )
    desc = "Research interests: " + ", ".join(f"{a} {b}" if b else a for a, b, _ in INTERESTS) + ". " + " ".join(STATEMENT)
    return section_open(H, "Research interests", desc, fonts, css) + "".join(parts) + "</svg>\n"
