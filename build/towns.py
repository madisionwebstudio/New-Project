"""The 6 town pages. Each one is written separately so the local content is
unique (the plan asks for at least 60% unique copy per town).

TODO before launch:
  * Replace each town's 3 projects with REAL JOBS FROM TOM (photo + one line).
  * Double-check the drive distances from 5821 Thrush Ln.
"""
from common import (DOMAIN, BUSINESS_ID, esc, icon, url, render, breadcrumbs, breadcrumb_ld, page_hero,
                    faq_section, faq_ld, project_grid, form_band, map_embed,
                    review_cards, SERVICES, SERVICE_ICON, TOWNS, TEL, PHONE)

TOWN_DATA = {
    "verona-wi": dict(
        name="Verona",
        title="Roofer Verona WI | Hardtland Home Improvement",
        desc="Verona's local roofer since 1972. Roof replacement, repair, siding and storm damage. Free inspection, call (608) 575-9317.",
        lead="Verona's local roofer since 1972. Roof replacement, repair, siding and storm damage, with Tom Degenhardt on every job.",
        intro="""<p>Looking for a roofer in Verona, WI who will still be around in ten years? Hardtland Home Improvement has worked on Verona homes since 1972. Our base on the southwest side of Madison is only about 6 miles away, so we can get to you quickly for an inspection or a leak.</p>
        <p>Verona has grown a lot, and we've watched it happen. We work on everything from older homes near downtown and Main Street to the newer subdivisions that went up as the city grew. Whatever you live in, you'll deal with Tom, not a call center.</p>""",
        homes_h2="Roofs and Homes in Verona",
        homes="""<p>Many Verona homes were built in the same few decades, which means whole neighborhoods often reach roof-replacement age around the same time. If your neighbors are getting new roofs, it's a good time to have yours checked.</p>
        <p>Newer Verona homes often have architectural shingles and more complex rooflines, with valleys, dormers and multiple pitches. Those details need careful flashing to stay dry. Older homes may have more than one layer of shingles that need to come off before a new roof goes on.</p>""",
        storm="""<p>Verona sits right in the path of the storms that sweep east across southern Wisconsin in spring and summer. Hail and high wind can lift shingles and bruise them in ways you can't see from the ground. After a storm, call or text Tom for a free inspection. We'll photograph any damage and help with your insurance claim.</p>""",
        projects=[
            ("roof-replacement-verona-1.webp", "Completed asphalt shingle roof replacement on a ranch home in Verona, WI", "<strong>Roof replacement</strong>, Verona"),
            ("storm-damage-roof-verona-1.webp", "Roof replaced after a hailstorm on a home in Verona, WI", "<strong>Hail damage roof</strong>, Verona"),
            ("gutters-verona-1.webp", "New seamless gutters and downspouts on a home in Verona, WI", "<strong>Seamless gutters</strong>, Verona"),
        ],
        faqs=[
            ("How quickly can you get to my home in Verona?",
             "We're based about 6 miles away in southwest Madison, so Verona is close to home for us. Call or text Tom and we'll set up a time that works for you."),
            ("Do you need a permit to replace a roof in Verona?",
             "Permit rules depend on the city or town and the work being done. We'll check what's required for your address and take care of it as part of the job."),
        ],
        review="teresa",
        nearby=["madison-wi", "fitchburg-wi", "mount-horeb-wi"],
        map_q="Verona, WI", zoom=13,
    ),
    "madison-wi": dict(
        name="Madison",
        title="Roofer Madison WI | Roof Replacement & Repair",
        desc="Trusted Madison roofer since 1972. Shingle and metal roofs, storm repair and siding. Free inspection and estimate.",
        lead="A trusted Madison roofer since 1972. Shingle and metal roofs, storm repair and siding, from a family business based right here in town.",
        intro="""<p>Hardtland is a roofer in Madison, WI, and has been since 1972. Our base is on Madison's southwest side, so this is our hometown. We work across the whole city, from the west side neighborhoods near us to the near east side and north side.</p>
        <p>Madison homeowners hire us for roof replacement, roof repair, storm damage, siding and gutters. Tom Degenhardt runs every job, answers his own texts and gives you a straight answer about what your home needs.</p>""",
        homes_h2="Madison's Mix of Older and Newer Homes",
        homes="""<p>Madison has one of the widest ranges of homes in the area. Older neighborhoods have homes with steep roofs, dormers, chimneys and sometimes several layers of old shingles. Ranches and split-levels from the middle of the last century are common on the west and south sides. Newer homes on the edges of the city tend to have larger, more complex roofs.</p>
        <p>Older homes often need more care at the roof deck and around chimneys. We check the wood, replace soft boards and install new flashing, so the new roof has a solid base. Mature trees in many Madison neighborhoods also mean more clogged gutters, so we often pair roofs with <a href="/gutters/">gutter guards</a>.</p>""",
        storm="""<p>Spring and summer storms can bring hail and strong wind to Madison, and heavy winter snow leads to ice dams on many older homes. After a storm, a free inspection will tell you whether you have damage worth an insurance claim. If you have ice dams, we'll look at ventilation and insulation, not just the shingles.</p>""",
        projects=[
            ("roof-replacement-madison-2.webp", "New architectural shingle roof on a two-story home in Madison, WI", "<strong>Roof replacement</strong>, Madison"),
            ("roof-repair-madison-1.webp", "Repaired section of shingle roof after a leak fix on a home in Madison, WI", "<strong>Roof repair</strong>, Madison"),
            ("siding-fiber-cement-madison-1.webp", "Fiber cement siding installed on a home in Madison, WI", "<strong>Fiber cement siding</strong>, Madison"),
        ],
        faqs=[
            ("Do you work all over Madison?",
             "Yes. We're based on the southwest side and work across the whole city, plus the towns around it."),
            ("Can you work on older Madison homes with steep roofs?",
             "Yes. Steep roofs, dormers and old chimneys are common in Madison, and we've been working on them since 1972. We'll check the deck and flashing carefully before the new roof goes on."),
        ],
        review="cherise",
        nearby=["verona-wi", "fitchburg-wi", "middleton-wi"],
        map_q="Madison, WI", zoom=12,
    ),
    "fitchburg-wi": dict(
        name="Fitchburg",
        title="Roofer Fitchburg WI | Hardtland Home Improvement",
        desc="Roofing, siding and storm repair for Fitchburg homes from a nearby contractor since 1972. Free inspection.",
        lead="Roofing, siding and storm repair for Fitchburg homes, from a nearby contractor that has been doing it since 1972.",
        intro="""<p>Need a roofer in Fitchburg, WI? Hardtland is just up the road. Our base in southwest Madison is only about 5 miles from most of Fitchburg, so we can get there fast for a free inspection or a leak repair.</p>
        <p>Fitchburg is a mix of established neighborhoods off Fish Hatchery Road and newer subdivisions further south, plus rural homes with bigger lots. We work on all of them, and Tom Degenhardt is on every job.</p>""",
        homes_h2="Fitchburg Homes and What Their Roofs Need",
        homes="""<p>Many Fitchburg homes are newer than those in central Madison, but the first roof on a home from the 1990s or early 2000s may be near the end of its life now. Those are often the roofs we're replacing in Fitchburg today.</p>
        <p>Homes on larger, more open lots get the full force of the wind. That can mean lifted shingles, loose ridge caps and damaged siding. We check for wind damage on every inspection and replace soffit, fascia or siding if it's needed, all with one crew.</p>""",
        storm="""<p>Open land around parts of Fitchburg means storms can hit hard, with nothing to slow the wind. After hail or a big wind event, have your roof, siding and gutters checked. We'll document any damage with photos and help you work with your insurance company.</p>""",
        projects=[
            ("roof-replacement-fitchburg-1.webp", "Crew finishing a shingle roof replacement in Fitchburg, WI", "<strong>Roof replacement</strong>, Fitchburg"),
            ("siding-replacement-fitchburg-1.webp", "New vinyl siding with fresh soffit and fascia on a home in Fitchburg, WI", "<strong>Siding replacement</strong>, Fitchburg"),
            ("gutter-guards-fitchburg-1.webp", "Gutter guards installed on a home with tall trees in Fitchburg, WI", "<strong>Gutter guards</strong>, Fitchburg"),
        ],
        faqs=[
            ("Is my Fitchburg home's roof old enough to replace?",
             "If your home is from the 1990s or early 2000s and still has its first roof, it's worth a free inspection. We'll tell you honestly how much life it has left."),
            ("Do you also do siding in Fitchburg?",
             "Yes. We install and repair vinyl, fiber cement and metal siding, plus soffit and fascia."),
        ],
        review="sally",
        nearby=["madison-wi", "verona-wi", "oregon-wi"],
        map_q="Fitchburg, WI", zoom=13,
    ),
    "middleton-wi": dict(
        name="Middleton",
        title="Roofer Middleton WI | Roofing & Siding | Hardtland",
        desc="Roof replacement, repair and siding for Middleton homeowners. CertainTeed Master Shingler. Free estimate.",
        lead="Roof replacement, repair and siding for Middleton homeowners, from a CertainTeed Master Shingler that has been local since 1972.",
        intro="""<p>Hardtland is a roofer serving Middleton, WI homeowners from our base on Madison's west side, roughly 8 miles away. Since 1972, we've done roof replacements, repairs, siding and gutters for families all over the area.</p>
        <p>Middleton homeowners tend to care about quality and the details. That's a good fit for us. As a <strong>CertainTeed Master Shingler</strong> and <strong>Owens Corning Certified</strong> contractor, we install roofs to the manufacturer's standards, and Tom checks every job himself.</p>""",
        homes_h2="Middleton Homes, From Classic to Custom",
        homes="""<p>Middleton has older homes close to downtown, mid-century ranches, and larger newer homes with complex rooflines. Bigger homes often have several roof planes, valleys, dormers and skylights. Each of those spots needs careful flashing to stay watertight.</p>
        <p>Many Middleton homes are surrounded by mature trees, especially near parks and green spaces. Trees mean shade, moss, and clogged gutters. We look for those problems during every inspection and can add <a href="/gutters/">gutter guards</a> to help.</p>""",
        storm="""<p>Storms crossing Dane County regularly bring hail and wind through Middleton. Large trees can also drop limbs on roofs during a storm. If a storm or a fallen branch has damaged your roof, call or text Tom. We'll check it for free and help with your insurance claim if you need one.</p>""",
        projects=[
            ("storm-damage-roof-middleton-1.webp", "New roof installed after hail damage on a two-story home in Middleton, WI", "<strong>Hail damage roof</strong>, Middleton"),
            ("soffit-fascia-middleton-1.webp", "New soffit and fascia on a home in Middleton, WI", "<strong>Soffit &amp; fascia</strong>, Middleton"),
            ("windows-middleton-1.webp", "Replacement windows with new exterior trim in Middleton, WI", "<strong>Windows &amp; trim</strong>, Middleton"),
        ],
        faqs=[
            ("Can you handle a large, complex roof?",
             "Yes. Multiple roof planes, valleys, dormers and skylights are common in Middleton. Careful flashing in those spots is where experience counts."),
            ("Do you install premium shingles?",
             "We install CertainTeed and Owens Corning shingles, including higher-end lines. We'll show you options and prices side by side."),
        ],
        review="cherise",
        nearby=["madison-wi", "verona-wi", "mount-horeb-wi"],
        map_q="Middleton, WI", zoom=13,
    ),
    "oregon-wi": dict(
        name="Oregon",
        title="Roofer Oregon WI | Hardtland Home Improvement",
        desc="Local roofing and siding for Oregon, WI homes since 1972. Storm damage help and free inspections.",
        lead="Local roofing and siding for Oregon, WI homes since 1972. Storm damage help and free inspections from a Dane County roofer.",
        intro="""<p>If you're looking for a roofer in Oregon, WI, Hardtland is a short drive away. Our base in southwest Madison is about 12 miles from Oregon, and we've been working on homes across southern Dane County since 1972.</p>
        <p>Oregon has a small-town feel, with older homes near the village center and newer subdivisions around the edges. We work on both, plus rural homes, garages and outbuildings in the countryside nearby.</p>""",
        homes_h2="Homes and Roofs Around Oregon",
        homes="""<p>Older homes near downtown Oregon often have steeper roofs, chimneys and sometimes more than one layer of old shingles. Newer homes may still have their first roof, which may be getting close to replacement age.</p>
        <p>Rural properties around Oregon often have barns, sheds and garages too. Metal roofing is a popular choice for those buildings, and for homes where owners want a roof that sheds snow and lasts. See our <a href="/metal-roofing/">metal roofing</a> page.</p>""",
        storm="""<p>Southern Dane County gets its share of hail and strong wind, and open farmland around Oregon gives storms room to build. Wind damage often shows up as lifted shingles and loose siding. After a storm, we'll do a free inspection, take photos and help with your claim.</p>""",
        projects=[
            ("metal-roof-oregon-1.webp", "Standing seam metal roof installed on a home in Oregon, WI", "<strong>Metal roof</strong>, Oregon"),
            ("storm-damage-siding-oregon-1.webp", "Siding replaced after wind damage on a home in Oregon, WI", "<strong>Wind damage siding</strong>, Oregon"),
            ("roof-replacement-oregon-1.webp", "Shingle roof replacement on a home in Oregon, WI", "<strong>Roof replacement</strong>, Oregon"),
        ],
        faqs=[
            ("Do you roof garages and outbuildings around Oregon?",
             "Yes. Ask about garages, sheds and outbuildings when we come out. Metal is often a good fit for those."),
            ("Will you come out to rural homes near Oregon?",
             "Yes. We serve Oregon and the countryside around it as part of our Dane County service area."),
        ],
        review="charles",
        nearby=["fitchburg-wi", "verona-wi", "madison-wi"],
        map_q="Oregon, WI", zoom=13,
    ),
    "mount-horeb-wi": dict(
        name="Mount Horeb",
        title="Roofer Mount Horeb WI | Hardtland Home Improvement",
        desc="Roofing, siding and storm repair for Mount Horeb homes. Free inspection from a Dane County roofer since 1972.",
        lead="Roofing, siding and storm repair for Mount Horeb homes. Free inspection from a Dane County roofer since 1972.",
        intro="""<p>Hardtland serves Mount Horeb, WI as part of our western Dane County service area. We're about 17 miles east, on Madison's southwest side, and we've been roofing in this part of Wisconsin since 1972.</p>
        <p>Mount Horeb homeowners call us for roof replacement, roof repair, storm damage, siding and gutters. Tom Degenhardt is on every job, so you always know who you're dealing with.</p>""",
        homes_h2="Roofs in the Hills West of Madison",
        homes="""<p>Mount Horeb sits up on the ridge west of Madison, and homes on higher, open ground take more wind than homes in town. That means checking ridge caps, roof edges and siding carefully for wind damage.</p>
        <p>You'll find older homes near the historic downtown, newer neighborhoods on the edges of the village, and rural homes with outbuildings nearby. Many rural owners choose <a href="/metal-roofing/">metal roofing</a> for its long life and how well it sheds snow.</p>""",
        storm="""<p>Storms often build as they move across the hills west of Madison, and Mount Horeb can see strong wind and hail. Winter brings heavy snow and ice dams. After any big storm, call or text Tom for a free inspection and help with your insurance claim.</p>""",
        projects=[
            ("gutters-mount-horeb-1.webp", "Seamless gutters with leaf guards on a home in Mount Horeb, WI", "<strong>Gutters &amp; leaf guards</strong>, Mount Horeb"),
            ("metal-roof-mount-horeb-1.webp", "Metal roof on a farmhouse-style home near Mount Horeb, WI", "<strong>Metal roof</strong>, Mount Horeb"),
        ],
        faqs=[
            ("Do you travel to Mount Horeb for small repairs?",
             "Yes. Call or text Tom and tell us what's going on. We'll set up a time to come out."),
            ("What roof holds up best to wind on the ridge?",
             "A properly installed roof, shingle or metal, with the right nailing and good ridge caps, holds up well. We'll talk through which makes sense for your home."),
        ],
        review="sally",
        nearby=["verona-wi", "middleton-wi", "madison-wi"],
        map_q="Mount Horeb, WI", zoom=13,
    ),
}


def town_page(slug):
    d = TOWN_DATA[slug]
    name = d["name"]
    path = url(slug)
    trail = [("Home", "/"), ("Service Areas", "/service-areas/"), (f"{name}, WI", path)]

    svc_links = "".join(
        f'<li><a href="{url(s)}">{icon(SERVICE_ICON[s])}<span><strong>{esc(n)}</strong> in {esc(name)}</span></a></li>'
        for s, n in SERVICES)
    nearby = "".join(
        f'<li><a href="{url(s)}">{icon("i-map-pin")}Roofer in {esc(dict(TOWNS)[s])}, WI</a></li>'
        for s in d["nearby"])

    main = "\n  ".join([
        breadcrumbs(trail),
        page_hero(f"Roofer in {esc(name)}, WI", d["lead"], eyebrow=f"Serving {name}"),
        f"""<section class="section">
    <div class="container split">
      <div class="prose">
        <h2>Your Local Roofer in {esc(name)}</h2>
        {d["intro"]}
      </div>
      <aside class="split__aside">
        {review_cards([d["review"]])}
      </aside>
    </div>
  </section>""",
        f"""<section class="section section--sand">
    <div class="container"><div class="prose">
      <h2>{esc(d["homes_h2"])}</h2>
      {d["homes"]}
    </div></div>
  </section>""",
        f"""<!-- REAL JOBS FROM TOM: replace with 2-3 actual {name} projects (photo + one line each) -->
  <section class="section" aria-labelledby="projects-title">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Local work</p>
        <h2 id="projects-title">Recent Projects in {esc(name)}</h2>
      </div>
      {project_grid(d["projects"])}
    </div>
  </section>""",
        f"""<section class="section section--sand" aria-labelledby="svc-title">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Services</p>
        <h2 id="svc-title">Roofing &amp; Exterior Services in {esc(name)}</h2>
        <p>Everything we offer is available to {esc(name)} homeowners. Pick a service to learn more.</p>
      </div>
      <ul class="link-list link-list--grid">{svc_links}</ul>
    </div>
  </section>""",
        f"""<section class="section">
    <div class="container split">
      <div class="prose">
        <p class="eyebrow">Storms</p>
        <h2>Storm &amp; Hail Damage in {esc(name)}</h2>
        {d["storm"]}
        <p><a class="text-link" href="/storm-hail-damage/">What to do after a storm {icon("i-arrow-right", "icon icon-sm")}</a></p>
      </div>
      <aside class="split__aside">
        {map_embed(d["map_q"], f"Map of {name}, WI", d["zoom"])}
      </aside>
    </div>
  </section>""",
        faq_section(d["faqs"], title=f"{name} Roofing Questions"),
        f"""<section class="section" aria-labelledby="nearby-title">
    <div class="container">
      <h2 id="nearby-title" class="h3-like">Nearby towns we serve</h2>
      <ul class="link-list link-list--row">{nearby}<li><a href="/service-areas/">{icon("i-map-pin")}All service areas</a></li></ul>
    </div>
  </section>""",
        form_band(path, heading=f"Free Roof Inspection in {name}"),
    ])
    local_service = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"Roofing in {name}, WI",
        "serviceType": "Roofing contractor",
        "description": d["desc"],
        "url": DOMAIN + path,
        "provider": {"@id": BUSINESS_ID},
        "areaServed": {"@type": "City", "name": f"{name}, WI",
                       "containedInPlace": {"@type": "State", "name": "Wisconsin"}},
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": f"Roofing and exterior services in {name}",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n,
                                 "url": DOMAIN + url(s)}} for s, n in SERVICES],
        },
    }
    schemas = [local_service, faq_ld(d["faqs"]), breadcrumb_ld(trail)]
    return path, render(path, d["title"], d["desc"], main, schemas=schemas)


PAGES = [lambda s=s: town_page(s) for s, _ in TOWNS]
