"""Footer strip: later that night, the child leads the robot home along the river.
Static apart from three windows that switch off and on at long, step-timed intervals."""
import random

from common import RADIUS, P, n, n1, rect_d

W, H = 1200, 150
BASE = 112  # skyline meets the water
GROUND = 128
FEET = 142

SEED = 311
rng = random.Random(SEED)


COLORS = [(P["warm"], 36), (P["amber"], 28), (P["warmwhite"], 20), (P["orange"], 10), (P["cool"], 6)]


def pick():
    r = rng.uniform(0, 100)
    for c, w in COLORS:
        r -= w
        if r <= 0:
            return c
    return COLORS[0][0]


def skyline():
    blocks, lit, unlit, refl, toggles = [], {}, [], {}, []
    x = -4
    while x < W + 4:
        w = rng.choice([30, 36, 42, 48, 56, 64])
        h = rng.uniform(26, 64)
        if 1030 < x < 1140:
            h = min(h, 34)  # leave the moon's reflection a clear stretch of water
        top = BASE - h
        blocks.append(rect_d(x, top, w, h))
        if rng.random() < 0.3:
            blocks.append(rect_d(x + w * 0.6, top - 6, 6, 6))
        cols = int((w - 6) // 6.6)
        x0 = x + (w - (cols - 1) * 6.6 - 3) / 2
        for r in range(int((h - 6) // 8)):
            yy = top + 5 + r * 8
            for c in range(cols):
                xx = x0 + c * 6.6
                if rng.random() < 0.42:
                    col = pick()
                    o = rng.choice((0.7, 0.85, 1.0))
                    if len(toggles) < 3 and rng.random() < 0.01 and 200 < xx < 1000:
                        toggles.append((rect_d(xx, yy, 3, 3.6), col))
                        continue
                    lit.setdefault((col, o), []).append(rect_d(xx, yy, 3, 3.6))
                    depth = BASE - yy
                    yr = BASE + depth * 0.9
                    if yr < GROUND - 2 and rng.random() < 0.8:
                        ln = rng.uniform(3, 7)
                        refl.setdefault(col, []).append(rect_d(xx + 1.5 - ln / 2 + rng.uniform(-1, 1), yr, ln, 1))
                else:
                    unlit.append(rect_d(xx, yy, 3, 3.6))
        x += w + rng.choice([0, 2, 3, 5])
    s = [f'<path d="{"".join(blocks)}" fill="{P["mid"]}"/>', f'<path d="{"".join(unlit)}" fill="{P["unlit"]}" fill-opacity="0.5"/>']
    for (c, o), rects in sorted(lit.items()):
        s.append(f'<path d="{"".join(rects)}" fill="{c}" fill-opacity="{n(o)}"/>')
    for i, (d, c) in enumerate(toggles):
        s.append(f'<path class="toggle t{i}" d="{d}" fill="{c}"/>')
    water = [f'<rect x="0" y="{BASE}" width="{W}" height="{GROUND-BASE}" fill="url(#water)"/>',
             f'<rect x="0" y="{BASE}" width="{W}" height="1" fill="#FFCF8A" fill-opacity="0.18"/>']
    for c, rects in sorted(refl.items()):
        water.append(f'<path d="{"".join(rects)}" fill="{c}" fill-opacity="0.3"/>')
    # the moon's broken reflection
    water.append(f'<path d="{"".join(rect_d(1086 - l/2, BASE + 3 + i * 2.6, l, 1) for i, l in enumerate((10, 7, 12, 6, 9, 4)))}" fill="#FFF0CF" fill-opacity="0.35"/>')
    return "".join(s), "".join(water)


def limb(points, width, color):
    return f'<path d="M{" L".join(f"{n(x)},{n(y)}" for x, y in points)}" fill="none" stroke="{color}" stroke-width="{n(width)}" stroke-linecap="round" stroke-linejoin="round"/>'


ROBOT_HAND = (11, -30)
CHILD_DX = 24


def robot(c, g=0.0):
    """Side view, walking right; its near hand reaches forward to the child."""
    return "".join([
        limb([(-1, -30), (-4, -16), (-8, -3)], 4.6 + g, c),
        limb([(1, -30), (5, -16), (8, -3)], 4.6 + g, c),
        f'<rect x="{n(-12-g/2)}" y="{n(-4-g/2)}" width="{n(7+g)}" height="{n(4+g)}" rx="1.6" fill="{c}"/>',
        f'<rect x="{n(5.5-g/2)}" y="{n(-4-g/2)}" width="{n(7.5+g)}" height="{n(4+g)}" rx="1.6" fill="{c}"/>',
        f'<rect x="{n(-7-g/2)}" y="{n(-50-g/2)}" width="{n(14+g)}" height="{n(22+g)}" rx="5" fill="{c}"/>',
        f'<rect x="{n(-11-g/2)}" y="{n(-48-g/2)}" width="{n(6+g)}" height="{n(13+g)}" rx="2" fill="{c}"/>',
        limb([(-2, -46), (-7, -36), (-9, -28)], 3.8 + g, c),
        limb([(2, -46), (7, -38), (ROBOT_HAND[0], ROBOT_HAND[1])], 3.8 + g, c),
        f'<rect x="{n(-2.5-g/2)}" y="{n(-54-g/2)}" width="{n(5+g)}" height="{n(5+g)}" fill="{c}"/>',
        f'<ellipse cx="1.5" cy="-60" rx="{n(7+g/2)}" ry="{n(7.6+g/2)}" fill="{c}"/>',
    ])


def child(c, g=0.0):
    hx = ROBOT_HAND[0] - CHILD_DX
    return "".join([
        limb([(0, -15), (-3, -8), (-5, -2)], 3.3 + g, c),
        limb([(1, -15), (4, -8), (6, -2)], 3.3 + g, c),
        f'<rect x="{n(-8-g/2)}" y="{n(-3-g/2)}" width="{n(5+g)}" height="{n(3+g)}" rx="1.2" fill="{c}"/>',
        f'<rect x="{n(4-g/2)}" y="{n(-3-g/2)}" width="{n(5.2+g)}" height="{n(3+g)}" rx="1.2" fill="{c}"/>',
        f'<path d="M-4.5,-27 C-4.5,-29.5 -2.5,-30.5 0,-30.5 C2.5,-30.5 4.5,-29.5 4.5,-27 L5.5,-15 L-5.5,-15 Z" fill="{c}"' + (f' stroke="{c}" stroke-width="{n(g)}" stroke-linejoin="round"' if g else "") + "/>",
        limb([(-1, -27), (-6, -27.5), (hx + 1, ROBOT_HAND[1] + 0.5)], 2.8 + g, c),
        limb([(1.5, -27), (4.5, -22), (6.5, -18)], 2.8 + g, c),
        f'<circle cx="0.5" cy="-35" r="{n(5.6+g/2)}" fill="{c}"/>',
        f'<circle cx="-1.8" cy="-41" r="{n(2.3+g/2)}" fill="{c}"/>',
    ])


def figures(x):
    rim = "#FFC67A"
    near = P["near"]
    cx = x + CHILD_DX
    return (
        f'<ellipse cx="{x+12}" cy="{FEET}" rx="30" ry="2.6" fill="#000" fill-opacity="0.45"/>'
        f'<g filter="url(#soft)" opacity="0.55"><g transform="translate({x},{FEET})">{robot(rim, 1.8)}</g><g transform="translate({cx},{FEET})">{child(rim, 1.6)}</g></g>'
        f'<g transform="translate({x},{FEET})">{robot(near)}'
        f'<rect x="-10.4" y="-46.5" width="4.6" height="10" rx="1.5" fill="#0E1532"/><circle cx="-8.1" cy="-41" r="1" fill="{P["cyan"]}"/>'
        f'<path d="M6.8,-63 C8.8,-61 8.8,-58 6.8,-56" stroke="{P["cyan"]}" stroke-width="1.6" stroke-linecap="round" fill="none"/></g>'
        f'<g transform="translate({cx},{FEET})">{child(near)}'
        f'<rect x="-7.2" y="-27" width="3.6" height="10" rx="1.4" fill="#101838"/><rect x="-7" y="-21" width="3.2" height="1.3" fill="{P["amber"]}"/></g>'
    )


def lamp(x, h=62):
    top = FEET - h
    return (
        f'<circle cx="{x}" cy="{top+4}" r="24" fill="url(#halo)" opacity="0.6"/>'
        f'<path d="M{x-1.1} {top+7}h2.2v{h-7}h-2.2z M{x-3.5} {FEET-5}h7v5h-7z M{x-5.5},{top} L{x+5.5},{top} L{x},{top-4.5} Z" fill="{P["near"]}"/>'
        f'<path d="M{x-4.2},{top+8} L{x+4.2},{top+8} L{x+3},{top} L{x-3},{top} Z" fill="#FFD891"/>'
        f'<ellipse cx="{x}" cy="{FEET+1}" rx="36" ry="4" fill="url(#pool)"/>'
    )


def build():
    global rng
    rng = random.Random(SEED)
    stars = []
    for _ in range(46):
        x, y = rng.uniform(10, W - 10), rng.uniform(8, 70)
        stars.append(f'<circle cx="{n1(x)}" cy="{n1(y)}" r="{rng.choice((0.5, 0.6, 0.8, 1.0))}" fill="#fff" fill-opacity="{n(rng.uniform(.2, .75))}"/>')
    city, water = skyline()
    body = (
        f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
        + "".join(stars)
        + '<circle cx="1086" cy="44" r="46" fill="url(#moonglow)"/><circle cx="1086" cy="44" r="12" fill="#FFF0CF" mask="url(#crescent)"/>'
        + f'<ellipse cx="600" cy="{BASE}" rx="620" ry="70" fill="url(#cityglow)"/>'
        + city
        + water
        + f'<rect x="0" y="{GROUND}" width="{W}" height="{H-GROUND}" fill="url(#deck)"/>'
        + f'<rect x="0" y="{GROUND}" width="{W}" height="1" fill="#FFCF8A" fill-opacity="0.2"/>'
        + lamp(214)
        + lamp(760)
        + figures(470)
    )
    defs = f'''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="{BASE}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#14224E"/><stop offset="0.55" stop-color="#1F2F66"/><stop offset="1" stop-color="#57508E"/></linearGradient>
<radialGradient id="cityglow" cx="0.5" cy="1" r="0.5"><stop offset="0" stop-color="#FF9E57" stop-opacity="0.28"/><stop offset="1" stop-color="#FF9E57" stop-opacity="0"/></radialGradient>
<radialGradient id="moonglow"><stop offset="0" stop-color="#FFE7B8" stop-opacity="0.26"/><stop offset="1" stop-color="#FFE7B8" stop-opacity="0"/></radialGradient>
<linearGradient id="water" x1="0" y1="{BASE}" x2="0" y2="{GROUND}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#3A3A6E"/><stop offset="1" stop-color="#151A38"/></linearGradient>
<linearGradient id="deck" x1="0" y1="{GROUND}" x2="0" y2="{H}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#232A55"/><stop offset="1" stop-color="#161B3C"/></linearGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#FFD58A" stop-opacity="0.8"/><stop offset="1" stop-color="#FFB54D" stop-opacity="0"/></radialGradient>
<radialGradient id="pool"><stop offset="0" stop-color="#FFC26B" stop-opacity="0.25"/><stop offset="1" stop-color="#FFC26B" stop-opacity="0"/></radialGradient>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="0.9"/></filter>
<mask id="crescent"><rect x="1070" y="28" width="32" height="32" fill="#fff"/><circle cx="1093" cy="39" r="11" fill="#000"/></mask>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="{RADIUS}"/></clipPath>'''
    style = (
        "<style>"
        ".toggle{animation:off 12.8s step-end infinite}.t1{animation-duration:16s;animation-delay:-4s}.t2{animation-duration:20s;animation-delay:-9.6s}"
        "@keyframes off{0%{opacity:1}62.5%{opacity:.08}87.5%{opacity:1}}"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
        "</style>"
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">'
        '<title id="t">Later that night, the child leads the robot home along the river.</title>'
        f"{style}<defs>{defs}</defs><g clip-path=\"url(#frame)\">{body}</g></svg>\n"
    )
