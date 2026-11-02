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



SEED_RATING, SEED_REVIEWS = "4.7", "32"


def fill_tokens(html):
    """{{RATING}}/{{REVIEWS}}: plain text in <head>, editable markers in <body>."""
    head, sep, body = html.partition("</head>")
    head = head.replace("{{RATING}}", SEED_RATING).replace("{{REVIEWS}}", SEED_REVIEWS)
    body = (body.replace("{{RATING}}", f"<!--biz:rating-->{SEED_RATING}<!--/biz:rating-->")
                .replace("{{REVIEWS}}", f"<!--biz:reviews-->{SEED_REVIEWS}<!--/biz:reviews-->"))
    return head + sep + body


def write_page(path, html):
    html = fill_tokens(html)
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

STATE_FILE = os.path.join(HERE, "sitemap-state.json")
PRIORITY = {"/": "1.0"}


def indexable(path, html):
    return not path.endswith(".html") and 'content="noindex' not in html


def content_hash(html):
    """Hash of the page minus admin-managed bits, so lastmod only moves on real edits."""
    import hashlib
    stripped = re.sub(r"<!--biz:([a-z]+)-->.*?<!--/biz:\1-->", "", html, flags=re.S)
    return hashlib.sha256(stripped.encode()).hexdigest()[:16]


def write_sitemap(built):
    import datetime
    import json
    from xml.sax.saxutils import escape
    today = datetime.date.today().isoformat()
    try:
        state = json.load(open(STATE_FILE))
    except (OSError, ValueError):
        state = {}
    order = ["/"] + [common.url(s) for s, _ in common.SERVICES] + [common.url(s) for s, _ in common.TOWNS]
    pages_ = sorted([(p, h) for p, h in built if indexable(p, h)],
                    key=lambda ph: (order.index(ph[0]) if ph[0] in order else len(order), ph[0]))
    new_state, entries = {}, []
    for path, html in pages_:
        h = content_hash(html)
        old = state.get(path, {})
        lastmod = old.get("lastmod", today) if old.get("hash") == h else today
        new_state[path] = {"hash": h, "lastmod": lastmod}
        main = html.split("<main", 1)[-1].split("</main>", 1)[0]
        imgs = []
        for src in re.findall(r'<img[^>]*?src="(/img/[^"]+)"', main):
            if "badge-" not in src and src not in imgs:
                imgs.append(src)
        img_xml = "".join(f"\n    <image:image><image:loc>{escape(common.DOMAIN + i)}</image:loc></image:image>"
                          for i in imgs[:20])
        prio = PRIORITY.get(path, "0.8" if path in order else "0.6")
        entries.append(f"  <url>\n    <loc>{escape(common.DOMAIN + path)}</loc>\n    <lastmod>{lastmod}</lastmod>"
                       f"\n    <priority>{prio}</priority>{img_xml}\n  </url>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
                '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
                + "\n".join(entries) + "\n</urlset>\n")
    with open(STATE_FILE, "w") as f:
        json.dump(new_state, f, indent=1, sort_keys=True)
    print(f"sitemap.xml: {len(entries)} pages")


def write_robots():
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write("# Hardtland Home Improvement\n"
                "User-agent: *\n"
                "Allow: /\n"
                "Disallow: /admin/\n"
                "Disallow: /lead.php\n"
                "\n"
                f"Sitemap: {common.DOMAIN}/sitemap.xml\n")


def write_llms(built):
    """llms.txt: a plain summary that AI assistants and answer engines can read."""
    def meta(html, pat):
        m = re.search(pat, html)
        return __import__("html").unescape(m.group(1)) if m else ""
    groups = [("Services", [common.url(s) for s, _ in common.SERVICES]),
              ("Service areas", ["/service-areas/"] + [common.url(s) for s, _ in common.TOWNS]),
              ("About and help", ["/about/", "/reviews/", "/gallery/", "/faq/", "/contact/"])]
    by_path = dict(built)
    lines = ["# Hardtland Home Improvement, Inc.", "",
             "> Family-owned roofing contractor in Madison, Wisconsin, founded in 1972 by Tom Degenhardt. "
             "CertainTeed Master Shingler and Owens Corning Certified. Roof replacement, roof repair, "
             "hail and storm damage, insurance claim help, metal roofing, siding, gutters, windows and doors "
             "for Madison, Verona, Fitchburg, Middleton, Oregon, Mount Horeb and Dane, Green and Rock counties.", "",
             f"- Phone (call or text): {common.PHONE}",
             f"- Email: {common.EMAIL}",
             "- Address: 5821 Thrush Ln, Madison, WI 53711",
             "- Free roof and exterior inspections; works with all insurance companies",
             "- Payment: insurance, personal checks, cash, Zelle", ""]
    for title, paths in groups:
        lines.append(f"## {title}")
        lines.append("")
        for p in paths:
            h = by_path.get(p, "")
            name = meta(h, r'<h1[^>]*>(.*?)</h1>')
            desc = meta(h, r'name="description" content="([^"]*)"')
            lines.append(f"- [{re.sub('<[^>]+>', '', name)}]({common.DOMAIN}{p}): {desc}")
        lines.append("")
    with open(os.path.join(ROOT, "llms.txt"), "w") as f:
        f.write("\n".join(lines))


def make_brand_images():
    """Share image (1200x630), favicons and app icons, created once if missing."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return
    red, charcoal, white = "#E8282B", "#1F2328", "#FFFFFF"

    def heart(draw, cx, cy, size, fill):
        r = size * 0.27
        draw.ellipse([cx - 2 * r, cy - 1.6 * r, cx, cy + 0.4 * r], fill=fill)
        draw.ellipse([cx, cy - 1.6 * r, cx + 2 * r, cy + 0.4 * r], fill=fill)
        draw.polygon([(cx - 1.93 * r, cy - 0.2 * r), (cx + 1.93 * r, cy - 0.2 * r), (cx, cy + 2.0 * r)], fill=fill)
        draw.polygon([(cx - r, cy - 0.6 * r), (cx + r, cy - 0.6 * r), (cx, cy + 0.6 * r)], fill=fill)

    def font(bold, size):
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else "")
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            return ImageFont.load_default()

    og = os.path.join(ROOT, "img", "og-hardtland.jpg")
    if not os.path.exists(og):
        im = Image.new("RGB", (1200, 630), charcoal)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 1200, 12], fill=red)
        heart(d, 128, 150, 120, red)
        d.text((220, 105), "HARDTLAND", fill=white, font=font(True, 64))
        d.text((222, 180), "HOME IMPROVEMENT, INC.", fill="#B9B5AF", font=font(False, 28))
        d.text((90, 300), "Madison & Verona's", fill=white, font=font(True, 66))
        d.text((90, 380), "Roofer Since 1972", fill=white, font=font(True, 66))
        d.text((90, 500), f"CertainTeed Master Shingler  \u00b7  Free Inspections  \u00b7  {common.PHONE}",
               fill="#E9E6E1", font=font(False, 30))
        im.save(og, "JPEG", quality=85, optimize=True)
    for name, size, pad in (("apple-touch-icon.png", 180, 0.18), ("icon-192.png", 192, 0.18),
                            ("icon-512.png", 512, 0.18), ("favicon-48.png", 48, 0.08)):
        dest = os.path.join(ROOT, name)
        if os.path.exists(dest):
            continue
        big = size * 4
        im = Image.new("RGB", (big, big), charcoal if name != "favicon-48.png" else white)
        heart(ImageDraw.Draw(im), big / 2, big * 0.47, big * (1 - 2 * pad), red)
        im.resize((size, size), Image.LANCZOS).save(dest, "PNG", optimize=True)
    manifest = os.path.join(ROOT, "site.webmanifest")
    with open(manifest, "w") as f:
        f.write('{\n  "name": "Hardtland Home Improvement",\n  "short_name": "Hardtland",\n'
                '  "icons": [\n    {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},\n'
                '    {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}\n  ],\n'
                '  "theme_color": "#1F2328",\n  "background_color": "#FAF8F5",\n  "display": "browser"\n}\n')


def main():
    built = []
    for group in (pages.PAGES, services.PAGES, towns.PAGES):
        for fn in group:
            path, html = fn()
            write_page(path, html)
            built.append((path, html))
            print(f"  {path}")

    write_sitemap(built)
    write_robots()
    write_llms(built)
    make_brand_images()

    made = make_placeholders([h for _, h in built])
    print(f"Built {len(built)} pages, {len(made)} new placeholder images.")

    # Apply the admin-editable business info (data/site.json) to the new pages.
    import subprocess
    try:
        subprocess.run(["php", os.path.join(ROOT, "inc", "publish-cli.php")], check=True)
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"WARNING: could not run php inc/publish-cli.php ({e}). Pages show seed values.")


if __name__ == "__main__":
    main()
