"""Homepage and supporting pages: service areas, reviews, about, gallery,
FAQ, contact, privacy, accessibility and 404."""
import html
import json
import os
import re

from common import (DOMAIN, BUSINESS_ID, RATING, REVIEW_COUNT, ld, esc, icon, stars, url, render, breadcrumbs, breadcrumb_ld, page_hero,
                    faq_section, faq_ld, review_cards, project_grid, form_band, form,
                    map_embed, photo, SERVICES, SERVICE_ICON, TOWNS, TEL, SMS, PHONE,
                    EMAIL, HOURS, GOOGLE_REVIEWS)

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = []


def add(fn):
    PAGES.append(fn)
    return fn


def simple_section(inner, band=False, h_id=None):
    cls = "section section--sand" if band else "section"
    return f'<section class="{cls}"><div class="container">{inner}</div></section>'


# ==========================================================================
# HOME
# ==========================================================================
WEBSITE_LD = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": DOMAIN + "/#website",
    "url": DOMAIN + "/",
    "name": "Hardtland Home Improvement",
    "alternateName": "Hardtland",
    "inLanguage": "en-US",
    "publisher": {"@id": BUSINESS_ID},
}

TOM_LD = {
    "@context": "https://schema.org",
    "@type": "Person",
    "@id": DOMAIN + "/about/#tom",
    "name": "Tom Degenhardt",
    "jobTitle": "Owner",
    "worksFor": {"@id": BUSINESS_ID},
    "url": DOMAIN + "/about/",
    "knowsAbout": ["Roof replacement", "Roof repair", "Storm and hail damage", "Siding", "Gutters",
                   "Windows and doors", "Roofing insurance claims"],
}

HOME_PRELOAD = (
    '<link rel="preload" as="image" type="image/webp" '
    'href="/img/hero-roof-replacement-verona-1600.webp" '
    'imagesrcset="/img/hero-roof-replacement-verona-800.webp 800w, '
    '/img/hero-roof-replacement-verona-1600.webp 1600w" '
    'imagesizes="100vw" fetchpriority="high">')


@add
def home():
    main = open(os.path.join(HERE, "home_main.html")).read().strip()
    main = main.replace("{{HOME_FORM}}", form("/", None, "f"))
    faq = json.loads(open(os.path.join(HERE, "home_ld_faq.json")).read())
    # Business schema is written by inc/publish-cli.php from data/site.json
    business = ("\n  <!--biz:ld-->" + ld(json.loads(open(os.path.join(HERE, "home_ld_business.json")).read()))
                + "<!--/biz:ld-->")
    return "/", render(
        "/", "Roofing Contractor Madison & Verona WI | Hardtland Since 1972",
        "Family roofer serving Madison, Verona and Dane County since 1972. CertainTeed Master Shingler. Free roof inspections and insurance claim help.",
        main, schemas=[WEBSITE_LD, faq], preload_html=HOME_PRELOAD, head_html=business,
        og_title="Madison & Verona's Roofer Since 1972 | Hardtland Home Improvement")


# ==========================================================================
# SERVICE AREAS
# ==========================================================================
TOWN_BLURBS = {
    "verona-wi": "About 6 miles from our base. Older homes near Main Street and newer subdivisions alike.",
    "madison-wi": "Our hometown since 1972. West side, near east side and everywhere in between.",
    "fitchburg-wi": "Just up the road. Established neighborhoods and newer homes needing their first new roof.",
    "middleton-wi": "Larger homes with complex rooflines, plus classic homes near downtown.",
    "oregon-wi": "Village homes, newer subdivisions and rural properties in southern Dane County.",
    "mount-horeb-wi": "Homes on the ridge west of Madison that take the brunt of the wind.",
}


@add
def service_areas():
    path = "/service-areas/"
    trail = [("Home", "/"), ("Service Areas", path)]
    cards = "\n".join(
        f"""<article class="card service-card">
          <span class="service-card__icon">{icon("i-map-pin", "icon icon-lg")}</span>
          <h3><a href="{url(s)}">Roofer in {esc(n)}, WI</a></h3>
          <p>{TOWN_BLURBS[s]}</p>
          <span class="service-card__more" aria-hidden="true">See {esc(n)} page {icon("i-arrow-right", "icon icon-sm")}</span>
        </article>""" for s, n in TOWNS)
    main = "\n  ".join([
        breadcrumbs(trail),
        page_hero("Areas We Serve",
                  "Hardtland is a roofer serving Dane County, WI, plus parts of Green and Rock counties. Our base is on Madison's southwest side, and we've worked across this area since 1972.",
                  eyebrow="Service areas"),
        f"""<section class="section">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Our main towns</p>
        <h2>Roofing in Dane County, WI</h2>
        <p>Pick your town to see local projects, the homes and roofs we see there, and notes on local storms.</p>
      </div>
      <div class="grid grid--3">
        {cards}
      </div>
    </div>
  </section>""",
        f"""<section class="section section--sand">
    <div class="container split">
      <div class="prose">
        <h2>Dane, Green &amp; Rock Counties</h2>
        <p>We also work in many smaller towns nearby, including Monona, McFarland, Stoughton, Belleville, New Glarus and Cross Plains, plus other communities in Dane, Green and Rock counties.</p>
        <p>Don't see your town? Call or text Tom at <a href="{TEL}">{PHONE}</a>. If we can get to you, we'll set up a free inspection.</p>
        <h3>Services in every town</h3>
        <ul class="link-list">{"".join(f'<li><a href="{url(s)}">{icon(SERVICE_ICON[s])}{esc(n)}</a></li>' for s, n in SERVICES)}</ul>
      </div>
      <aside class="split__aside">
        {map_embed("Dane County, WI", "Map of Dane County, Wisconsin", 9)}
      </aside>
    </div>
  </section>""",
        form_band(path),
    ])
    return path, render(path, "Service Areas | Roofer in Dane County WI | Hardtland",
                        "Towns we serve across Dane, Green and Rock counties, with links to each local page.",
                        main, schemas=[breadcrumb_ld(trail)])


# ==========================================================================
# REVIEWS
# ==========================================================================
@add
def reviews():
    path = "/reviews/"
    trail = [("Home", "/"), ("Reviews", path)]
    main = "\n  ".join([
        breadcrumbs(trail),
        page_hero("What Our Customers Say",
                  "Hardtland Home Improvement reviews from homeowners in Madison, Verona and nearby. We're rated {{RATING}} out of 5 stars on Google from {{REVIEWS}} reviews.",
                  eyebrow="Reviews", cta_label="Leave Us a Review", cta_href=GOOGLE_REVIEWS),
        f"""<!-- Review text is word for word from Google. Replace excerpts with the full text before launch.
       Optional: add a lightweight Google review feed here later (avoid heavy widgets that slow the page). -->
  <section class="section" aria-labelledby="reviews-title">
    <div class="container">
      <div class="section-head">
        <h2 id="reviews-title">Hardtland Reviews From Real Homeowners</h2>
        <div class="rating-summary">
          <span class="rating-summary__score">{RATING}</span>{stars()}
          <span>{RATING} out of 5 stars on Google, from {REVIEW_COUNT} reviews</span>
        </div>
      </div>
      <div class="grid grid--2">
        {review_cards(["cherise", "charles", "sally", "teresa"])}
      </div>
    </div>
  </section>""",
        f"""<section class="section section--sand">
    <div class="container split">
      <div class="prose">
        <h2>What Reviewers Mention Most</h2>
        <p>Across our Google reviews, the same things come up again and again:</p>
        <ul class="check-list">
          <li>Siding replacement done well</li>
          <li>Help choosing the right shingles</li>
          <li>Quick completion</li>
          <li>Efficient, hard-working crews</li>
          <li>A clean job site when we're done</li>
        </ul>
        <p>We read every review, good and bad. If we ever fall short, we want to hear about it so we can make it right.</p>
      </div>
      <aside class="split__aside">
        <div class="callout">
          <span class="callout__icon">{icon("i-star")}</span>
          <h3>Worked with us?</h3>
          <p>A quick Google review helps your neighbors find a roofer they can trust. It only takes a minute.</p>
          <!-- TODO: swap for the direct "write a review" link -->
          <a class="btn btn--primary btn--block" href="{GOOGLE_REVIEWS}" target="_blank" rel="noopener">Leave a Google Review<span class="visually-hidden"> (opens in a new tab)</span></a>
        </div>
      </aside>
    </div>
  </section>""",
        form_band(path),
    ])
    return path, render(path, "Hardtland Home Improvement Reviews | 4.7 Stars on Google",
                        "Read what Madison and Verona homeowners say about Hardtland. 4.7 stars on Google.",
                        main, schemas=[breadcrumb_ld(trail)])


# ==========================================================================
# ABOUT
# ==========================================================================
@add
def about():
    path = "/about/"
    trail = [("Home", "/"), ("About", path)]
    main = "\n  ".join([
        breadcrumbs(trail),
        page_hero("Owner-Run Since 1972",
                  "Hardtland Home Improvement has been a roofer since 1972, owned and run by Tom Degenhardt. Tom is a CertainTeed Master Shingler, and he's still on every job.",
                  eyebrow="About us"),
        f"""<section class="section">
    <div class="container why">
      <div class="why__photo">
        <!-- PHOTO NEEDED: Tom with the Hardtland trailer -->
        {photo("tom-degenhardt-hardtland-trailer.webp", "Tom Degenhardt, owner of Hardtland Home Improvement, standing by the company trailer in Madison, WI", 720, 900)}
        <div class="why__badge"><strong>1972</strong><span>Year Tom started Hardtland</span></div>
      </div>
      <div class="prose">
        <p class="eyebrow">Meet Tom</p>
        <h2>A Roofer Since 1972, Still on Every Job</h2>
        <p>Tom Degenhardt started Hardtland Home Improvement in 1972. More than five decades later, he still runs the company, still meets homeowners himself, and still checks every job before we call it done.</p>
        <!-- ORIGIN STORY: replace the line below with the confirmed story from Tom.
             The old site mentions "Bremen, Indiana" — confirm before using. -->
        <p class="placeholder-note">[CONFIRMED STORY FROM TOM]</p>
        <p>Customers describe Tom as friendly, calm and honest. He answers his own texts, gives straight answers, and would rather tell you a repair is enough than sell you a roof you don't need.</p>
      </div>
    </div>
  </section>""",
        f"""<section class="section section--sand" aria-labelledby="values-title">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">How we work</p>
        <h2 id="values-title">Honest, Clean, Local</h2>
      </div>
      <div class="grid grid--3">
        <div class="card feature"><span class="service-card__icon">{icon("i-user-check")}</span><h3>Honest</h3><p>Photos of what we find, a clear written quote, and a straight repair-or-replace answer. No pressure.</p></div>
        <div class="card feature"><span class="service-card__icon">{icon("i-check-circle")}</span><h3>Clean</h3><p>We pick up old shingles, nails and scraps every day. Your yard should look like we were never there.</p></div>
        <div class="card feature"><span class="service-card__icon">{icon("i-map-pin")}</span><h3>Local</h3><p>Based in Madison since 1972. Not a storm chaser. We'll be here long after your roof is done.</p></div>
      </div>
    </div>
  </section>""",
        f"""<section class="section" aria-labelledby="cert-title">
    <div class="container split">
      <div class="prose">
        <p class="eyebrow">Certifications</p>
        <h2 id="cert-title">Certified, Licensed &amp; Insured</h2>
        <ul class="check-list">
          <li><strong>CertainTeed Master Shingler</strong>, trained to install CertainTeed shingles to the manufacturer's standards</li>
          <li><strong>Owens Corning Certified</strong> contractor</li>
          <li><strong>Licensed in Wisconsin</strong></li>
          <li><strong>Licensed, bonded and insured</strong></li>
        </ul>
        <p>We accept insurance payments, personal checks, cash and Zelle.</p>
      </div>
      <aside class="split__aside">
        <div class="badge-row">
          {photo("badge-certainteed-master-shingler.webp", "CertainTeed Master Shingler certification badge", 240, 120)}
          {photo("badge-owens-corning-certified.webp", "Owens Corning Certified contractor badge", 240, 120)}
        </div>
      </aside>
    </div>
  </section>""",
        f"""<section class="section section--sand" aria-labelledby="reviews-title">
    <div class="container">
      <div class="section-head"><p class="eyebrow">In their words</p><h2 id="reviews-title">What Customers Say About Tom</h2></div>
      <div class="grid grid--2">{review_cards(["cherise", "teresa"])}</div>
    </div>
  </section>""",
        form_band(path),
    ])
    return path, render(path, "About Tom Degenhardt & Hardtland | Roofing Since 1972",
                        "Owner-run since 1972. Meet Tom Degenhardt, a CertainTeed Master Shingler serving Madison and Verona.",
                        main, schemas=[TOM_LD, breadcrumb_ld(trail)],
                        page_extra={"mainEntity": {"@id": DOMAIN + "/about/#tom"}})


# ==========================================================================
# GALLERY
# ==========================================================================
GALLERY = [
    ("roofing", "roof-replacement-verona-1.webp", "Completed asphalt shingle roof replacement on a ranch home in Verona, WI", "<strong>Roof replacement</strong>, Verona"),
    ("roofing", "roof-replacement-madison-2.webp", "New architectural shingle roof on a two-story home in Madison, WI", "<strong>Roof replacement</strong>, Madison"),
    ("siding", "siding-replacement-fitchburg-1.webp", "New vinyl siding with fresh soffit and fascia on a home in Fitchburg, WI", "<strong>Siding replacement</strong>, Fitchburg"),
    ("roofing", "storm-damage-roof-middleton-1.webp", "New roof installed after hail damage on a two-story home in Middleton, WI", "<strong>Hail damage roof</strong>, Middleton"),
    ("roofing", "metal-roof-oregon-1.webp", "Standing seam metal roof installed on a home in Oregon, WI", "<strong>Metal roof</strong>, Oregon"),
    ("gutters", "gutters-mount-horeb-1.webp", "Seamless gutters with leaf guards on a home in Mount Horeb, WI", "<strong>Gutters &amp; leaf guards</strong>, Mount Horeb"),
    ("siding", "siding-fiber-cement-madison-1.webp", "Fiber cement siding installed on a home in Madison, WI", "<strong>Fiber cement siding</strong>, Madison"),
    ("roofing", "roof-repair-madison-1.webp", "Repaired section of shingle roof after a leak fix on a home in Madison, WI", "<strong>Roof repair</strong>, Madison"),
    ("gutters", "gutters-verona-1.webp", "New seamless gutters and downspouts on a home in Verona, WI", "<strong>Seamless gutters</strong>, Verona"),
    ("siding", "soffit-fascia-middleton-1.webp", "New soffit and fascia on a home in Middleton, WI", "<strong>Soffit &amp; fascia</strong>, Middleton"),
    ("windows", "windows-madison-1.webp", "New replacement windows on a home in Madison, WI", "<strong>Replacement windows</strong>, Madison"),
    ("gutters", "gutter-guards-fitchburg-1.webp", "Gutter guards installed on a home with tall trees in Fitchburg, WI", "<strong>Gutter guards</strong>, Fitchburg"),
]


@add
def gallery():
    path = "/gallery/"
    trail = [("Home", "/"), ("Gallery", path)]
    filters = [("all", "All"), ("roofing", "Roofing"), ("siding", "Siding"),
               ("gutters", "Gutters"), ("windows", "Windows &amp; Doors")]
    btns = "".join(
        f'<button type="button" class="filter-btn" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{lbl}</button>'
        for k, lbl in filters)
    items = "\n".join(
        f"""        <li data-cat="{cat}">
          <figure class="project">
            {photo(f, alt)}
            <figcaption>{icon("i-map-pin")}<span>{cap}</span></figcaption>
          </figure>
        </li>""" for cat, f, alt, cap in GALLERY)
    main = "\n  ".join([
        breadcrumbs(trail),
        page_hero("Our Recent Projects",
                  "Roofing and siding projects we've installed across Madison, Verona and Dane County. Every photo is a real Hardtland job.",
                  eyebrow="Gallery"),
        f"""<!-- PHOTOS NEEDED: swap in Tom's 20+ gallery photos and his Google photos.
       Caption each with the job type and town. Add data-cat="roofing|siding|gutters|windows". -->
  <section class="section" aria-labelledby="gallery-title">
    <div class="container">
      <h2 id="gallery-title" class="visually-hidden">Roofing &amp; siding project photos</h2>
      <div class="filter-bar" role="group" aria-label="Filter projects">{btns}</div>
      <p class="visually-hidden" aria-live="polite" id="gallery-status"></p>
      <ul class="projects" id="gallery-grid">
{items}
      </ul>
    </div>
  </section>""",
        form_band(path, heading="Want Results Like These?"),
    ])
    return path, render(path, "Roofing & Siding Projects | Hardtland Gallery",
                        "Real roofs and siding we've installed across Madison, Verona and Dane County.",
                        main, schemas=[breadcrumb_ld(trail)],
                        page_extra={"image": [{"@type": "ImageObject", "contentUrl": f"{DOMAIN}/img/{f}",
                                               "caption": html.unescape(re.sub("<[^>]+>", "", cap))}
                                              for _, f, _, cap in GALLERY]})


# ==========================================================================
# FAQ
# ==========================================================================
FAQ_GROUPS = [
    ("Cost &amp; Timing", "faq-cost", [
        ("How much does a new roof cost in Wisconsin?",
         'It depends on your roof\'s size and pitch, how many old layers come off, the material you pick and any repairs needed underneath. We don\'t quote prices over the phone. We measure during a free inspection and give you a written estimate. <a href="/roof-replacement/">What affects roof cost</a>.'),
        ("What time of year is cheapest to replace a roof?",
         "Prices depend more on materials and labor than the season. Booking early, before the busy storm season, gives you more choice of dates. Shingles seal best in warm weather, so we plan around the forecast."),
        ("How long does a roof replacement take?",
         "Many homes are done in a day or two. Bigger or steeper roofs, extra layers and weather can add time. We'll give you an expected schedule with your estimate."),
        ("How long does a shingle roof last in Wisconsin?",
         "Many asphalt shingle roofs here last somewhere around 20 to 30 years. Ventilation, shingle quality, trees and hail all affect it."),
        ("How long does a metal roof last in Wisconsin?",
         'A well-installed metal roof often lasts 40 years or more. <a href="/metal-roofing/">More on metal roofing</a>.'),
    ]),
    ("Insurance &amp; Storms", "faq-insurance", [
        ("Do you work with my insurance company?",
         'Yes. We work with all insurance companies. We photograph the damage and help you through the claim. <a href="/insurance-claims/">How claim help works</a>.'),
        ("Does insurance go up if you claim hail damage?",
         "It depends on your insurer and policy. Ask your insurance agent before you file."),
        ("Will insurance cover a metal roof?",
         "Insurance usually pays to replace what you had. Upgrading from shingles to metal may mean paying the difference. Ask your agent, and we'll price both."),
        ("What should I do right after a hailstorm?",
         'Stay safe, take photos, stop any leaks if you safely can, and call for a free inspection. See our <a href="/storm-hail-damage/">first-48-hours checklist</a>.'),
    ]),
    ("Repairs &amp; Inspections", "faq-repairs", [
        ("Is a roof inspection free?",
         'Yes. Our roof and exterior inspections are free, with no pressure. <a href="/free-roof-inspection/">Book one here</a>.'),
        ("Can you repair just a section of a roof?",
         "Often, yes. If the damage is in one area, we can repair that section and match the shingles as closely as we can."),
        ("What is the 25% rule for roofing?",
         "In some places, codes or insurers say that if more than about 25% of a roof is repaired or replaced in a year, the whole roof must meet current code. Rules vary, and we'll tell you what applies to your home."),
        ("How can you tell if a roof needs to be replaced?",
         "Curling or cracked shingles, bare spots, leaks in several places and a sagging deck are common signs. We'll show you photos so you can see for yourself."),
    ]),
    ("Siding, Gutters &amp; Windows", "faq-exterior", [
        ("Siding repair or replacement?",
         'Damage in a few spots can usually be repaired. Siding that is faded, warped or leaking all over is usually worth replacing. <a href="/siding/">More on siding</a>.'),
        ("Are gutter guards worth it?",
         'For many homes with trees nearby, yes. They cut down on clogs and ladder trips, though no guard is completely maintenance-free. <a href="/gutters/">More on gutters</a>.'),
    ]),
    ("Working With Hardtland", "faq-working", [
        ("What warranty do I get?",
         "It depends on the products and the job. Tom will explain the manufacturer warranty and our workmanship coverage in writing with your estimate."),
        ("Are you licensed and insured?",
         "Yes. We're licensed in Wisconsin, and licensed, bonded and insured. Tom is a CertainTeed Master Shingler and we're Owens Corning Certified."),
        ("What forms of payment do you accept?",
         "Insurance, personal checks, cash and Zelle."),
        ("What areas do you serve?",
         'Verona, Madison, Fitchburg, Middleton, Oregon, Mount Horeb and other towns in Dane, Green and Rock counties. <a href="/service-areas/">See all service areas</a>.'),
    ]),
]


@add
def faq():
    path = "/faq/"
    trail = [("Home", "/"), ("FAQ", path)]
    all_faqs = [qa for _, _, qs in FAQ_GROUPS for qa in qs]
    jump = "".join(f'<li><a href="#{hid}">{t}</a></li>' for t, hid, _ in FAQ_GROUPS)
    groups = "\n".join(
        f"""<div class="faq-group">
        <h2 id="{hid}">{t}</h2>
        <div class="faq">""" + "".join(
            f"""
          <details class="faq-item">
            <summary>{esc(q)} {icon("i-plus")}</summary>
            <div class="faq-item__body"><p>{a}</p></div>
          </details>""" for q, a in qs) + "\n        </div>\n      </div>"
        for t, hid, qs in FAQ_GROUPS)
    main = "\n  ".join([
        breadcrumbs(trail),
        page_hero("Roofing Questions, Answered",
                  "Straight answers to common roofing questions about costs, insurance claims, timing and warranties, from a Madison roofer since 1972.",
                  eyebrow="FAQ"),
        f"""<section class="section">
    <div class="container faq-page">
      <nav class="faq-jump" aria-label="FAQ topics"><ul>{jump}</ul></nav>
      {groups}
      <p class="faq-foot">Have a question we didn't answer? Call or text Tom at <a href="{TEL}">{PHONE}</a>.</p>
    </div>
  </section>""",
        form_band(path),
    ])
    return path, render(path, "Roofing FAQ | Costs, Insurance & Timing | Hardtland",
                        "Straight answers about roof costs, insurance claims, timing and warranties from a Madison roofer since 1972.",
                        main, schemas=[faq_ld(all_faqs), breadcrumb_ld(trail)])


# ==========================================================================
# CONTACT
# ==========================================================================
@add
def contact():
    path = "/contact/"
    trail = [("Home", "/"), ("Contact", path)]
    main = "\n  ".join([
        breadcrumbs(trail),
        page_hero("Get Your Free Inspection",
                  f"Contact Hardtland for a free roof inspection. Call or text Tom at {PHONE}, or fill out the form and we'll call you back within 1 business day.",
                  eyebrow="Contact", buttons=False),
        f"""<section class="section" id="free-inspection">
    <div class="container contact-grid">
      <div class="form-card form-card--inline">
        <h2 class="h3-like">Book a Free Inspection</h2>
        <p>Takes about 30 seconds.</p>
        {form(path, None, "c")}
      </div>
      <div class="contact-list">
        <h2 class="h3-like">Contact Hardtland</h2>
        <ul>
          <li>{icon("i-phone")}<div><strong>Call</strong><a href="{TEL}">{PHONE}</a></div></li>
          <li>{icon("i-message")}<div><strong>Text Tom</strong><a href="{SMS}">{PHONE}</a></div></li>
          <li>{icon("i-mail")}<div><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
          <li>{icon("i-map-pin")}<div><strong>Address</strong><span>5821 Thrush Ln<br>Madison, WI 53711</span></div></li>
          <li>{icon("i-clock")}<div><strong>Hours</strong><span>{HOURS}</span></div></li>
          <li>{icon("i-wallet")}<div><strong>Payment</strong><span>Insurance, personal checks, cash and Zelle</span></div></li>
        </ul>
      </div>
    </div>
  </section>""",
        f"""<section class="section section--sand">
    <div class="container">
      <h2 class="h3-like">Where we're based</h2>
      {map_embed("Hardtland Home Improvement, 5821 Thrush Ln, Madison, WI 53711", "Map of Hardtland Home Improvement at 5821 Thrush Ln, Madison, WI", 12)}
    </div>
  </section>""",
    ])
    return path, render(path, "Contact Hardtland | Free Roof Inspection | (608) 575-9317",
                        "Call or text (608) 575-9317 or book a free inspection online. 5821 Thrush Ln, Madison, WI 53711.",
                        main, schemas=[breadcrumb_ld(trail)])


# ==========================================================================
# PRIVACY + ACCESSIBILITY + 404
# ==========================================================================
@add
def privacy():
    path = "/privacy-policy/"
    trail = [("Home", "/"), ("Privacy Policy", path)]
    body = f"""<div class="prose">
      <!-- TODO: have this reviewed before launch, and update it if analytics or a form service is added. -->
      <p>This page explains what information Hardtland Home Improvement, Inc. collects through this website and how we use it.</p>
      <h2>What we collect</h2>
      <p>When you fill out our inspection form, we collect your name, phone number, address and the service you're interested in. If you call, text or email us, we receive the information you share.</p>
      <h2>How we use it</h2>
      <p>We use your information only to contact you about your project, schedule inspections and provide estimates and service. We do not sell your information.</p>
      <h2>Website data and analytics</h2>
      <p>Like most websites, our hosting provider may log basic technical data such as your browser type and pages visited.</p>
      <p>We may use Google Analytics to understand how people find and use our site, such as which pages are visited and when someone taps to call or text us. Google Analytics uses cookies and collects data under <a href="https://policies.google.com/privacy" rel="noopener">Google's privacy policy</a>. You can opt out with <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener">Google's opt-out browser add-on</a>.</p>
      <h2>Embedded maps</h2>
      <p>Some pages include Google Maps. Google may collect data when you view or use these maps, under Google's own privacy policy.</p>
      <h2>Contact us</h2>
      <p>Questions about your information? Call <a href="{TEL}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </div>"""
    main = "\n  ".join([breadcrumbs(trail),
                        page_hero("Privacy Policy", "How we handle the information you share with us.", buttons=False),
                        simple_section(body)])
    return path, render(path, "Privacy Policy | Hardtland Home Improvement",
                        "How Hardtland Home Improvement collects and uses information shared through this website.",
                        main, schemas=[breadcrumb_ld(trail)])


@add
def accessibility():
    path = "/accessibility/"
    trail = [("Home", "/"), ("Accessibility", path)]
    body = f"""<div class="prose">
      <p>Hardtland Home Improvement wants everyone to be able to use this website. We built it to meet the Web Content Accessibility Guidelines (WCAG) 2.1 Level AA.</p>
      <h2>What we've done</h2>
      <ul>
        <li>Text and buttons with strong color contrast</li>
        <li>Every page works with a keyboard, with visible focus outlines</li>
        <li>Labels on every form field</li>
        <li>Descriptive text for every image</li>
        <li>Large tap targets on phones</li>
        <li>No pop-ups or floating widgets that cover the content</li>
      </ul>
      <h2>Need help?</h2>
      <p>If anything on this site is hard to use, please call or text <a href="{TEL}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>. We'll help you directly and fix the problem.</p>
    </div>"""
    main = "\n  ".join([breadcrumbs(trail),
                        page_hero("Accessibility", "Our commitment to a website everyone can use.", buttons=False),
                        simple_section(body)])
    return path, render(path, "Accessibility Statement | Hardtland Home Improvement",
                        "Hardtland's commitment to an accessible website, and how to reach us if you need help.",
                        main, schemas=[breadcrumb_ld(trail)])


@add
def thank_you():
    path = "/thank-you/"
    body = f"""<div class="prose">
      <p>Tom or the crew will call you back within 1 business day to set up your free inspection.</p>
      <p>Need us sooner? Call or text Tom at <a href="{TEL}">{PHONE}</a>.</p>
      <h2 class="h3-like">While you wait</h2>
      <ul class="link-list">
        <li><a href="/reviews/">{icon("i-star")}Read what customers say</a></li>
        <li><a href="/gallery/">{icon("i-camera")}See recent projects</a></li>
        <li><a href="/storm-hail-damage/">{icon("i-hail")}What to do after a storm</a></li>
      </ul>
    </div>"""
    main = "\n  ".join([page_hero("Thanks! We Got Your Request", "Your free inspection request is on its way to Tom.", buttons=False),
                        simple_section(body)])
    return path, render(path, "Thank You | Hardtland Home Improvement",
                        "Thanks for requesting a free inspection from Hardtland Home Improvement.",
                        main, robots="noindex")


@add
def not_found():
    path = "/404.html"
    body = f"""<div class="prose">
      <p>The page you're looking for may have moved. Here are some good places to start:</p>
      <ul class="link-list">
        <li><a href="/">{icon("i-home")}Home</a></li>
        <li><a href="/free-roof-inspection/">{icon("i-search")}Free Roof Inspection</a></li>
        <li><a href="/service-areas/">{icon("i-map-pin")}Service Areas</a></li>
        <li><a href="/contact/">{icon("i-phone")}Contact</a></li>
      </ul>
    </div>"""
    main = "\n  ".join([page_hero("Page Not Found", f"Sorry, we couldn't find that page. Call or text Tom at {PHONE} if you need help.", buttons=False),
                        simple_section(body)])
    return path, render(path, "Page Not Found | Hardtland Home Improvement",
                        "Sorry, we couldn't find that page.", main, robots="noindex")
