#!/usr/bin/env python3
"""Build the Hardtland static site.

    python3 build/build.py

Writes every page as plain HTML into the repo root (/, /roof-repair/, ...),
plus sitemap.xml and robots.txt, and creates a labeled grey placeholder for
any /img/*.webp file a page uses that doesn't exist yet. Real photos dropped
into /img/ with the same file name are never overwritten.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import common  # noqa: E402
import pages  # noqa: E402
import services  # noqa: E402
import towns  # noqa: E402

LASTMOD = "2026-11-02"


def write_page(path, html):
    if path.endswith(".html"):
        out = os.path.join(ROOT, path.lstrip("/"))
    else:
        out = os.path.join(ROOT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return out


def make_placeholders(htmls):
    """Grey 'PHOTO PLACEHOLDER' images for any referenced photo not on disk."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("  (Pillow not installed; skipping placeholder images)")
        return []
    img_re = re.compile(r'<img[^>]*?src="/img/([^"]+\.webp)"[^>]*?width="(\d+)"[^>]*?height="(\d+)"')
    wanted = {}
    for h in htmls:
        for name, w, hgt in img_re.findall(h):
            wanted.setdefault(name, (int(w), int(hgt)))
    made = []
    bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    reg = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    for name, (w, h) in sorted(wanted.items()):
        dest = os.path.join(ROOT, "img", name)
        if os.path.exists(dest):
            continue
        if name.startswith("badge-"):
            w, h = 240, 120
        im = Image.new("RGB", (w, h), "#C9C2B8" if len(made) % 2 == 0 else "#BFC6CE")
        d = ImageDraw.Draw(im)
        s = max(12, w // 32)
        try:
            fb, fr = ImageFont.truetype(bold, s), ImageFont.truetype(reg, max(10, int(s * .6)))
        except OSError:
            fb = fr = ImageFont.load_default()
        d.text((w // 2, h // 2 - s), "BADGE" if name.startswith("badge-") else "PHOTO PLACEHOLDER",
               fill="#5B6068", font=fb, anchor="mm")
        d.text((w // 2, h // 2 + s), name, fill="#5B6068", font=fr, anchor="mm")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        im.save(dest, "WEBP", quality=60)
        made.append(name)
    return made


def main():
    built = []
    for group in (pages.PAGES, services.PAGES, towns.PAGES):
        for fn in group:
            path, html = fn()
            write_page(path, html)
            built.append((path, html))
            print(f"  {path}")

    # sitemap + robots
    urls = [p for p, h in built if not p.endswith(".html")]
    order = ["/"] + [common.url(s) for s, _ in common.SERVICES] + \
            [common.url(s) for s, _ in common.TOWNS]
    urls.sort(key=lambda u: (order.index(u) if u in order else len(order), u))
    entries = "\n".join(
        f"  <url>\n    <loc>{common.DOMAIN}{u}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n  </url>"
        for u in urls)
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                f"{entries}\n</urlset>\n")
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\nDisallow: /build/\n\n"
                f"Sitemap: {common.DOMAIN}/sitemap.xml\n")

    made = make_placeholders([h for _, h in built])
    print(f"Built {len(built)} pages, {len(urls)} in sitemap, {len(made)} new placeholder images.")


if __name__ == "__main__":
    main()
