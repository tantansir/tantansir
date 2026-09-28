"""Hero banner: a waterfront city at blue hour whose windows light up one by one,
watched from the promenade by a child and a humanoid robot holding hands.
The child points at one lit window; the robot follows the gesture and looks at the same home."""
import math
import random
from collections import defaultdict

from common import P, font_face, n, n1, rect_d, text_width

W, H = 1200, 460
BASE = 372  # skyline meets the water
GROUND = 430  # promenade edge
FEET = 449
FIG_SCALE = 0.96
ROBOT_X = 330

TITLE = "Kaizhen Tan"
SUB = "URBAN SCIENCE × EMBODIED INTELLIGENCE"
HUD = "31.23°N 121.47°E · 40.71°N 74.01°W"
SEAL = "万家灯火"  # 万家灯火, laid out in seal order: right column first

TITLE_X, TITLE_Y, TITLE_SIZE = 66, 158, 108
SUB_Y, SUB_SIZE, SUB_TRACK = 202, 16.5, 3.4

N_DELAY = 24  # switch-on groups for the city lights
SEED = 20260928
rng = random.Random(SEED)
out = []


def add(s):
    out.append(s)


# ---------------------------------------------------------------- lights
WIN_COLORS = [(P["warm"], 34), (P["amber"], 26), (P["warmwhite"], 20), (P["orange"], 10), (P["cool"], 7), (P["tv"], 3)]


def pick_color():
    r = rng.uniform(0, sum(w for _, w in WIN_COLORS))
    for c, w in WIN_COLORS:
        r -= w
        if r <= 0:
            return c
    return WIN_COLORS[0][0]


class Lights:
    """Collects the windows of one layer and writes them as a handful of compact paths.
    Windows sharing a colour, brightness and switch-on delay share one <path>."""

    def __init__(self):
        self.lit = defaultdict(list)
        self.unlit = []
        self.special = []
        self.reflectable = []

    def window(self, x, y, w, h, lit_p, dim=1.0, unlit_o=0.5, reflect=False):
        if rng.random() < lit_p:
            c = pick_color()
            o = round(rng.choice((0.74, 0.87, 1.0)) * dim, 2)
            d = rng.randrange(N_DELAY)
            # a few TVs and lamps that get switched off now and then are already on at dusk
            if c == P["tv"] and rng.random() < 0.7:
                self.special.append(f'<path class="w tv" d="{rect_d(x, y, w, h)}" fill="{c}" fill-opacity="{n(o)}"/>')
            elif rng.random() < 0.03:
                self.special.append(f'<path class="w toggle t{rng.randrange(3)}" d="{rect_d(x, y, w, h)}" fill="{c}" fill-opacity="{n(o)}"/>')
            else:
                self.lit[(c, d, o)].append(rect_d(x, y, w, h))
            if reflect:
                self.reflectable.append((x, y, w, h, c))
        elif unlit_o:
            self.unlit.append(rect_d(x, y, w, h))

    def light(self, x, y, w, h, c, o):
        self.lit[(c, rng.randrange(N_DELAY), o)].append(rect_d(x, y, w, h))

    def flush(self, unlit_o=0.5):
        s = []
        if self.unlit:
            s.append(f'<path d="{"".join(self.unlit)}" fill="{P["unlit"]}" fill-opacity="{n(unlit_o)}"/>')
        for (c, d, o), rects in sorted(self.lit.items()):
            s.append(f'<path class="w d{d}" d="{"".join(rects)}" fill="{c}" fill-opacity="{n(o)}"/>')
        s += self.special
        self.lit.clear()
        self.unlit.clear()
        self.special.clear()
        return "".join(s)


# ---------------------------------------------------------------- defs
def defs():
    return f'''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="{BASE}" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="{P['sky0']}"/><stop offset="0.42" stop-color="{P['sky1']}"/><stop offset="0.74" stop-color="{P['sky2']}"/><stop offset="0.91" stop-color="{P['sky3']}"/><stop offset="1" stop-color="{P['sky4']}"/></linearGradient>
<radialGradient id="cityglow" cx="0.5" cy="1" r="0.5"><stop offset="0" stop-color="#FF9E57" stop-opacity="0.32"/><stop offset="0.55" stop-color="#E0706A" stop-opacity="0.1"/><stop offset="1" stop-color="#E0706A" stop-opacity="0"/></radialGradient>
<radialGradient id="moonglow"><stop offset="0" stop-color="#FFE7B8" stop-opacity="0.3"/><stop offset="1" stop-color="#FFE7B8" stop-opacity="0"/></radialGradient>
<linearGradient id="haze" x1="0" y1="250" x2="0" y2="{BASE}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{P['sky3']}" stop-opacity="0"/><stop offset="1" stop-color="#6A3B4C" stop-opacity="0.55"/></linearGradient>
<linearGradient id="water" x1="0" y1="{BASE}" x2="0" y2="{GROUND}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#1A1834"/><stop offset="0.3" stop-color="#0B0E22"/><stop offset="1" stop-color="#05070F"/></linearGradient>
<linearGradient id="deck" x1="0" y1="{GROUND}" x2="0" y2="{H}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#0C0F1E"/><stop offset="1" stop-color="#03040A"/></linearGradient>
<radialGradient id="pool"><stop offset="0" stop-color="#FFC26B" stop-opacity="0.22"/><stop offset="1" stop-color="#FFC26B" stop-opacity="0"/></radialGradient>
<radialGradient id="shadow"><stop offset="0" stop-color="#000" stop-opacity="0.6"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<radialGradient id="warmhalo"><stop offset="0" stop-color="#FFD58A" stop-opacity="0.85"/><stop offset="0.35" stop-color="#FFB54D" stop-opacity="0.28"/><stop offset="1" stop-color="#FFB54D" stop-opacity="0"/></radialGradient>
<radialGradient id="cyanhalo"><stop offset="0" stop-color="{P['cyan']}" stop-opacity="0.9"/><stop offset="1" stop-color="{P['cyan']}" stop-opacity="0"/></radialGradient>
<radialGradient id="rosehalo"><stop offset="0" stop-color="{P['rose']}" stop-opacity="0.55"/><stop offset="1" stop-color="{P['rose']}" stop-opacity="0"/></radialGradient>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.4"/></filter>
<filter id="stamp" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="2" seed="11" result="noise"/><feColorMatrix in="noise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -4.2 3.35" result="speckle"/><feComposite in="SourceGraphic" in2="speckle" operator="in"/></filter>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<mask id="crescent"><rect x="1040" y="50" width="80" height="80" fill="#fff"/><circle cx="1098" cy="82" r="19" fill="#000"/></mask>'''


# ---------------------------------------------------------------- sky
def stars():
    static, twinkle = [], defaultdict(list)
    for _ in range(130):
        y = 12 + (rng.random() ** 1.7) * 255
        x = rng.uniform(8, W - 8)
        if 40 < x < 640 and 60 < y < 225:  # keep the title block clean
            continue
        r = rng.choice([0.55, 0.6, 0.7, 0.8, 0.9, 1.0, 1.15, 1.35])
        o = max(0.18, min(0.95, (1 - y / 300) * rng.uniform(0.5, 1.1)))
        c = rng.choice(["#FFFFFF", "#FFFFFF", "#DCE8FF", "#FFEFD6"])
        dot = f'<circle cx="{n1(x)}" cy="{n1(y)}" r="{n(r)}" fill="{c}" fill-opacity="{n(o)}"/>'
        if rng.random() < 0.3:
            twinkle[rng.randrange(6)].append(dot)
        else:
            static.append(dot)
    add("<g>" + "".join(static) + "</g>")
    for k, dots in sorted(twinkle.items()):
        add(f'<g class="tw s{k}">' + "".join(dots) + "</g>")


def moon():
    add('<circle cx="1086" cy="90" r="78" fill="url(#moonglow)"/><circle cx="1086" cy="90" r="21" fill="#FFF0CF" mask="url(#crescent)"/>')


# ---------------------------------------------------------------- far layer: landmarks of both cities
FAR = P["far"]


def shanghai_tower(L, cx, h):
    top = BASE - h
    d = (
        f"M{n(cx-27)},{BASE} C{n(cx-26)},{n(BASE-h*0.5)} {n(cx-20)},{n(top+h*0.22)} {n(cx-14)},{n(top+13)} "
        f"L{n(cx-13)},{n(top+9)} L{n(cx+12)},{n(top)} L{n(cx+13)},{n(top+6)} "
        f"C{n(cx+17)},{n(top+h*0.26)} {n(cx+25)},{n(BASE-h*0.5)} {n(cx+26)},{BASE} Z"
    )
    s = [f'<path d="{d}" fill="{FAR}"/>']
    s.append(
        f'<path d="M{n(cx+20)},{BASE-30} C{n(cx+12)},{n(BASE-h*0.45)} {n(cx-4)},{n(top+h*0.45)} {n(cx-12)},{n(top+16)}" '
        f'fill="none" stroke="#A9C6FF" stroke-opacity="0.22" stroke-width="1.1"/>'
    )
    for k in range(8, int(h) - 20, 13):
        half = 26.5 - 12.5 * (k / h) ** 1.3
        if rng.random() < 0.55:
            L.light(cx - half + 3, BASE - k, 2 * half - 6, 1.1, P["cool"], round(rng.uniform(0.18, 0.4), 2))
    return s, (cx, top)


def swfc(L, cx, h):
    top = BASE - h
    hole = f"M{n(cx-7.5)},{n(top+7)} L{n(cx+7.5)},{n(top+7)} L{n(cx+5.5)},{n(top+22)} L{n(cx-5.5)},{n(top+22)} Z"
    s = [
        f'<path d="M{n(cx-21)},{BASE} L{n(cx-10)},{n(top)} L{n(cx+10)},{n(top)} L{n(cx+21)},{BASE} Z {hole}" fill="{FAR}" fill-rule="evenodd"/>',
        f'<path d="{hole}" fill="none" stroke="#9EC3FF" stroke-opacity="0.35" stroke-width="0.9"/>',
    ]
    for k in range(30, int(h) - 30, 11):
        half = 21 - 11 * k / h
        for j in range(int(half * 2 / 5)):
            if rng.random() < 0.16:
                L.light(cx - half + 2 + j * 5, BASE - k, 2, 1.6, P["warmwhite"], 0.6)
    return s, (cx, top)


def jinmao(L, cx, h):
    top = BASE - h
    pts = [(cx - 17, BASE), (cx - 15, BASE - h * 0.55)]
    half, y = 15, BASE - h * 0.55
    for _ in range(9):
        seg = h * 0.28 / 9
        pts += [(cx - half, y - seg * 0.7), (cx - half - 1.2, y - seg * 0.72), (cx - half - 1.2, y - seg)]
        half -= 1.25
        pts.append((cx - half, y - seg))
        y -= seg
    pts += [(cx - half, y - 6), (cx - 3.5, y - 16), (cx - 1, y - 16), (cx - 0.6, top)]
    pts += [(2 * cx - x, yy) for x, yy in reversed(pts)]
    s = [f'<path d="M{" L".join(f"{n(x)},{n(yy)}" for x, yy in pts)} Z" fill="{FAR}"/>']
    s.append(f'<path class="w d{rng.randrange(N_DELAY)}" d="M{n(cx-half)},{n(y-5)} L{n(cx-3.2)},{n(y-15)} L{n(cx+3.2)},{n(y-15)} L{n(cx+half)},{n(y-5)} Z" fill="#FFC870" fill-opacity="0.55"/>')
    for k in range(18, int(h * 0.8), 9):
        hw = 16 - 6 * k / h
        for j in range(int(hw * 2 / 4.5)):
            if rng.random() < 0.18:
                L.light(cx - hw + 1.5 + j * 4.5, BASE - k, 1.8, 1.8, P["warm"], 0.7)
    return s, (cx, top)


def pearl(L, cx, h):
    b = BASE
    s = [
        f'<path d="M{n(cx-24)},{b} L{n(cx-6)},{b-52} L{n(cx-2)},{b-52} L{n(cx-15)},{b} Z M{n(cx+24)},{b} L{n(cx+6)},{b-52} L{n(cx+2)},{b-52} L{n(cx+15)},{b} Z" fill="{FAR}"/>',
        f'<rect x="{n(cx-3)}" y="{b-62}" width="6" height="62" fill="{FAR}"/>',
        f'<rect x="{n(cx-6)}" y="{b-176}" width="12" height="120" fill="{FAR}"/>',
    ]
    s1, s2, s3 = b - 74, b - 146, b - 180
    for cy, r in ((s1, 20), (s2, 12.5), (s3, 5.5)):
        s.append(f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{r}" fill="{FAR}"/>')
    for k in range(5):
        s.append(f'<circle cx="{n(cx)}" cy="{n(b-100-k*8)}" r="2.6" fill="{FAR}"/>')
    s.append(f'<rect x="{n(cx-1.4)}" y="{b-h}" width="2.8" height="{h-180}" fill="{FAR}"/>')
    s.append(f'<circle class="w d{rng.randrange(N_DELAY)}" cx="{n(cx)}" cy="{n(s1)}" r="34" fill="url(#rosehalo)" opacity="0.8"/>')
    s.append(f'<circle class="w d{rng.randrange(N_DELAY)}" cx="{n(cx)}" cy="{n(s2)}" r="22" fill="url(#rosehalo)" opacity="0.7"/>')
    dots = []
    for cy, r, k in ((s1, 20, 14), (s2, 12.5, 10)):
        for i in range(k):
            a = math.pi * (0.12 + 0.76 * i / (k - 1))
            x = cx - math.cos(a) * (r - 2.5)
            y = cy + math.sin(a) * (r - 2.5) * 0.35
            dots.append(f"M{n1(x-0.95)} {n1(y)}a.95 .95 0 1 0 1.9 0a.95 .95 0 1 0 -1.9 0")
    s.append(f'<path class="w d{rng.randrange(N_DELAY)}" d="{"".join(dots)}" fill="#FFC2DA" fill-opacity="0.9"/>')
    return s, (cx, b - h)


def one_wtc(L, cx, h):
    top = BASE - h
    s = [
        f'<path d="M{n(cx-19)},{BASE} L{n(cx-10)},{top} L{n(cx+10)},{top} L{n(cx+19)},{BASE} Z" fill="{FAR}"/>',
        f'<path d="M{n(cx-19)},{BASE} L{n(cx+10)},{top} M{n(cx+19)},{BASE} L{n(cx-10)},{top}" stroke="#A9C6FF" stroke-opacity="0.16" stroke-width="0.9"/>',
        f'<rect x="{n(cx-1.1)}" y="{top-46}" width="2.2" height="46" fill="{FAR}"/>',
        f'<rect x="{n(cx-4)}" y="{top-12}" width="8" height="3" fill="{FAR}"/>',
    ]
    for k in range(10, h - 6, 8):
        hw = 19 - 9 * k / h
        for j in range(int(hw * 2 / 4.2)):
            if rng.random() < 0.13:
                L.light(cx - hw + 1.5 + j * 4.2, BASE - k, 1.8, 1.6, P["cool"], 0.65)
    return s, (cx, top - 46)


def empire(L, cx, h):
    tiers = [(24, 0.24), (19, 0.70), (14, 0.83), (10, 0.89), (7, 0.93), (4.8, 0.965), (3, 1.0)]
    pts, prev = [], BASE
    for hw, f in tiers:
        y = BASE - h * f
        pts += [(cx - hw, prev), (cx - hw, y)]
        prev = y
    pts += [(2 * cx - x, y) for x, y in reversed(pts)]
    top = BASE - h
    s = [f'<path d="M{" L".join(f"{n(x)},{n(y)}" for x, y in pts)} Z" fill="{FAR}"/>', f'<rect x="{n(cx-1)}" y="{n(top-34)}" width="2" height="34" fill="{FAR}"/>']
    L.light(cx - 9.4, BASE - h * 0.885, 18.8, 3, "#FFE3A8", 0.7)
    L.light(cx - 6.5, BASE - h * 0.925, 13, 3, "#FFE3A8", 0.8)
    L.light(cx - 4.2, BASE - h * 0.96, 8.4, 2.6, "#FFF1CF", 0.85)
    for k in range(12, int(h * 0.8), 7):
        hw = 24 if k < h * 0.24 else (19 if k < h * 0.7 else 14)
        for j in range(int(hw * 2 / 4)):
            if rng.random() < 0.2:
                L.light(cx - hw + 1.4 + j * 4, BASE - k, 1.7, 1.7, P["warm"], 0.7)
    return s, (cx, top - 34)


def chrysler(L, cx, h):
    shaft = h * 0.66
    s = [f'<rect x="{n(cx-15)}" y="{n(BASE-shaft)}" width="30" height="{n(shaft)}" fill="{FAR}"/>']
    y = BASE - shaft
    tri = []
    for hw in (13, 10.5, 8.2, 6, 4):
        s.append(f'<path d="M{n(cx-hw)},{n(y)} L{n(cx-hw)},{n(y-10+hw*0.5)} A{n(hw)},{n(hw*0.9)} 0 0 1 {n(cx+hw)},{n(y-10+hw*0.5)} L{n(cx+hw)},{n(y)} Z" fill="{FAR}"/>')
        for j in range(-2, 3):
            if abs(j) * 3 < hw:
                x = cx + j * hw * 0.36
                tri.append(f"M{n1(x-1)} {n1(y-2)}h2l-1 -3.5z")
        y -= 8
    s.append(f'<path class="w d{rng.randrange(N_DELAY)}" d="{"".join(tri)}" fill="#FFF0C8" fill-opacity="0.85"/>')
    s.append(f'<path d="M{n(cx-2.2)},{n(y+2)} L{n(cx)},{n(BASE-h)} L{n(cx+2.2)},{n(y+2)} Z" fill="{FAR}"/>')
    for k in range(10, int(shaft) - 4, 7):
        for j in range(7):
            if rng.random() < 0.17:
                L.light(cx - 13.5 + j * 4, BASE - k, 1.6, 1.7, P["warm"], 0.7)
    return s, (cx, BASE - h)


def generic_far(L, x0, x1, hmin, hmax):
    s = []
    x = x0
    while x < x1:
        w = rng.uniform(16, 38)
        h = rng.uniform(hmin, hmax)
        top = BASE - h
        s.append(rect_d(x, top, w + 0.6, h))
        if rng.random() < 0.25:
            s.append(rect_d(x + w / 2 - 0.6, top - 10, 1.2, 10))
        for yy in range(int(top) + 5, BASE - 3, 6):
            for xx in range(int(x) + 3, int(x + w) - 2, 4):
                if rng.random() < 0.09:
                    L.light(xx, yy, 1.6, 1.6, pick_color(), 0.55)
        x += w + rng.uniform(-3, 5)
    return s


def far_layer():
    L = Lights()
    blocks = generic_far(L, -10, 560, 40, 92) + generic_far(L, 560, 1210, 60, 125)
    add(f'<path d="{"".join(blocks)}" fill="{FAR}"/>')
    beacons = []
    for fn, cx, h in (
        (chrysler, 590, 136),
        (empire, 646, 166),
        (one_wtc, 722, 178),
        (pearl, 826, 206),
        (jinmao, 908, 196),
        (swfc, 958, 214),
        (shanghai_tower, 1022, 256),
    ):
        parts, beacon = fn(L, cx, h)
        add("".join(parts))
        beacons.append(beacon)
    add(L.flush())
    for k in range(3):
        dots = "".join(f'<circle cx="{n(x)}" cy="{n(y-1)}" r="1.6"/>' for i, (x, y) in enumerate(beacons) if i % 3 == k)
        add(f'<g class="beacon b{k}" fill="{P["red"]}">{dots}</g>')
    add(f'<rect x="0" y="250" width="{W}" height="{BASE-250}" fill="url(#haze)"/>')


# ---------------------------------------------------------------- homes: two residential depths
TARGET = {}
TARGET_SPAN = (600, 680)
# keep landmark silhouettes readable: max building height by x range
LOW_ZONES = [(566, 614, 80), (790, 862, 56)]


def cap_height(x, w, h):
    for a, b, m in LOW_ZONES:
        if x < b and x + w > a:
            h = min(h, m)
    return h


def residential(L, x, w, h, kind, spec, target=False):
    top = BASE - h
    k = spec["s"]
    shapes = [rect_d(x, top, w, h)]
    if kind == "tank":
        shapes.append(rect_d(x + w * 0.62, top - 9 * k, 9 * k, 9 * k))
    elif kind == "gable":
        shapes.append(f"M{n1(x-1)} {n1(top)}L{n1(x+w/2)} {n1(top-12*k)}L{n1(x+w+1)} {n1(top)}z")
    elif kind == "antenna":
        shapes.append(rect_d(x + w * 0.3, top - 16 * k, 1.2, 16 * k))
    elif kind == "stair":
        shapes.append(rect_d(x + w * 0.15, top - 8 * k, w * 0.28, 8 * k))
    ww, wh = spec["win"]
    gx, gy = spec["grid"]
    if rng.random() < 0.3:
        ww, gx = ww * 1.5, gx * 1.25
    cols = max(1, int((w - 2 * spec["pad"]) // gx) + 1)
    rows = int((h - spec["pad"] - 4) // gy)
    x_off = x + (w - (cols - 1) * gx - ww) / 2
    lit_p = min(0.9, spec["lit"] * rng.uniform(0.75, 1.2))
    target_cell = (2, cols // 2) if target else None
    balconies = []
    for r in range(rows):
        yy = top + spec["pad"] + r * gy
        if yy + wh > BASE - 2:
            break
        for c in range(cols):
            xx = x_off + c * gx
            if target_cell == (r, c):
                TARGET.update(x=xx, y=yy, w=ww, h=wh)
                continue
            L.window(xx, yy, ww, wh, lit_p, dim=spec["dim"], unlit_o=spec["unlit"], reflect=spec["near"])
        if spec["near"] and kind in ("flat", "tank"):
            balconies.append(rect_d(x + 2, yy + wh + 1.6, w - 4, 0.9))
    return shapes, balconies


BACK = dict(color="#111733", win=(2.4, 3.0), grid=(5.2, 6.6), pad=5, s=0.6, lit=0.5, unlit=0, dim=0.72, near=False)
NEAR = dict(color=P["mid"], win=(4.2, 5.2), grid=(8.4, 10.5), pad=7, s=1.0, lit=0.62, unlit=0.55, dim=1.0, near=True)


def back_residential():
    L = Lights()
    shapes = []
    x = -4
    while x < W + 4:
        w = rng.uniform(22, 46)
        h = rng.uniform(60, 100) if x < 560 else rng.uniform(70, 150)
        h = cap_height(x, w, h)
        sh, _ = residential(L, x, w, h, rng.choice(["flat", "flat", "antenna", "stair"]), BACK)
        shapes += sh
        x += w + rng.uniform(1, 9)
    add(f'<path d="{"".join(shapes)}" fill="{BACK["color"]}"/>')
    add(L.flush())


def near_residential():
    L = Lights()
    shapes, balconies = [], []
    towers = {760: 150, 872: 124, 1090: 146, 1160: 118}
    x = -6
    while x < W + 6:
        w = rng.choice([46, 52, 58, 64, 70, 78, 86])
        h = rng.uniform(40, 86) if x < 560 else rng.uniform(48, 104)
        for tx, th in list(towers.items()):
            if tx - 30 <= x <= tx + 10:
                w, h = rng.choice([40, 44, 48]), th
                del towers[tx]
                break
        target = False
        if TARGET_SPAN[0] <= x + w / 2 <= TARGET_SPAN[1] and not TARGET:
            target, h, w = True, 104, 70
        h = cap_height(x, w, h)
        sh, bal = residential(L, x, w, h, rng.choice(["flat", "tank", "gable", "antenna", "stair", "flat"]), NEAR, target)
        shapes += sh
        balconies += bal
        x += w + rng.choice([0, 2, 4, 6, 10])
    add(f'<path d="{"".join(shapes)}" fill="{NEAR["color"]}"/>')
    add(f'<path d="{"".join(balconies)}" fill="#2A3158" fill-opacity="0.8"/>')
    add(L.flush(NEAR["unlit"]))
    return L.reflectable


# ---------------------------------------------------------------- water
def water(reflectable):
    add(f'<rect x="0" y="{BASE}" width="{W}" height="{GROUND-BASE}" fill="url(#water)"/>')
    add(f'<rect x="0" y="{BASE}" width="{W}" height="1.2" fill="#FFCF8A" fill-opacity="0.2"/>')
    buckets = defaultdict(list)
    for x, y, w, h, c in reflectable:
        depth = BASE - (y + h / 2)
        yr = BASE + depth * 0.92
        if yr > GROUND - 3:
            continue
        spread = 2 + depth * 0.06
        for _ in range(rng.randint(2, 4)):
            yy = yr + rng.uniform(-spread, spread)
            if not (BASE + 2 < yy < GROUND - 2):
                continue
            ln = w * rng.uniform(0.8, 2.2)
            fade = 1 - (yy - BASE) / (GROUND - BASE) * 0.65
            o = round(rng.choice((0.2, 0.32, 0.45)) * fade, 1) or 0.1
            cls = f"sh h{rng.randrange(4)}" if rng.random() < 0.45 else ""
            buckets[(c, o, cls)].append(rect_d(x + w / 2 - ln / 2 + rng.uniform(-1.5, 1.5), yy, ln, 1.2))
    g = ['<g class="refl">']
    by_cls = defaultdict(list)
    for (c, o, cls), rects in sorted(buckets.items()):
        by_cls[cls].append(f'<path d="{"".join(rects)}" fill="{c}" fill-opacity="{n(o)}"/>')
    for cls, paths in sorted(by_cls.items()):
        g.append((f'<g class="{cls}">' if cls else "<g>") + "".join(paths) + "</g>")
    ripples = [rect_d(rng.uniform(-50, W), rng.uniform(BASE + 4, GROUND - 3), rng.uniform(60, 220), 0.8) for _ in range(16)]
    g.append(f'<path d="{"".join(ripples)}" fill="#B8C6F0" fill-opacity="0.06"/>')
    g.append("</g>")
    add("".join(g))


def boat():
    y = BASE
    lights = "".join(rect_d(15 + i * 6, y + 19.5, 3.2, 3.2) for i in range(8))
    upper = "".join(rect_d(25 + i * 6.5, y + 12.5, 3, 2.6) for i in range(4))
    refl = "".join(rect_d(13 + i * 6, y + 36 + (i % 3) * 2.4, rng.uniform(4, 8), 1.2) for i in range(8))
    add(
        '<g transform="translate(724 0)">'
        f'<path d="M0,{y+26} L78,{y+26} L70,{y+33} L6,{y+33} Z M12 {y+17}h52v9h-52z M22 {y+11}h30v6h-30z" fill="{P["near"]}"/>'
        f'<path d="{lights}" fill="{P["warm"]}" fill-opacity="0.95"/>'
        f'<path d="{upper}" fill="{P["warmwhite"]}" fill-opacity="0.9"/>'
        f'<circle cx="37" cy="{y+9}" r="1.4" fill="{P["red"]}"/>'
        f'<path d="{refl}" fill="{P["warm"]}" fill-opacity="0.3"/>'
        "</g>"
    )


# ---------------------------------------------------------------- promenade
def promenade():
    add(f'<rect x="0" y="{GROUND}" width="{W}" height="{H-GROUND}" fill="url(#deck)"/>')
    add(f'<rect x="0" y="{GROUND}" width="{W}" height="1.2" fill="#FFCF8A" fill-opacity="0.22"/>')
    for x in (96, 1128):
        add(f'<ellipse cx="{x}" cy="{FEET+2}" rx="70" ry="9" fill="url(#pool)"/>')


def lamp(x, h=150):
    top = FEET - h
    add(
        f'<g class="lamp"><circle cx="{x}" cy="{top+7}" r="46" fill="url(#warmhalo)" opacity="0.55"/>'
        f'<path d="M{x-1.6} {top+12}h3.2v{h-12}h-3.2z M{x-5} {FEET-10}h10v10h-10z M{x-9},{top} L{x+9},{top} L{x},{top-7} Z M{x-8} {top+13}h16v2.4h-16z" fill="{P["near"]}"/>'
        f'<path d="M{x-7},{top+14} L{x+7},{top+14} L{x+5},{top} L{x-5},{top} Z" fill="#FFD891"/></g>'
    )


# ---------------------------------------------------------------- the two figures
def limb(points, width, color):
    d = "M" + " L".join(f"{n(x)},{n(y)}" for x, y in points)
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{n(width)}" stroke-linecap="round" stroke-linejoin="round"/>'


ROBOT_HAND = (41.5, -61)


def robot_shapes(c, g=0.0):
    """Humanoid robot from behind, head turned toward the window the child points at.
    Local origin between the feet; g inflates every shape for the rim light."""
    s = [
        limb([(-8.5, -80), (-9.5, -44)], 12.5 + g, c),
        limb([(-9.5, -44), (-9.8, -8)], 9.5 + g, c),
        limb([(8.5, -80), (9.5, -44)], 12.5 + g, c),
        limb([(9.5, -44), (9.8, -8)], 9.5 + g, c),
        f'<rect x="{n(-17-g/2)}" y="{n(-8-g/2)}" width="{n(14+g)}" height="{n(8+g)}" rx="3" fill="{c}"/>',
        f'<rect x="{n(3-g/2)}" y="{n(-8-g/2)}" width="{n(14+g)}" height="{n(8+g)}" rx="3" fill="{c}"/>',
        f'<rect x="{n(-15-g/2)}" y="{n(-91-g/2)}" width="{n(30+g)}" height="{n(17+g)}" rx="6" fill="{c}"/>',
        f'<path d="M-24,-126 C-24,-132 -19,-135 -12,-135 L12,-135 C19,-135 24,-132 24,-126 L20,-104 C18,-96 15,-91 12,-88 '
        f'L-12,-88 C-15,-91 -18,-96 -20,-104 Z" fill="{c}"' + (f' stroke="{c}" stroke-width="{n(g)}" stroke-linejoin="round"' if g else "") + "/>",
        limb([(-24, -124), (-28, -97)], 10 + g, c),
        limb([(-28, -97), (-29, -70)], 8.5 + g, c),
        limb([(24, -124), (31, -97)], 10 + g, c),
        limb([(31, -97), (40, -66)], 8.5 + g, c),
        f'<circle cx="-29.5" cy="-65" r="{n(5+g/2)}" fill="{c}"/>',
        f'<circle cx="{ROBOT_HAND[0]}" cy="{ROBOT_HAND[1]}" r="{n(5.2+g/2)}" fill="{c}"/>',
        f'<circle cx="-24" cy="-124" r="{n(8.5+g/2)}" fill="{c}"/>',
        f'<circle cx="24" cy="-124" r="{n(8.5+g/2)}" fill="{c}"/>',
        f'<rect x="{n(-4.5-g/2)}" y="{n(-141-g/2)}" width="{n(9+g)}" height="{n(9+g)}" fill="{c}"/>',
        f'<ellipse cx="2" cy="-154" rx="{n(13.5+g/2)}" ry="{n(15.5+g/2)}" transform="rotate(9 2 -154)" fill="{c}"/>',
    ]
    return s


def robot_details():
    ln = "#3B4A78"
    return [
        f'<path d="M0,-133 L0,-92 M-17,-114 C-8,-110 8,-110 17,-114 M-10.5,-160 C-4,-163 6,-163 13,-158" stroke="{ln}" stroke-width="0.9" fill="none" opacity="0.8"/>',
        f'<path d="M-6.2,-44a3.1 3.1 0 1 0 6.2 0a3.1 3.1 0 1 0 -6.2 0 M6.3,-44a3.1 3.1 0 1 0 6.2 0a3.1 3.1 0 1 0 -6.2 0 '
        f'M-28.4,-124a4.4 4.4 0 1 0 8.8 0a4.4 4.4 0 1 0 -8.8 0 M19.6,-124a4.4 4.4 0 1 0 8.8 0a4.4 4.4 0 1 0 -8.8 0" stroke="{ln}" stroke-width="0.9" fill="none"/>',
        f'<rect x="-9" y="-129" width="18" height="21" rx="4" fill="#0E1532" stroke="{ln}" stroke-width="0.9"/>',
        f'<circle class="led" cx="0" cy="-113" r="1.8" fill="{P["cyan"]}"/>',
        f'<path d="M13.5,-162 C17.2,-156 17,-148 13,-142" stroke="{P["cyan"]}" stroke-width="2.2" stroke-linecap="round" fill="none"/>',
        '<circle cx="15.5" cy="-153" r="9" fill="url(#cyanhalo)" opacity="0.55"/>',
    ]


def child_shapes(c, hand, aim, g=0.0):
    """Child from behind. `hand` is where the robot's hand is (child-local);
    `aim` is the pointing direction in radians (screen coordinates)."""
    hx, hy = hand
    sx, sy = 10, -67
    ex, ey = sx + 13 * math.cos(aim + 0.14), sy + 13 * math.sin(aim + 0.14)
    px, py = ex + 12 * math.cos(aim - 0.02), ey + 12 * math.sin(aim - 0.02)
    fx, fy = px + 6.5 * math.cos(aim), py + 6.5 * math.sin(aim)
    s = [
        limb([(-4.6, -40), (-4.8, -6)], 7.4 + g, c),
        limb([(4.6, -40), (4.8, -6)], 7.4 + g, c),
        f'<rect x="{n(-10-g/2)}" y="{n(-7-g/2)}" width="{n(10+g)}" height="{n(7+g)}" rx="3" fill="{c}"/>',
        f'<rect x="{n(0.2-g/2)}" y="{n(-7-g/2)}" width="{n(10+g)}" height="{n(7+g)}" rx="3" fill="{c}"/>',
        f'<path d="M-12,-66 C-12,-71 -8,-73 -4,-73 L4,-73 C8,-73 12,-71 12,-66 L15,-40 C15,-38 14,-37 12,-37 '
        f'L-12,-37 C-14,-37 -15,-38 -15,-40 Z" fill="{c}"' + (f' stroke="{c}" stroke-width="{n(g)}" stroke-linejoin="round"' if g else "") + "/>",
        limb([(-10, -66), ((-10 + hx) / 2 - 1, (-66 + hy) / 2 + 2.5), (hx + 1.5, hy)], 6.2 + g, c),
        limb([(sx, sy), (ex, ey), (px, py)], 6.2 + g, c),
        limb([(px, py), (fx, fy)], 2.6 + g, c),
        f'<circle cx="{n(px)}" cy="{n(py)}" r="{n(3.6+g/2)}" fill="{c}"/>',
        f'<circle cx="0" cy="-84" r="{n(11.5+g/2)}" fill="{c}"/>',
        f'<circle cx="-1" cy="-97.5" r="{n(4.6+g/2)}" fill="{c}"/>',
    ]
    return s, (fx, fy)


def child_details():
    ln = "#3B4A78"
    return [
        f'<rect x="-9" y="-68" width="18" height="24" rx="5" fill="#101838" stroke="{ln}" stroke-width="0.9"/>',
        f'<path d="M-6,-60 L6,-60 M-8.5,-89 C-4,-93 3,-93 8,-90" stroke="{ln}" stroke-width="0.85" fill="none"/>',
        f'<rect x="-4" y="-53" width="8" height="2.2" rx="1" fill="{P["amber"]}" fill-opacity="0.85"/>',
    ]


def figures_and_attention():
    s = FIG_SCALE
    child_x = ROBOT_X + 70 * s
    tx = TARGET["x"] + TARGET["w"] / 2
    ty = TARGET["y"] + TARGET["h"] / 2
    # the robot's hand in the child's local frame, so the two hands always meet
    hand = ((ROBOT_X + ROBOT_HAND[0] * s - child_x) / s, ROBOT_HAND[1])
    shoulder = (child_x + 10 * s, FEET - 67 * s)
    aim = math.atan2(ty - shoulder[1], tx - shoulder[0])
    _, (fx, fy) = child_shapes("#000", hand, aim)
    finger = (child_x + fx * s, FEET + fy * s)
    visor = (ROBOT_X + 17 * s, FEET - 152 * s)

    # attention: warm line from the child's finger, cyan from the robot's eyes, meeting at one home
    add(f'<linearGradient id="gh" gradientUnits="userSpaceOnUse" x1="{n(finger[0])}" y1="{n(finger[1])}" x2="{n(tx)}" y2="{n(ty)}"><stop offset="0" stop-color="{P["amber"]}" stop-opacity="0.95"/><stop offset="1" stop-color="{P["amber"]}" stop-opacity="0.35"/></linearGradient>')
    add(f'<linearGradient id="gr" gradientUnits="userSpaceOnUse" x1="{n(visor[0])}" y1="{n(visor[1])}" x2="{n(tx)}" y2="{n(ty)}"><stop offset="0" stop-color="{P["cyan"]}" stop-opacity="0.95"/><stop offset="1" stop-color="{P["cyan"]}" stop-opacity="0.3"/></linearGradient>')
    add('<g class="attn">')
    add(f'<circle class="home-glow" cx="{n(tx)}" cy="{n(ty)}" r="16" fill="url(#warmhalo)"/>')
    add(f'<rect class="home" x="{n(TARGET["x"]-0.4)}" y="{n(TARGET["y"]-0.4)}" width="{n(TARGET["w"]+0.8)}" height="{n(TARGET["h"]+0.8)}" fill="#FFE2A0"/>')
    add(f'<path class="ray ray-h" d="M{n(finger[0]+2)},{n(finger[1]-1)} L{n(tx-4)},{n(ty+1.5)}" stroke="url(#gh)" stroke-width="1.25" stroke-dasharray="1.5 5" stroke-linecap="round"/>')
    add(f'<path class="ray ray-r" d="M{n(visor[0]+2)},{n(visor[1])} L{n(tx-4)},{n(ty)}" stroke="url(#gr)" stroke-width="1.25" stroke-dasharray="1.5 5" stroke-linecap="round"/>')
    add("</g>")

    rim = "#FFC67A"
    rt = f"translate({ROBOT_X},{FEET}) scale({s})"
    ct = f"translate({n(child_x)},{FEET}) scale({s})"
    add('<g class="figures">')
    add(f'<ellipse cx="{n(ROBOT_X+16)}" cy="{FEET}" rx="64" ry="5" fill="url(#shadow)"/>')
    rim_child, _ = child_shapes(rim, hand, aim, 2.4)
    add(f'<g filter="url(#soft)" opacity="0.6"><g transform="{rt}">{"".join(robot_shapes(rim, 2.6))}</g><g transform="{ct}">{"".join(rim_child)}</g></g>')
    body_child, _ = child_shapes(P["near"], hand, aim)
    add(f'<g transform="{rt}">{"".join(robot_shapes(P["near"]))}{"".join(robot_details())}</g>')
    add(f'<g transform="{ct}">{"".join(body_child)}{"".join(child_details())}</g>')
    add("</g>")


# ---------------------------------------------------------------- type
def title_block():
    tw = text_width("InstrumentSerif-Regular.ttf", TITLE, TITLE_SIZE)
    add(f'<text class="name" x="{TITLE_X}" y="{TITLE_Y}">{TITLE}</text>')
    a, b = SUB.split(" × ")
    add(f'<text class="sub" x="{TITLE_X+3}" y="{SUB_Y}">{a} <tspan class="x">×</tspan> {b}</text>')
    sx, sy, sz = TITLE_X + tw + 26, TITLE_Y - 76, 54
    t = [(0.735, 0.455), (0.735, 0.87), (0.265, 0.455), (0.265, 0.87)]
    chars = "".join(f'<text class="seal-t" x="{n(sz*u)}" y="{n(sz*v)}">{ch}</text>' for ch, (u, v) in zip(SEAL, t))
    add(
        f'<g class="seal" transform="translate({n(sx)},{n(sy)})" filter="url(#stamp)">'
        f'<rect width="{sz}" height="{sz}" rx="5" fill="{P["seal"]}"/>'
        f'<rect x="3.5" y="3.5" width="{sz-7}" height="{sz-7}" rx="2.5" fill="none" stroke="#FBEBDD" stroke-width="1.3"/>{chars}</g>'
    )


def hud():
    k, i = 16, 22
    corners = "".join(
        f"M{x},{y+dy*k} L{x},{y} L{x+dx*k},{y} "
        for x, y, dx, dy in ((i, i, 1, 1), (W - i, i, -1, 1), (i, H - i, 1, -1), (W - i, H - i, -1, -1))
    )
    add(f'<path d="{corners}" stroke="#8FA9D6" stroke-opacity="0.45" stroke-width="1.4" fill="none"/>')
    add(f'<text class="hud-t" x="{W-40}" y="44" text-anchor="end">{HUD}</text>')


def style(fonts):
    # Browsers re-rasterise the whole image whenever an animated value changes, so nothing
    # here is eased. Intro: windows switch on along a 0.2 s grid (real lamps pop on, with one
    # flicker). Idle loop: step-timed keyframes that all land on multiples of 0.8 s, so the
    # banner repaints about once per 0.8 s instead of 60 times a second.
    delays = "".join(f".d{i}{{animation-delay:{n(0.4 + 0.2 * i)}s}}" for i in range(N_DELAY))
    return f"""<style>{fonts}
.name{{font-family:'KT Serif','Iowan Old Style','Palatino Linotype',Georgia,serif;font-size:{TITLE_SIZE}px;fill:{P['ink']};letter-spacing:.5px}}
.sub{{font-family:'KT Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:{SUB_SIZE}px;font-weight:500;letter-spacing:{SUB_TRACK}px;fill:{P['mute']}}}
.sub .x{{fill:{P['amber']}}}
.hud-t{{font-family:'KT Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12.5px;font-weight:500;letter-spacing:1.4px;fill:#8FA9D6;fill-opacity:.7}}
.seal-t{{font-family:'KT Seal','Songti SC','STSong','SimSun','Noto Serif CJK SC',serif;font-weight:900;font-size:21px;fill:#FBEBDD;text-anchor:middle}}
.w{{animation:lit .6s step-end backwards}}{delays}
@keyframes lit{{0%{{opacity:.08}}33.3%{{opacity:1}}66.6%{{opacity:.45}}}}
.tv{{animation:lit .6s step-end backwards,tv 3.2s step-end 6.4s infinite}}
@keyframes tv{{0%{{opacity:1}}25%{{opacity:.5}}50%{{opacity:.85}}75%{{opacity:.6}}}}
.toggle.t0{{animation:lit .6s step-end backwards,off 12.8s step-end 7.2s infinite}}
.toggle.t1{{animation:lit .6s step-end backwards,off 16s step-end 8.8s infinite}}
.toggle.t2{{animation:lit .6s step-end backwards,off 20s step-end 10.4s infinite}}
@keyframes off{{0%{{opacity:1}}62.5%{{opacity:.06}}87.5%{{opacity:1}}}}
.tw{{animation:tw 6.4s step-end infinite}}.s1{{animation-delay:-.8s}}.s2{{animation-delay:-2.4s}}.s3{{animation-delay:-4s}}.s4{{animation-delay:-4.8s}}.s5{{animation-delay:-5.6s}}
@keyframes tw{{0%{{opacity:1}}25%{{opacity:.3}}37.5%{{opacity:1}}75%{{opacity:.55}}87.5%{{opacity:1}}}}
.beacon{{animation:blink 3.2s step-end infinite}}.b1{{animation-delay:-1.6s}}.b2{{animation-delay:-.8s}}
@keyframes blink{{0%{{opacity:.15}}75%{{opacity:1}}}}
.refl{{animation:fadein 4s steps(5,end) .8s backwards}}.lamp{{animation:fadein .6s steps(3,end) .2s backwards}}
@keyframes fadein{{0%{{opacity:.1}}100%{{opacity:1}}}}
.sh{{animation:sh 3.2s step-end infinite}}.h1{{animation-delay:-.8s}}.h2{{animation-delay:-1.6s}}.h3{{animation-delay:-2.4s}}
@keyframes sh{{0%{{opacity:1;transform:translateX(0)}}50%{{opacity:.45;transform:translateX(2px)}}}}
.led{{animation:led 1.6s step-end infinite}}
@keyframes led{{0%{{opacity:1}}50%{{opacity:.25}}}}
.home{{animation:fadein .8s steps(2,end) 5.6s backwards}}
.home-glow{{animation:fadein .8s steps(2,end) 6.4s backwards,breathe 4.8s step-end 7.2s infinite}}
@keyframes breathe{{0%{{opacity:1}}50%{{opacity:.6}}}}
.ray{{fill:none;opacity:.8;animation:ray .8s steps(2,end) backwards,march 1.6s step-end infinite}}
.ray-h{{animation-delay:5.6s,6.4s}}.ray-r{{animation-delay:6.4s,7.2s}}
@keyframes ray{{0%{{opacity:0}}100%{{opacity:.8}}}}
@keyframes march{{0%{{stroke-dashoffset:0}}50%{{stroke-dashoffset:-3.25}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>"""


def build():
    global rng
    rng = random.Random(SEED)
    out.clear()
    TARGET.clear()
    add(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
    stars()
    moon()
    add(f'<ellipse cx="760" cy="{BASE}" rx="760" ry="220" fill="url(#cityglow)"/>')
    far_layer()
    back_residential()
    reflectable = near_residential()
    water(reflectable)
    boat()
    promenade()
    lamp(96)
    lamp(1128)
    figures_and_attention()
    title_block()
    hud()
    fonts = "".join(
        [
            font_face("KT Serif", "InstrumentSerif-Regular.ttf", TITLE),
            font_face("KT Mono", "JetBrainsMono-500.ttf", SUB + HUD, 500),
            font_face("KT Seal", "NotoSerifSC-900.ttf", SEAL, 900),
        ]
    )
    head = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">'
        f"<title id=\"t\">Kaizhen Tan: Urban Science × Embodied Intelligence</title>"
        f'<desc id="d">A waterfront city at dusk. Windows light up across Shanghai and New York landmarks while a child and a humanoid robot, holding hands on the promenade, look at the same lit window.</desc>'
        + style(fonts)
        + f"<defs>{defs()}</defs>"
        + '<g clip-path="url(#frame)">'
    )
    return head + "".join(out) + "</g></svg>\n"
