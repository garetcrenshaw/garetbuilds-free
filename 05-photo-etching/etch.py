"""Photo to ink etching: turns a portrait into a money-style line engraving (SVG).

    python etch.py photo.jpg -o etching.svg --png preview.png

Works best on a head-and-shoulders photo against a plain background.
"""
import argparse
import math

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

p = argparse.ArgumentParser(description="Turn a photo into a line engraving.")
p.add_argument("photo")
p.add_argument("-o", "--out", default="etching.svg", help="SVG to write")
p.add_argument("--png", help="also write a PNG preview here")
p.add_argument("--size", type=int, default=600, help="working size in pixels (bigger = finer, slower)")
p.add_argument("--ink", default="#171512", help="line colour")
p.add_argument("--keep-background", action="store_true", help="etch the background too instead of removing it")
p.add_argument("--no-halo", action="store_true", help="skip the oval of fine lines behind the subject")
p.add_argument("--spacing", type=float, default=3.3, help="gap between lines; smaller = darker and finer")
args = p.parse_args()

# square crop around the centre, resized to the working size
img = Image.open(args.photo).convert("RGB")
w, h = img.size
side = min(w, h)
img = img.crop(((w - side) // 2, 0, (w - side) // 2 + side, side)).resize((args.size, args.size), Image.LANCZOS)
S = args.size
k = S / 600  # scale factor for pixel-based settings
im = np.asarray(img).astype(float)

# subject mask: anything that differs from the average border colour
if args.keep_background:
    fgs = np.ones((S, S))
else:
    border = np.concatenate([im[0], im[-1], im[:, 0], im[:, -1]])
    bg_colour = np.median(border, axis=0)
    dist = np.sqrt(((im - bg_colour) ** 2).sum(-1))
    fg = dist > 60
    fg = ndi.binary_opening(fg, iterations=max(1, round(5 * k)))
    fg = ndi.binary_fill_holes(fg)
    lab, n = ndi.label(fg)
    if n > 1:
        sizes = ndi.sum(fg, lab, range(1, n + 1))
        fg = lab == (1 + int(np.argmax(sizes)))
    fgs = ndi.gaussian_filter(fg.astype(float), 1.2 * k)

# tone: local contrast so evenly lit faces still get shadows
gray = (0.3 * im[..., 0] + 0.59 * im[..., 1] + 0.11 * im[..., 2]) / 255.0
base = ndi.gaussian_filter(gray, 18 * k)
gray = np.clip(gray + (gray - base) * 1.1, 0, 1)
gray = ndi.gaussian_filter(gray, 1.4 * k)
dark = np.clip(((1 - gray) - 0.12) / 0.8, 0, 1) ** 1.85

yy, xx = np.mgrid[0:S, 0:S]
halo = np.zeros((S, S))
if not args.no_halo and not args.keep_background:
    ell = ((xx - S / 2) / (S * 0.44)) ** 2 + ((yy - S * 0.43) / (S * 0.5)) ** 2
    halo = np.clip((1.0 - ell) / 0.35, 0, 1) * 0.075
edge = np.clip(ndi.gaussian_gradient_magnitude(fgs, 1.0 * k) * 2.2 * k, 0, 0.8)
tone = np.maximum(fgs * (0.05 + 0.95 * dark) + (1 - fgs) * halo, edge)
bend = ndi.gaussian_filter(tone, 6 * k)  # lines curve gently around the form


def sample(a, x, y):
    return ndi.map_coordinates(a, [np.clip(y, 0, S - 1.001), np.clip(x, 0, S - 1.001)], order=1)


polys = []


def emit(run, nrm):
    if len(run) < 3:
        return
    top = [(x + nrm[0] * w / 2, y + nrm[1] * w / 2) for x, y, w in run]
    bot = [(x - nrm[0] * w / 2, y - nrm[1] * w / 2) for x, y, w in run][::-1]
    polys.append(top + bot)


def layer(angle, spacing, max_w, t_min, amp, use):
    th = math.radians(angle)
    d = np.array([math.cos(th), math.sin(th)])
    nrm = np.array([-d[1], d[0]])
    diag = S * 1.5
    off = -diag / 2
    while off < diag / 2:
        t = np.arange(-diag / 2, diag / 2, 1.5 * k)
        px = S / 2 + d[0] * t + nrm[0] * off
        py = S / 2 + d[1] * t + nrm[1] * off
        inside = (px >= 0) & (px < S) & (py >= 0) & (py < S)
        if inside.any():
            px, py = px[inside], py[inside]
            shift = amp * (sample(bend, px, py) - 0.3)
            cx, cy = px + nrm[0] * shift, py + nrm[1] * shift
            v = use(sample(tone, cx, cy))
            width = np.where(v > t_min, max_w * v, 0.0)
            run = []
            for i in range(len(cx)):
                if width[i] > 0.18 * k:
                    run.append((cx[i], cy[i], width[i]))
                elif run:
                    emit(run, nrm)
                    run = []
            if run:
                emit(run, nrm)
        off += spacing


# main lines, then cross-hatching only in the shadows
layer(-12, args.spacing * k, 2.6 * k, 0.03, 4.0 * k, lambda v: v)
layer(58, args.spacing * 1.15 * k, 1.9 * k, 0.05, 4.0 * k, lambda v: np.clip((v - 0.45) / 0.55, 0, 1))

path = "".join("M" + " ".join(f"{x:.1f},{y:.1f}" for x, y in poly) + "Z" for poly in polys)
with open(args.out, "w") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}"><path fill="{args.ink}" d="{path}"/></svg>')
print(f"wrote {args.out} ({len(polys)} strokes)")

if args.png:
    sc = 2
    out = Image.new("RGB", (S * sc, S * sc), (241, 236, 227))
    draw = ImageDraw.Draw(out)
    ink = tuple(int(args.ink.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    for poly in polys:
        draw.polygon([(x * sc, y * sc) for x, y in poly], fill=ink)
    out.save(args.png)
    print(f"wrote {args.png}")
