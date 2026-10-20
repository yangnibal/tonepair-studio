#!/usr/bin/env python3
"""Compose an Instagram post (1080x1350) from a generated mannequin image.

The garment colors shown on the chips are sampled from the image itself,
so the chips always match what the viewer sees.

Usage:
  .venv/bin/python scripts/compose_post.py work/specs/men_navy_cream.json
"""
import json
import pathlib
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1080, 1350
INK = (29, 29, 31)
FONT_SANS = "/System/Library/Fonts/Avenir Next.ttc"
FONT_SERIF = "/System/Library/Fonts/NewYork.ttf"


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def background_color(arr):
    border = np.concatenate([arr[:40].reshape(-1, 3), arr[:, :40].reshape(-1, 3), arr[:, -40:].reshape(-1, 3)])
    return np.median(border, axis=0)


def figure_mask(arr, bg, threshold=60):
    dist = np.sqrt(((arr.astype(float) - bg) ** 2).sum(axis=2))
    mask = dist > threshold
    return np.array(Image.fromarray(mask.astype(np.uint8) * 255).filter(ImageFilter.MedianFilter(5))) > 127


def bbox(mask):
    mask = mask.copy()
    h, w = mask.shape
    mask[:, : int(w * 0.08)] = False
    mask[:, int(w * 0.92):] = False
    mask[: int(h * 0.03)] = False
    rows = np.where(mask.sum(axis=1) > 6)[0]
    cols = np.where(mask.sum(axis=0) > 6)[0]
    return cols[0], rows[0], cols[-1], rows[-1]


def sample(arr, mask, box, rel, use_mask=False):
    x0, y0, x1, y1 = box
    fw, fh = x1 - x0, y1 - y0
    a, b, c, d = rel
    sx0, sx1 = int(x0 + a * fw), int(x0 + c * fw)
    sy0, sy1 = int(y0 + b * fh), int(y0 + d * fh)
    region = arr[sy0:sy1, sx0:sx1].reshape(-1, 3)
    m = mask[sy0:sy1, sx0:sx1].reshape(-1)
    px = region[m] if use_mask and m.sum() > 50 else region
    return tuple(int(v) for v in np.median(px, axis=0))


def feather(size, pad):
    w, h = size
    alpha = Image.new("L", size, 0)
    ImageDraw.Draw(alpha).rectangle([pad, pad, w - pad, h - pad], fill=255)
    return alpha.filter(ImageFilter.GaussianBlur(pad / 2))


def compose(spec_path):
    spec = json.loads(pathlib.Path(spec_path).read_text())
    src = Image.open(ROOT / spec["image"]).convert("RGB")
    arr = np.array(src)
    bg = background_color(arr)
    mask = figure_mask(arr, bg)
    box = bbox(mask)
    loose = figure_mask(arr, bg, threshold=40)
    colors = [(it["name"], sample(arr, loose, box, it["box"], it.get("mask", False))) for it in spec["items"]]

    fig_h = box[3] - box[1]
    scale = min(1.0, 1040 / fig_h)
    img = src.resize((int(src.width * scale), int(src.height * scale)), Image.LANCZOS)
    cx = (box[0] + box[2]) / 2 * scale
    foot = box[3] * scale
    ox, oy = int(420 - cx), int(H - 80 - foot)

    canvas = Image.new("RGB", (W, H), tuple(int(v) for v in bg))
    canvas.paste(img, (ox, oy), feather(img.size, 70))
    draw = ImageDraw.Draw(canvas)

    draw.text((64, 64), spec["number"], font=font(FONT_SANS, 28, 1), fill=INK + (255,))
    draw.text((62, 104), spec["title"], font=font(FONT_SERIF, 60), fill=INK)

    top = H // 2 - (len(colors) * 128) // 2
    for i, (name, rgb) in enumerate(colors):
        y = top + i * 128
        draw.ellipse([740, y, 812, y + 72], fill=rgb, outline=tuple(int(v * 0.86) for v in bg), width=2)
        draw.text((832, y + 6), name, font=font(FONT_SANS, 30, 5), fill=INK)
        draw.text((832, y + 42), "#%02X%02X%02X" % rgb, font=font(FONT_SANS, 23), fill=(90, 90, 92))

    handle = "@tonepair.studio"
    f = font(FONT_SANS, 24)
    tw = draw.textlength(handle, font=f)
    draw.text((W - 64 - tw, H - 64), handle, font=f, fill=(90, 90, 92))

    out = ROOT / spec["output"]
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, "JPEG", quality=92)
    print(out.relative_to(ROOT), [(n, "#%02X%02X%02X" % c) for n, c in colors])





def text_color(rgb):
    r, g, b = rgb
    return (255, 255, 255) if (0.299 * r + 0.587 * g + 0.114 * b) < 150 else INK


def extend_background(img, ox, oy):
    """Fill the full canvas with the photo's own backdrop gradient so the photo has no visible frame."""
    a = np.asarray(img).astype(float)
    left = np.median(a[:, :14], axis=1)
    right = np.median(a[:, -14:], axis=1)
    rows = np.clip(np.arange(H) - oy, 0, a.shape[0] - 1)
    L, R = left[rows], right[rows]
    t = (np.arange(W) / (W - 1))[None, :, None]
    fill = L[:, None, :] * (1 - t) + R[:, None, :] * t
    return Image.fromarray(fill.astype(np.uint8))


def compose_pair(spec_path):
    """One scene with a male and a female mannequin, plus a full-width palette band."""
    spec = json.loads(pathlib.Path(spec_path).read_text())
    src = Image.open(ROOT / spec["image"]).convert("RGB")
    arr = np.array(src)
    bg = background_color(arr)
    x0, y0, x1, y1 = bbox(figure_mask(arr, bg))
    colors = []
    for it in spec["items"]:
        a, b, c, d = it["abs"]
        colors.append((it["name"], tuple(int(v) for v in np.median(arr[b:d, a:c].reshape(-1, 3), axis=0))))

    band_h = 190
    fig_top, fig_bottom = 185, H - band_h - 36
    scale = min((fig_bottom - fig_top) / (y1 - y0), W / src.width * 1.15)
    img = src.resize((int(src.width * scale), int(src.height * scale)), Image.LANCZOS)
    ox = int(W / 2 - (x0 + x1) / 2 * scale)
    oy = int(fig_top - y0 * scale)
    canvas = extend_background(img, ox, oy)
    canvas.paste(img, (ox, oy), feather(img.size, 46))
    draw = ImageDraw.Draw(canvas)

    draw.text((64, 58), spec["number"], font=font(FONT_SANS, 26, 1), fill=INK)
    draw.text((62, 94), spec["title"], font=font(FONT_SERIF, 56), fill=INK)
    handle = "@tonepair.studio"
    f = font(FONT_SANS, 24)
    draw.text((W - 64 - draw.textlength(handle, font=f), 66), handle, font=f, fill=(90, 90, 92))

    n = len(colors)
    bw = W / n
    top = H - band_h
    for i, (name, rgb) in enumerate(colors):
        bx0, bx1 = int(i * bw), int((i + 1) * bw)
        draw.rectangle([bx0, top, bx1, H], fill=rgb)
        tc = text_color(rgb)
        draw.text((bx0 + 36, top + 84), name, font=font(FONT_SANS, 36, 5), fill=tc)
        draw.text((bx0 + 36, top + 130), "#%02X%02X%02X" % rgb, font=font(FONT_SANS, 26), fill=tc)

    out = ROOT / spec["output"]
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, "JPEG", quality=94)
    print(out.relative_to(ROOT), "scale %.3f" % scale, [(nm, "#%02X%02X%02X" % c) for nm, c in colors])


if __name__ == "__main__":
    for p in sys.argv[1:]:
        layout = json.loads(pathlib.Path(p).read_text()).get("layout", "single")
        (compose_pair if layout == "pair" else compose)(p)
