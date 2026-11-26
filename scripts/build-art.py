#!/usr/bin/env python3
"""Builds the static README art in assets/ (banner, terminal, divider).

Theme = the homelab "404 // Signal Lost" page: neon cyan / magenta / green on near-black,
perspective grid, scanlines, glitch title, typing terminal.
Fonts are tiny Google Fonts subsets (OFL) embedded as base64, because GitHub serves README
SVGs as <img>, which cannot load external fonts.

Usage: python3 scripts/build-art.py <fonts-dir>   (orbitron.woff2, rajdhani.woff2, mono.woff2)
"""
import base64
import random
import sys
from pathlib import Path

FONTS = Path(sys.argv[1] if len(sys.argv) > 1 else "fonts")
OUT = Path("assets")
OUT.mkdir(exist_ok=True)

BG, CYAN, MAGENTA, GREEN, TEXT = "#030712", "#00f0ff", "#ff00c8", "#00ff9f", "#d7f7ff"


def font(name, family):
    b64 = base64.b64encode((FONTS / name).read_bytes()).decode()
    return f"@font-face{{font-family:'{family}';src:url(data:font/woff2;base64,{b64}) format('woff2');}}"


REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}.cover{display:none}}"

# ---------------------------------------------------------------- banner
W, H = 1200, 320
HORIZON, VX = 222, W / 2
rnd = random.Random(404)

grid = []
for i in range(-14, 15):  # rays to the vanishing point
    x = VX + i * 95
    grid.append(f'<line x1="{VX + (x - VX) * 0.08:.1f}" y1="{HORIZON}" x2="{x:.1f}" y2="{H}"/>')
for k in range(1, 9):  # receding horizontals
    y = HORIZON + (H - HORIZON) * (k / 8) ** 2
    grid.append(f'<line x1="0" y1="{y:.1f}" x2="{W}" y2="{y:.1f}"/>')

particles = []
for i in range(28):
    x, d, delay = rnd.uniform(20, W - 20), rnd.uniform(6, 14), rnd.uniform(0, 12)
    c = rnd.choice([CYAN, CYAN, CYAN, GREEN, MAGENTA])
    particles.append(
        f'<circle class="p" cx="{x:.0f}" cy="{H}" r="{rnd.uniform(0.8, 1.8):.1f}" fill="{c}" '
        f'style="animation-duration:{d:.1f}s;animation-delay:-{delay:.1f}s"/>'
    )

banner = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
<title id="t">merlinlcb: Lehi Bennett, Systems Administrator</title>
<style>
{font("orbitron.woff2", "Orbitron")}
{font("rajdhani.woff2", "Rajdhani")}
.title{{font:900 112px Orbitron,'Segoe UI',Verdana,sans-serif;letter-spacing:6px}}
.sub{{font:700 27px Rajdhani,'Segoe UI',sans-serif;letter-spacing:9px;fill:#9aefff;animation:flick 4s infinite}}
.tags{{font:700 17px Rajdhani,'Segoe UI',sans-serif;letter-spacing:5px;fill:{TEXT};opacity:.6}}
.g1{{animation:gl1 5s infinite steps(1)}} .g2{{animation:gl2 5s infinite steps(1)}} .main{{animation:pulse 3s ease-in-out infinite;transform-origin:center;transform-box:fill-box}}
.p{{animation-name:rise;animation-timing-function:linear;animation-iteration-count:infinite}}
.grid{{animation:gridfade 6s ease-in-out infinite}}
@keyframes rise{{from{{transform:translateY(0);opacity:0}}10%{{opacity:1}}to{{transform:translateY(-{H + 20}px);opacity:0}}}}
@keyframes flick{{0%,18%,22%,25%,53%,57%,100%{{opacity:1}}20%,24%,55%{{opacity:.3}}}}
@keyframes pulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.012)}}}}
@keyframes gl1{{0%,100%{{transform:translate(4px,-3px)}}91%{{transform:translate(-9px,2px)}}93%{{transform:translate(7px,-5px)}}95%{{transform:translate(4px,-3px)}}}}
@keyframes gl2{{0%,100%{{transform:translate(-4px,3px)}}91%{{transform:translate(10px,-1px)}}93%{{transform:translate(-8px,4px)}}95%{{transform:translate(-4px,3px)}}}}
@keyframes gridfade{{0%,100%{{opacity:.45}}50%{{opacity:.75}}}}
{REDUCED}
</style>
<defs>
  <radialGradient id="bg" cx="50%" cy="45%" r="75%"><stop offset="0" stop-color="#08111f"/><stop offset=".6" stop-color="#02040a"/><stop offset="1" stop-color="#000"/></radialGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="1"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
  <pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#fff" fill-opacity=".025"/></pattern>
  <filter id="glow" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="soft"><feGaussianBlur stdDeviation="1.6"/></filter>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <g class="grid" stroke="{CYAN}" stroke-opacity=".22" stroke-width="1">{"".join(grid)}</g>
  <rect y="{HORIZON - 2}" width="{W}" height="46" fill="url(#fade)" opacity=".85"/>
  <line x1="0" y1="{HORIZON}" x2="{W}" y2="{HORIZON}" stroke="{MAGENTA}" stroke-opacity=".55" filter="url(#soft)"/>
  <g filter="url(#soft)">{"".join(particles)}</g>
  <g text-anchor="middle">
    <text class="title g1" x="{VX}" y="128" fill="{MAGENTA}" opacity=".7">MERLINLCB</text>
    <text class="title g2" x="{VX}" y="128" fill="{GREEN}" opacity=".7">MERLINLCB</text>
    <text class="title main" x="{VX}" y="128" fill="{CYAN}" filter="url(#glow)">MERLINLCB</text>
    <text class="sub" x="{VX}" y="176">LEHI BENNETT // SYSTEMS ADMINISTRATOR</text>
    <text class="tags" x="{VX}" y="207">IT PROFESSIONAL · UI/UX DEVELOPER · 10 CERTIFICATIONS · 11+ YEARS</text>
  </g>
  <rect width="{W}" height="{H}" fill="url(#scan)"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{CYAN}" stroke-opacity=".35"/>
</svg>
"""
(OUT / "banner.svg").write_text(banner)

# ---------------------------------------------------------------- terminal
lines = [
    ("cmd", "whoami"),
    ("out", "lehi bennett — systems administrator · it professional · ui/ux developer"),
    ("cmd", "cat ~/.mission"),
    ("out", "I keep systems running, identities secure, and users happy,"),
    ("out", "and I build the tools that automate the rest."),
    ("cmd", "uptime"),
    ("out", "11+ years in IT · 10 industry certifications · eagle scout"),
]
TW, LH, TOP, LEFT, CH = 1000, 32, 74, 34, 9.9  # CH ≈ Share Tech Mono advance at 18px
TH = TOP + LH * len(lines) + 40
rows, t = [], 0.4
for i, (kind, s) in enumerate(lines):
    y = TOP + i * LH
    if kind == "cmd":
        text = f'<tspan fill="{GREEN}">merlin@lcb</tspan><tspan fill="{TEXT}" fill-opacity=".5">:</tspan><tspan fill="{CYAN}">~</tspan><tspan fill="{TEXT}" fill-opacity=".5">$ </tspan><tspan fill="{TEXT}">{s}</tspan>'
        n, dur = len("merlin@lcb:~$ ") + len(s), 0.06 * len(s) + 0.2
    else:
        text = f'<tspan fill="#89ffca">{s}</tspan>'
        n, dur = len(s), 0.5
    width = n * CH + 12
    rows.append(f'<text x="{LEFT}" y="{y}">{text}</text>')
    rows.append(
        f'<rect class="cover" x="{LEFT - 2}" y="{y - 22}" width="{width:.0f}" height="30" fill="#050a14" '
        f'style="animation:reveal {dur:.2f}s steps({max(n, 8)}) {t:.2f}s forwards"/>'
    )
    t += dur + (0.35 if kind == "cmd" else 0.15)
cy = TOP + len(lines) * LH
prompt_w = len("merlin@lcb:~$ ") * CH
rows.append(
    f'<g class="last" style="animation:show 0s {t:.2f}s forwards"><text x="{LEFT}" y="{cy}"><tspan fill="{GREEN}">merlin@lcb</tspan>'
    f'<tspan fill="{TEXT}" fill-opacity=".5">:</tspan><tspan fill="{CYAN}">~</tspan><tspan fill="{TEXT}" fill-opacity=".5">$ </tspan></text>'
    f'<rect class="cur" x="{LEFT + prompt_w:.0f}" y="{cy - 17}" width="10" height="20" fill="{GREEN}"/></g>'
)

terminal = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{TH}" viewBox="0 0 {TW} {TH}" role="img" aria-labelledby="t">
<title id="t">whoami: Lehi Bennett, systems administrator. I keep systems running, identities secure, and users happy, and I build the tools that automate the rest.</title>
<style>
{font("mono.woff2", "STM")}
text{{font:18px STM,'Cascadia Mono',Consolas,'DejaVu Sans Mono',monospace;white-space:pre}}
.cover{{transform-box:fill-box;transform-origin:right center}}
.last{{opacity:0}} .cur{{animation:blink 1s steps(1) infinite}}
@keyframes reveal{{to{{transform:scaleX(0)}}}}
@keyframes show{{to{{opacity:1}}}}
@keyframes blink{{50%{{opacity:0}}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}.cover{{display:none}}.last{{opacity:1}}}}
</style>
<defs><pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#fff" fill-opacity=".02"/></pattern></defs>
<rect x=".5" y=".5" width="{TW - 1}" height="{TH - 1}" rx="18" fill="#050a14" stroke="{CYAN}" stroke-opacity=".35"/>
<circle cx="32" cy="28" r="6.5" fill="#ff5f56"/><circle cx="54" cy="28" r="6.5" fill="#ffbd2e"/><circle cx="76" cy="28" r="6.5" fill="#27c93f"/>
<text x="{TW / 2}" y="33" text-anchor="middle" fill="{TEXT}" fill-opacity=".35" style="font-size:14px">~/signal — bash</text>
{"".join(rows)}
<rect x="1" y="1" width="{TW - 2}" height="{TH - 2}" rx="18" fill="url(#scan)"/>
</svg>
"""
(OUT / "terminal.svg").write_text(terminal)

# ---------------------------------------------------------------- divider
divider = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="18" viewBox="0 0 1200 18" aria-hidden="true">
<style>.dot{{animation:run 6s linear infinite}}@keyframes run{{from{{transform:translateX(0)}}to{{transform:translateX(1200px)}}}}{REDUCED}</style>
<defs>
  <linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".2" stop-color="{CYAN}"/><stop offset=".5" stop-color="{MAGENTA}"/><stop offset=".8" stop-color="{GREEN}"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>
  <filter id="g" x="-50%" y="-300%" width="200%" height="700%"><feGaussianBlur stdDeviation="3"/></filter>
</defs>
<rect x="0" y="8" width="1200" height="2" fill="url(#l)" opacity=".5"/>
<rect x="0" y="7" width="1200" height="4" fill="url(#l)" opacity=".5" filter="url(#g)"/>
<circle class="dot" cx="0" cy="9" r="3" fill="#fff" filter="url(#g)"/><circle class="dot" cx="0" cy="9" r="1.6" fill="#fff"/>
</svg>
"""
(OUT / "divider.svg").write_text(divider)

for f in sorted(OUT.iterdir()):
    print(f, f.stat().st_size)
