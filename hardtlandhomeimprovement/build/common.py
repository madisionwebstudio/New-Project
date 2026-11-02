"""Shared templates for the Hardtland static site.

Every page is plain static HTML. This module only stitches the shared
header, footer, form band and icons around each page's own content so they
stay identical everywhere. Run `python3 build/build.py` after any edit.
"""
import html
import json
import os

DOMAIN = "https://www.hardtlandhomeimprovement.com"
PHONE = "(608) 575-9317"
TEL = "tel:+16085759317"
SMS = "sms:+16085759317"
EMAIL = "tomd@tds.net"
# Editable from the admin panel (data/site.json). The build writes these seed
# values; inc/publish-cli.php then applies the current data/site.json.
HOURS = ('<!--biz:hours--><span class="hours"><span class="hours-note">[REAL HOURS FROM TOM]'
         '</span></span><!--/biz:hours-->')
RATING = "{{RATING}}"      # becomes <!--biz:rating-->4.7<!--/biz:rating--> in the page body
REVIEW_COUNT = "{{REVIEWS}}"
# Where the site is hosted:
#   "netlify" -> forms use Netlify Forms (submissions in the Netlify dashboard,
#                email alerts set up in Netlify). PHP admin/lead.php don't run there.
#   "php"     -> forms post to lead.php (saved in the /admin/ panel + emailed).
HOSTING = "netlify"
FORM_ACTION = "/lead.php"
NETLIFY_FORM = "free-inspection"
GOOGLE_REVIEWS = ("https://www.google.com/maps/search/?api=1&amp;query="
                  "Hardtland+Home+Improvement+Inc+5821+Thrush+Ln+Madison+WI")
BUSINESS_ID = DOMAIN + "/#business"

esc = html.escape

# --------------------------------------------------------------------------
# Site structure
# --------------------------------------------------------------------------
SERVICES = [  # slug, short name, nav label
    ("roof-replacement", "Roof Replacement"),
    ("roof-repair", "Roof Repair"),
    ("storm-hail-damage", "Storm & Hail Damage"),
    ("insurance-claims", "Insurance Claim Help"),
    ("metal-roofing", "Metal Roofing"),
    ("free-roof-inspection", "Free Roof Inspection"),
    ("siding", "Siding"),
    ("gutters", "Gutters"),
    ("windows-doors", "Windows & Doors"),
]
SERVICE_NAME = dict(SERVICES)

TOWNS = [
    ("verona-wi", "Verona"),
    ("madison-wi", "Madison"),
    ("fitchburg-wi", "Fitchburg"),
    ("middleton-wi", "Middleton"),
    ("oregon-wi", "Oregon"),
    ("mount-horeb-wi", "Mount Horeb"),
]
TOWN_NAME = dict(TOWNS)

ROOFING_SLUGS = ["roof-replacement", "roof-repair", "storm-hail-damage",
                 "metal-roofing", "free-roof-inspection"]

SERVICE_ICON = {
    "roof-replacement": "i-home", "roof-repair": "i-wrench",
    "storm-hail-damage": "i-hail", "insurance-claims": "i-file",
    "metal-roofing": "i-layers", "free-roof-inspection": "i-search",
    "siding": "i-siding", "gutters": "i-gutter", "windows-doors": "i-window",
}

# Real review text, word for word. These are excerpts; replace with the full
# Google text before launch.
REVIEWS = {
    "sally": ("Tom and his crew were highly recommended by our neighbor. "
              "They did an excellent job...", "Sally B.", "Hardtland customer"),
    "teresa": ("I have had Hardtland Home Improvement replace our roof twice in "
               "the last 20 years...", "Teresa Adams", "Hardtland customer"),
    "cherise": ("I enjoyed working with Tom! He was friendly, calm, and honest. "
                "After gathering a decent amount of quotes we decided to go "
                "with him due to his responsiveness through text, "
                "comprehensive package, legitimate website, and price.",
                "Cherise Kam", "Google review"),
    "charles": ("Fast and accurate. Modest pricing. Solved our problem without "
                "removing the entire roof...", "Charles Allen", "Google review"),
}

# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------
def icon(name, cls="icon"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#{name}"/></svg>'


def stars():
    s = '<svg><use href="#i-star"/></svg>' * 5
    return f'<span class="trust-stars" aria-hidden="true">{s}</span>'


def url(slug):
    return "/" if slug in ("", "/") else f"/{slug}/"


def ld(obj):
    """JSON-LD script block."""
    body = json.dumps(obj, indent=2, ensure_ascii=False)
    return f'<script type="application/ld+json">\n{body}\n</script>'


# Photo registry: every placeholder image the build should create if missing.
PHOTOS = {}


def photo(file, alt, w=None, h=None, lazy=True, cls=""):
    """<img> with real width/height (read from the file in /img/ when present)."""
    if w is None or h is None:
        w, h = 800, 600
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img", file)
        if os.path.exists(path):
            try:
                from PIL import Image
                with Image.open(path) as im:
                    w, h = im.size
            except Exception:
                pass
    PHOTOS[file] = (w, h)
    loading = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/img/{file}" width="{w}" height="{h}"{loading} '
            f'decoding="async" alt="{esc(alt)}">')


# --------------------------------------------------------------------------
# Icons (Lucide, ISC license) — defined once per page, reused with <use>
# --------------------------------------------------------------------------
SPRITE = """<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">
  <symbol id="i-phone" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></symbol>
  <symbol id="i-message" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></symbol>
  <symbol id="i-mail" viewBox="0 0 24 24"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></symbol>
  <symbol id="i-map-pin" viewBox="0 0 24 24"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></symbol>
  <symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></symbol>
  <symbol id="i-home" viewBox="0 0 24 24"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/></symbol>
  <symbol id="i-wrench" viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></symbol>
  <symbol id="i-hail" viewBox="0 0 24 24"><path d="M4 14.9A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.24"/><path d="M16 14v2"/><path d="M8 14v2"/><path d="M16 20h.01"/><path d="M8 20h.01"/><path d="M12 16v2"/><path d="M12 22h.01"/></symbol>
  <symbol id="i-siding" viewBox="0 0 24 24"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M3 15h18"/></symbol>
  <symbol id="i-layers" viewBox="0 0 24 24"><path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/></symbol>
  <symbol id="i-gutter" viewBox="0 0 24 24"><path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"/><path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"/></symbol>
  <symbol id="i-window" viewBox="0 0 24 24"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 12h18"/><path d="M12 3v18"/></symbol>
  <symbol id="i-star" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></symbol>
  <symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/></symbol>
  <symbol id="i-award" viewBox="0 0 24 24"><circle cx="12" cy="8" r="6"/><path d="M15.48 12.89 17 22l-5-3-5 3 1.52-9.11"/></symbol>
  <symbol id="i-calendar" viewBox="0 0 24 24"><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/></symbol>
  <symbol id="i-user-check" viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="m16 11 2 2 4-4"/></symbol>
  <symbol id="i-file" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/></symbol>
  <symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></symbol>
  <symbol id="i-check-circle" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></symbol>
  <symbol id="i-hammer" viewBox="0 0 24 24"><path d="m15 12-8.37 8.37a1 1 0 1 1-3-3L12 9"/><path d="m18 15 4-4"/><path d="m21.5 11.5-1.91-1.91A2 2 0 0 1 19 8.17V7l-2.26-2.26a6 6 0 0 0-4.2-1.76L9 2.96l.92.82A6.18 6.18 0 0 1 12 8.4V10l2 2h1.17a2 2 0 0 1 1.42.59L18.5 14.5"/></symbol>
  <symbol id="i-camera" viewBox="0 0 24 24"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></symbol>
  <symbol id="i-alert" viewBox="0 0 24 24"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></symbol>
  <symbol id="i-ruler" viewBox="0 0 24 24"><path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.41 2.41 0 0 1 0-3.4l2.6-2.6a2.41 2.41 0 0 1 3.4 0Z"/><path d="m14.5 12.5 2-2"/><path d="m11.5 9.5 2-2"/><path d="m8.5 6.5 2-2"/><path d="m17.5 15.5 2-2"/></symbol>
  <symbol id="i-snow" viewBox="0 0 24 24"><path d="M2 12h20"/><path d="M12 2v20"/><path d="m20 16-4-4 4-4"/><path d="m4 8 4 4-4 4"/><path d="m16 4-4 4-4-4"/><path d="m8 20 4-4 4 4"/></symbol>
  <symbol id="i-wallet" viewBox="0 0 24 24"><path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/></symbol>
  <symbol id="i-arrow-right" viewBox="0 0 24 24"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></symbol>
  <symbol id="i-chevron-down" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></symbol>
  <symbol id="i-plus" viewBox="0 0 24 24"><path d="M12 5v14"/><path d="M5 12h14"/></symbol>
  <symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/></symbol>
  <symbol id="i-x" viewBox="0 0 24 24"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></symbol>
  <symbol id="i-quote" viewBox="0 0 24 24"><path d="M3 21c3 0 7-1 7-8V5c0-1.25-.76-2.02-2-2H4c-1.25 0-2 .75-2 1.97V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .01-1 1.03V20c0 1 0 1 1 1z"/><path d="M15 21c3 0 7-1 7-8V5c0-1.25-.76-2.02-2-2h-4c-1.25 0-2 .75-2 1.97V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"/></symbol>
  <symbol id="i-heart" viewBox="0 0 24 24"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></symbol>
</svg>"""

# --------------------------------------------------------------------------
# Header / footer / call bar
# --------------------------------------------------------------------------
LOGO = """<svg class="logo__heart" aria-hidden="true"><use href="#i-heart"/></svg>
        <span class="logo__text">
          <span class="logo__name">Hardtland</span>
          <span class="logo__sub">Home Improvement, Inc.</span>
        </span>"""


def header(current):
    def cur(path):
        return ' aria-current="page"' if current == path else ""

    def link(path, label):
        return f'<li><a class="nav-link" href="{path}"{cur(path)}>{esc(label)}</a></li>'

    roof_items = "\n".join(
        f'            <li><a href="{url(s)}"{cur(url(s))}>{esc(SERVICE_NAME[s])}</a></li>'
        for s in ROOFING_SLUGS)
    town_items = "\n".join(
        f'            <li><a href="{url(s)}"{cur(url(s))}>{esc(n)}</a></li>' for s, n in TOWNS)
    return f"""<!--biz:notice--><!--/biz:notice-->
<header class="site-header">
  <div class="container header-inner">
    <!-- TODO: replace the heart + wordmark with Tom's high-res logo file -->
    <a class="logo" href="/" aria-label="Hardtland Home Improvement, home">
        {LOGO}
    </a>

    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
      {icon("i-menu", "icon icon-open")}
      {icon("i-x", "icon icon-close")}
      <span>Menu</span>
    </button>

    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul class="nav-list">
        {link("/", "Home")}
        <li class="has-sub">
          <button class="nav-sub-toggle" type="button" aria-expanded="false" aria-controls="sub-roofing">
            Roofing {icon("i-chevron-down", "icon icon-sm")}
          </button>
          <ul class="nav-sub" id="sub-roofing">
{roof_items}
          </ul>
        </li>
        {link("/siding/", "Siding")}
        {link("/gutters/", "Gutters")}
        {link("/windows-doors/", "Windows & Doors")}
        <li class="has-sub">
          <button class="nav-sub-toggle" type="button" aria-expanded="false" aria-controls="sub-areas">
            Service Areas {icon("i-chevron-down", "icon icon-sm")}
          </button>
          <ul class="nav-sub" id="sub-areas">
{town_items}
            <li><a href="/service-areas/"{cur("/service-areas/")}>All service areas</a></li>
          </ul>
        </li>
        {link("/reviews/", "Reviews")}
        {link("/about/", "About")}
      </ul>
      <div class="nav-mobile-cta">
        <a class="btn btn--primary btn--block" href="/free-roof-inspection/">Book a Free Inspection</a>
      </div>
    </nav>

    <a class="header-phone" href="{TEL}">
      {icon("i-phone")}
      <span>{PHONE}</span>
      <span class="visually-hidden">Call Hardtland</span>
    </a>
    <a class="btn btn--primary btn--sm header-cta" href="/free-roof-inspection/">Free Inspection</a>
  </div>
</header>"""


def footer():
    svc = "\n".join(f'        <li><a href="{url(s)}">{esc(n)}</a></li>' for s, n in SERVICES)
    towns = "\n".join(f'        <li><a href="{url(s)}">{esc(n)}, WI</a></li>' for s, n in TOWNS)
    return f"""<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <a class="logo" href="/" aria-label="Hardtland Home Improvement, home">
        {LOGO}
      </a>
      <address class="footer-nap">
        <strong class="visually-hidden">Hardtland Home Improvement, Inc.</strong>
        <div>{icon("i-map-pin")}<span>5821 Thrush Ln<br>Madison, WI 53711</span></div>
        <a href="{TEL}">{icon("i-phone")}{PHONE} (call or text)</a>
        <a href="mailto:{EMAIL}">{icon("i-mail")}{EMAIL}</a>
        <div>{icon("i-clock")}{HOURS}</div>
      </address>
    </div>

    <div>
      <h2 class="footer-title">Services</h2>
      <ul class="footer-links">
{svc}
      </ul>
    </div>

    <div>
      <h2 class="footer-title">Service Areas</h2>
      <ul class="footer-links">
{towns}
        <li><a href="/service-areas/">All service areas</a></li>
      </ul>
    </div>

    <div>
      <h2 class="footer-title">Certified &amp; Trusted</h2>
      <p>CertainTeed Master Shingler. Owens Corning Certified. Licensed in Wisconsin. Licensed, bonded and insured.</p>
      <div class="footer-badges">
        <!-- BADGE FILES NEEDED from Tom / the manufacturers -->
        {photo("badge-certainteed-master-shingler.webp", "CertainTeed Master Shingler certification badge", 120, 60)}
        {photo("badge-owens-corning-certified.webp", "Owens Corning Certified contractor badge", 120, 60)}
      </div>
      <!-- TODO: replace with the direct "write a review" link for the Google profile -->
      <a class="footer-review" href="{GOOGLE_REVIEWS}" target="_blank" rel="noopener">
        {stars()}
        {RATING} on Google. Leave us a review<span class="visually-hidden"> (opens in a new tab)</span>
      </a>
    </div>
  </div>

  <div class="container footer-bottom">
    <p>&copy; 2026 Hardtland Home Improvement, Inc. Owner-run since 1972.</p>
    <ul>
      <li><a href="/about/">About</a></li>
      <li><a href="/gallery/">Gallery</a></li>
      <li><a href="/faq/">FAQ</a></li>
      <li><a href="/contact/">Contact</a></li>
      <li><a href="/privacy-policy/">Privacy Policy</a></li>
      <li><a href="/accessibility/">Accessibility</a></li>
    </ul>
  </div>
</footer>

<div class="call-bar" role="region" aria-label="Quick contact">
  <a class="btn btn--primary" href="{TEL}">
    {icon("i-phone", "icon icon-sm")} Call
  </a>
  <a class="btn btn--dark" href="{SMS}">
    {icon("i-message", "icon icon-sm")} Text Tom
  </a>
</div>"""


# --------------------------------------------------------------------------
# Reusable page sections
# --------------------------------------------------------------------------
def form_band(source, heading="Get a Free Roof Inspection This Week",
              lead="Tell us a little about your home. Tom or the crew will set up a time to take a look, free and with no pressure.",
              select=None, uid="f"):
    return f"""<section class="section cta-band on-dark" id="free-inspection" aria-labelledby="cta-title">
    <div class="container cta-band__grid">
      <div>
        <p class="eyebrow">Free inspection</p>
        <h2 id="cta-title">{esc(heading)}</h2>
        <p class="cta-band__lead">{lead}</p>

        <ul class="cta-points">
          <li>{icon("i-check")}<span>Photos of what we find</span></li>
          <li>{icon("i-check")}<span>An honest repair-or-replace answer</span></li>
          <li>{icon("i-check")}<span>Help with insurance if it's storm damage</span></li>
        </ul>

        <div class="cta-contact">
          <a href="{TEL}">{icon("i-phone")}Call {PHONE}</a>
          <a href="{SMS}">{icon("i-message")}Text Tom at the same number</a>
        </div>
        <p class="cta-pay">We accept insurance, personal checks, cash and Zelle.</p>
      </div>

      <div class="form-card">
        <h3>Book a Free Inspection</h3>
        <p>Takes about 30 seconds.</p>
        {form(source, select, uid)}
      </div>
    </div>
  </section>"""


def form(source, select=None, uid="f"):
    options = ["Roof repair", "Roof replacement", "Storm/hail damage", "Siding",
               "Gutters", "Windows/doors", "Other"]
    opts = "\n".join(
        f'            <option{" selected" if o == select else ""}>{o}</option>' for o in options)
    if HOSTING == "netlify":
        open_tag = (f'<!-- Netlify Forms: submissions appear in the Netlify dashboard (Forms). -->\n'
                    f'        <form name="{NETLIFY_FORM}" action="/thank-you/" method="post" data-lead-form '
                    f'data-netlify="true" netlify-honeypot="website">\n'
                    f'          <input type="hidden" name="form-name" value="{NETLIFY_FORM}">')
    else:
        open_tag = (f'<!-- Saved to the admin panel (/admin/) and emailed. See lead.php. -->\n'
                    f'        <form action="{FORM_ACTION}" method="post" data-lead-form>')
    return f"""{open_tag}
          <input type="hidden" name="source_page" value="{source}">
          <input type="hidden" name="ts" value="">
          <div class="field">
            <label for="{uid}-name">Your name</label>
            <input id="{uid}-name" name="name" type="text" autocomplete="name" required>
          </div>
          <div class="field-row">
            <div class="field">
              <label for="{uid}-phone">Phone</label>
              <input id="{uid}-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required>
            </div>
            <div class="field">
              <label for="{uid}-need">What do you need?</label>
              <select id="{uid}-need" name="need" required>
            <option value="">Choose one</option>
{opts}
              </select>
            </div>
          </div>
          <div class="field">
            <label for="{uid}-address">Home address</label>
            <input id="{uid}-address" name="address" type="text" autocomplete="street-address" required>
          </div>
          <div class="hp-field" aria-hidden="true">
            <label for="{uid}-website">Leave this field empty</label>
            <input id="{uid}-website" name="website" type="text" tabindex="-1" autocomplete="off">
          </div>
          <p class="form-status" role="alert" aria-live="assertive"></p>
          <button class="btn btn--primary btn--block" type="submit">Book My Free Inspection</button>
          <p class="form-promise">
            {icon("i-clock", "icon icon-sm")}
            <span>Tom or the crew will call you back within 1 business day.</span>
          </p>
        </form>"""


def breadcrumbs(trail):
    """trail: list of (name, path); last item is the current page."""
    items = []
    for i, (name, path) in enumerate(trail):
        if i == len(trail) - 1:
            items.append(f'<li><span aria-current="page">{esc(name)}</span></li>')
        else:
            items.append(f'<li><a href="{path}">{esc(name)}</a></li>')
    return (f'<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container">'
            f'<ol>{"".join(items)}</ol></div></nav>')


def breadcrumb_ld(trail):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": DOMAIN + path}
            for i, (name, path) in enumerate(trail)
        ],
    }


def page_hero(h1, lead, eyebrow=None, buttons=True, cta_label="Book a Free Inspection",
              cta_href="#free-inspection"):
    eb = f'<p class="eyebrow">{esc(eyebrow)}</p>' if eyebrow else ""
    btns = ""
    if buttons:
        btns = f"""<div class="btn-row">
          <a class="btn btn--primary" href="{cta_href}">{esc(cta_label)}</a>
          <a class="btn btn--outline-light" href="{TEL}">{icon("i-phone", "icon icon-sm")} Call {PHONE}</a>
        </div>"""
    return f"""<section class="page-hero" aria-labelledby="page-title">
    <div class="container">
      <div class="page-hero__inner">
        {eb}
        <h1 id="page-title">{h1}</h1>
        <p class="page-hero__lead">{lead}</p>
        {btns}
        <ul class="chips" aria-label="Why Hardtland">
          <li>{icon("i-calendar", "icon icon-sm")}Since 1972</li>
          <li>{icon("i-award", "icon icon-sm")}CertainTeed Master Shingler</li>
          <li>{icon("i-star", "icon icon-sm")}{RATING} Google ({REVIEW_COUNT} reviews)</li>
          <li>{icon("i-user-check", "icon icon-sm")}Owner on every job</li>
        </ul>
      </div>
    </div>
  </section>"""


def faq_section(faqs, title="Common Questions", band=True, eyebrow="FAQ", h_id="faq-title"):
    items = "\n".join(
        f"""        <details class="faq-item">
          <summary>{esc(q)} {icon("i-plus")}</summary>
          <div class="faq-item__body">{a if a.lstrip().startswith("<") else "<p>" + a + "</p>"}</div>
        </details>""" for q, a in faqs)
    cls = "section section--sand" if band else "section"
    return f"""<section class="{cls}" aria-labelledby="{h_id}">
    <div class="container">
      <div class="section-head section-head--center">
        <p class="eyebrow">{eyebrow}</p>
        <h2 id="{h_id}">{esc(title)}</h2>
      </div>
      <div class="faq">
{items}
      </div>
    </div>
  </section>"""


def faq_ld(faqs):
    import re
    def plain(a):
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", a)).strip()
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": html.unescape(plain(a))}}
            for q, a in faqs
        ],
    }


def review_cards(keys):
    out = []
    for k in keys:
        text, name, source = REVIEWS[k]
        out.append(f"""<figure class="card review">
          {icon("i-quote", "icon review__mark")}
          <blockquote><p>"{esc(text, quote=False)}"</p></blockquote>
          <figcaption>
            <span class="review__avatar" aria-hidden="true">{name[0]}</span>
            <span><span class="review__name">{esc(name)}</span><span class="review__source">{source}</span></span>
          </figcaption>
        </figure>""")
    return "\n        ".join(out)


def reviews_section(keys, title="What Customers Say", band=False):
    cls = "section section--sand" if band else "section"
    grid = "grid--3" if len(keys) >= 3 else "grid--2"
    return f"""<section class="{cls}" aria-labelledby="reviews-title">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Reviews</p>
        <h2 id="reviews-title">{esc(title)}</h2>
        <div class="rating-summary">
          <span class="rating-summary__score">{RATING}</span>{stars()}
          <span>{RATING} out of 5 stars on Google, from {REVIEW_COUNT} reviews</span>
        </div>
      </div>
      <div class="grid {grid}">
        {review_cards(keys)}
      </div>
      <p class="services-foot"><a class="text-link" href="/reviews/">Read more reviews {icon("i-arrow-right", "icon icon-sm")}</a></p>
    </div>
  </section>"""


def project_grid(items):
    """items: list of (file, alt, caption_html)."""
    lis = "\n".join(
        f"""        <li>
          <figure class="project">
            {photo(f, alt)}
            <figcaption>{icon("i-map-pin")}<span>{cap}</span></figcaption>
          </figure>
        </li>""" for f, alt, cap in items)
    return f'<ul class="projects">\n{lis}\n      </ul>'


def projects_section(items, title, lead="Real Hardtland jobs. No stock photos.", band=True):
    cls = "section section--sand" if band else "section"
    return f"""<section class="{cls}" aria-labelledby="projects-title">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Recent work</p>
        <h2 id="projects-title">{esc(title)}</h2>
        <p>{lead}</p>
      </div>
      {project_grid(items)}
      <p class="services-foot"><a class="text-link" href="/gallery/">See more projects {icon("i-arrow-right", "icon icon-sm")}</a></p>
    </div>
  </section>"""


def steps_section(steps, title="Our 4-Step Process", lead=None, h_id="how-title"):
    icons = ["i-search", "i-camera", "i-file", "i-hammer"]
    lis = "\n".join(
        f"""        <li class="step">
          <span class="step__num" aria-hidden="true">{i + 1}</span>
          {icon(icons[i] if len(s) < 3 else s[2], "icon step__icon")}
          <h3>{esc(s[0])}</h3>
          <p>{s[1]}</p>
        </li>""" for i, s in enumerate(steps))
    lead_html = f"<p>{lead}</p>" if lead else ""
    return f"""<section class="section section--dark" aria-labelledby="{h_id}">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">How it works</p>
        <h2 id="{h_id}">{esc(title)}</h2>
        {lead_html}
      </div>
      <ol class="steps">
{lis}
      </ol>
    </div>
  </section>"""


def link_cards(slugs, names, kind="service"):
    out = []
    for s in slugs:
        name = names[s]
        ic = SERVICE_ICON.get(s, "i-map-pin")
        label = name if kind == "service" else f"Roofer in {name}, WI"
        out.append(f'<li><a href="{url(s)}">{icon(ic)}{esc(label)}</a></li>')
    return "".join(out)


def related_section(services, towns):
    return f"""<section class="section" aria-labelledby="related-title">
    <div class="container related">
      <div>
        <h2 id="related-title" class="h3-like">Related services</h2>
        <ul class="link-list">{link_cards(services, SERVICE_NAME)}</ul>
      </div>
      <div>
        <h2 class="h3-like">Local roofing near you</h2>
        <ul class="link-list">{link_cards(towns, TOWN_NAME, "town")}</ul>
      </div>
    </div>
  </section>"""


def map_embed(query, title, zoom=12):
    q = query.replace(" ", "+")
    return f"""<div class="map-frame">
        <iframe title="{esc(title)}"
          src="https://www.google.com/maps?q={q}&amp;z={zoom}&amp;output=embed"
          width="800" height="600" loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>"""


# --------------------------------------------------------------------------
# Full page shell
# --------------------------------------------------------------------------
PAGE_TYPES = {"/about/": "AboutPage", "/contact/": "ContactPage", "/gallery/": "ImageGallery",
              "/service-areas/": "CollectionPage"}
FONTS = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;600&amp;"
         "family=Oswald:wght@600;700&amp;display=swap")


def webpage_ld(path, title, description, page_type="WebPage", extra=None):
    """WebPage node tying every page to the site and the business."""
    obj = {
        "@context": "https://schema.org",
        "@type": page_type,
        "@id": DOMAIN + path + "#webpage",
        "url": DOMAIN + path,
        "name": html.unescape(title),
        "description": html.unescape(description),
        "inLanguage": "en-US",
        "isPartOf": {"@id": DOMAIN + "/#website"},
        "about": {"@id": BUSINESS_ID},
        "publisher": {"@id": BUSINESS_ID},
    }
    if extra:
        obj.update(extra)
    return obj


def render(path, title, description, main, current=None, schemas=(), preload=None,
           og_title=None, robots=None, preload_html=None, head_html="", page_extra=None):
    canonical = DOMAIN + path
    indexable = robots is None
    if indexable:
        schemas = [webpage_ld(path, title, description, PAGE_TYPES.get(path, "WebPage"), page_extra)] + list(schemas)
    pre = ""
    if preload:
        pre = (f'\n  <link rel="preload" as="image" type="image/webp" href="{preload}" '
               f'fetchpriority="high">')
    if preload_html:
        pre = "\n\n  <!-- Hero photo first: it is the largest thing on screen (LCP) -->\n  " + preload_html
    ld_blocks = "\n  ".join(ld(s) for s in schemas)
    robots_meta = (f'\n  <meta name="robots" content="{robots}">' if robots else
                   '\n  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">')
    return f"""<!doctype html>
<html lang="en-US" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">{robots_meta}
  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#1F2328">
  <meta name="geo.region" content="US-WI">
  <meta name="geo.placename" content="Madison">
  <meta name="geo.position" content="43.0295;-89.4822">
  <meta name="ICBM" content="43.0295, -89.4822">
  <!--biz:tracking--><!--/biz:tracking-->

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Hardtland Home Improvement, Inc.">
  <meta property="og:title" content="{esc(og_title or title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{DOMAIN}/img/og-hardtland.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Hardtland Home Improvement, Madison and Verona roofer since 1972">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(og_title or title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="twitter:image" content="{DOMAIN}/img/og-hardtland.jpg">

  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-48.png" type="image/png" sizes="48x48">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <script>document.documentElement.classList.replace('no-js', 'js');</script>{pre}

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <!-- Fonts load without blocking the first paint -->
  <link rel="preload" as="style" href="{FONTS}" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="{FONTS}"></noscript>
  <link rel="stylesheet" href="/css/styles.css">

  {ld_blocks}{head_html}

  <script src="/js/main.js" defer></script>
</head>
<body>

{SPRITE}

<a class="skip-link" href="#main">Skip to main content</a>

{header(current or path)}

<main id="main">
  {main}
</main>

{footer()}

</body>
</html>
"""


def service_ld(name, slug, description, service_type=None):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "serviceType": service_type or name,
        "description": description,
        "url": DOMAIN + url(slug),
        "provider": {"@id": BUSINESS_ID, "@type": "RoofingContractor",
                     "name": "Hardtland Home Improvement, Inc."},
        "areaServed": [{"@type": "City", "name": f"{n}, WI"} for _, n in TOWNS]
        + [{"@type": "AdministrativeArea", "name": c}
           for c in ("Dane County, WI", "Green County, WI", "Rock County, WI")],
    }
