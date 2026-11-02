"""The 9 service pages. Each follows the same template:
H1 > intro + button > what's included > signs > 4 steps > photos > reviews >
FAQs > related services + towns > form band.
"""
from common import (esc, form, icon, url, render, breadcrumbs, breadcrumb_ld, page_hero,
                  faq_section, faq_ld, reviews_section, projects_section,
                  steps_section, related_section, form_band, service_ld, TEL, PHONE)


# ---------- section helpers ----------
def prose(h2, body, band=False, aside=None, eyebrow=None, h_id=None):
    cls = "section section--sand" if band else "section"
    hid = f' id="{h_id}"' if h_id else ""
    eb = f'<p class="eyebrow">{esc(eyebrow)}</p>' if eyebrow else ""
    if aside:
        return f"""<section class="{cls}">
    <div class="container split">
      <div class="prose">{eb}<h2{hid}>{h2}</h2>{body}</div>
      <aside class="split__aside">{aside}</aside>
    </div>
  </section>"""
    return f"""<section class="{cls}">
    <div class="container"><div class="prose">{eb}<h2{hid}>{h2}</h2>{body}</div></div>
  </section>"""


def features(h2, lead, items, band=False, eyebrow="What's included"):
    cls = "section section--sand" if band else "section"
    cards = "\n".join(
        f"""        <div class="card feature">
          <span class="service-card__icon">{icon(ic, "icon")}</span>
          <h3>{esc(t)}</h3>
          <p>{txt}</p>
        </div>""" for ic, t, txt in items)
    cols = "grid--3" if len(items) % 3 == 0 else "grid--2"
    return f"""<section class="{cls}">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">{esc(eyebrow)}</p>
        <h2>{h2}</h2>
        <p>{lead}</p>
      </div>
      <div class="grid {cols}">
{cards}
      </div>
    </div>
  </section>"""


def checklist(items):
    return '<ul class="check-list">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def callout(title, body, ic="i-phone", button=True):
    btn = (f'<a class="btn btn--primary btn--block" href="#free-inspection">Book a Free Inspection</a>'
           f'<a class="btn btn--outline btn--block" href="{TEL}">{icon("i-phone", "icon icon-sm")} Call {PHONE}</a>'
           if button else "")
    return f"""<div class="callout">
        <span class="callout__icon">{icon(ic)}</span>
        <h3>{esc(title)}</h3>
        <p>{body}</p>
        {btn}
      </div>"""


def service_page(slug, *, title, desc, h1, crumb, lead, body, faqs, related, towns,
                 select, schema_name, eyebrow):
    path = url(slug)
    trail = [("Home", "/"), (crumb, path)]
    main = "\n  ".join([
        breadcrumbs(trail),
        page_hero(h1, lead, eyebrow=eyebrow),
        *body,
        faq_section(faqs, title="Questions We Hear a Lot"),
        related_section(related, towns),
        form_band(path, select=select),
    ])
    schemas = [service_ld(schema_name, slug, desc), faq_ld(faqs), breadcrumb_ld(trail)]
    return path, render(path, title, desc, main, schemas=schemas)


STD_STEPS = [
    ("Free inspection", "Tom or the crew looks over your roof and takes photos. It's free, and there's no pressure."),
    ("Photo report + honest quote", "You see what we found and get a clear written quote. Repair or replace, we tell you straight."),
    ("We help with insurance", "If storm damage is part of it, we help you with the claim. We work with all insurance companies."),
    ("Install + clean-up", "Our crew does the work, cleans up every day, and Tom walks the finished job with you."),
]

PAGES = []


def add(fn):
    PAGES.append(fn)
    return fn


# ==========================================================================
# ROOF REPLACEMENT
# ==========================================================================
@add
def roof_replacement():
    faqs = [
        ("How much does a new roof cost in Wisconsin?",
         "It depends on your roof. The size, the pitch, how many old layers come off and the material you choose all change the price. We don't quote prices over the phone, because a guess helps no one. We measure your roof during a free inspection and give you a written estimate with every part listed."),
        ("How long does a shingle roof last in Wisconsin?",
         "Many asphalt shingle roofs here last somewhere around 20 to 30 years. Attic ventilation, the shingle you pick, tree cover and hail all make a big difference. During an inspection, Tom will tell you honestly how much life your roof has left."),
        ("How can you tell if a roof needs to be replaced?",
         "Common signs are curling or cracked shingles, bare spots where the granules are gone, leaks in more than one place, and a sagging roof deck. One problem spot usually means a repair. Problems all over usually mean it's time. We'll show you photos so you can see it yourself."),
        ("What time of year is cheapest to replace a roof?",
         "Prices are set by materials and labor more than the calendar. That said, booking early, before the busy summer and storm season, gives you more choice of dates. Shingles seal best in warm weather, so we plan installs around the forecast."),
        ("Can you put new shingles over my old ones?",
         "Sometimes code allows a second layer, but we usually recommend tearing off down to the deck. That lets us check the wood, fix soft spots and install the new roof the way the manufacturer expects. We'll talk through both options with you."),
    ]
    body = [
        prose("Roof Replacement in Madison, WI, Done Right the First Time", """
        <p>A new roof is one of the biggest projects you'll do on your home. You want it done once and done right. Hardtland has been replacing roofs in Madison, Verona and across Dane County since 1972. Tom Degenhardt still runs every job himself.</p>
        <p>As a <strong>CertainTeed Master Shingler</strong> and <strong>Owens Corning Certified</strong> contractor, we install shingles the way the manufacturer intends. That matters for how long your roof lasts and for the manufacturer warranty options you can get. Tom will explain those options in writing with your estimate.</p>
        <p>We also install metal roofs. If you're weighing shingles against metal, we'll walk you through the trade-offs honestly. See our <a href="/metal-roofing/">metal roofing</a> page for more.</p>""",
              aside=callout("Free roof replacement estimate",
                            "We measure your roof, take photos and give you a clear written estimate. No pressure, no high-pressure sales pitch.",
                            "i-file")),
        features("What's Included in a Hardtland Roof Replacement",
                 "Every roof is a little different, but every job covers the same basics.",
                 [("i-hammer", "Full tear-off", "We remove the old shingles down to the roof deck so nothing is hidden under the new roof."),
                  ("i-search", "Deck check and repair", "We check the wood decking and replace soft or rotted boards before anything new goes on."),
                  ("i-shield", "Underlayment and ice protection", "Underlayment and ice and water barrier in the spots Wisconsin winters hit hardest, like eaves and valleys."),
                  ("i-home", "Shingle or metal roofing", "Architectural shingles from CertainTeed and Owens Corning, or a metal roof. We help you pick colors."),
                  ("i-wrench", "Flashing, vents and details", "New flashing around chimneys, walls and skylights, plus roof vents for a healthy attic."),
                  ("i-check-circle", "Daily clean-up", "We pick up old shingles, nails and scraps every day and do a final sweep before we leave.")],
                 band=True),
        prose("What Affects Roof Replacement Cost in Madison", """
        <p>We never quote a fixed price without seeing your roof. Here's what actually moves the number up or down:</p>
        <ul>
          <li><strong>Size.</strong> Roofs are priced by area. A bigger roof needs more material and more labor.</li>
          <li><strong>Pitch.</strong> A steep roof takes more time and more safety gear to work on than a low, walkable one.</li>
          <li><strong>Layers.</strong> If there are two or more old layers to tear off, there's more labor and more disposal.</li>
          <li><strong>Material.</strong> Architectural shingles, premium shingles and metal all cost different amounts.</li>
          <li><strong>Repairs underneath.</strong> Rotted decking or damaged flashing has to be fixed before the new roof goes on.</li>
          <li><strong>Details.</strong> Chimneys, skylights, valleys and dormers add work.</li>
        </ul>
        <p>Your written estimate lists each of these so you can compare quotes fairly. If storm damage is part of the picture, your insurance may cover some or all of it. Read about our <a href="/insurance-claims/">insurance claim help</a>.</p>"""),
        prose("Signs You Need a New Roof", checklist([
            "Shingles that are curling, cupping, cracked or missing in many spots",
            "Bare patches or lots of shingle granules in your gutters",
            "Leaks or water stains in more than one room",
            "A roof deck that looks wavy or saggy from the street",
            "Daylight showing through the roof boards in the attic",
            "Your roof is getting old and your neighbors are replacing theirs",
        ]) + '<p>Not sure? Book a <a href="/free-roof-inspection/">free roof inspection</a>. If a <a href="/roof-repair/">repair</a> will do, we\'ll tell you.</p>', band=True),
        steps_section(STD_STEPS, title="Our Roof Replacement Process"),
        projects_section([
            ("roof-replacement-verona-1.webp", "Completed asphalt shingle roof replacement on a ranch home in Verona, WI", "<strong>Roof replacement</strong>, Verona"),
            ("roof-replacement-madison-2.webp", "New architectural shingle roof on a two-story home in Madison, WI", "<strong>Roof replacement</strong>, Madison"),
            ("roof-replacement-fitchburg-1.webp", "Crew finishing a shingle roof replacement in Fitchburg, WI", "<strong>Roof replacement</strong>, Fitchburg"),
        ], "Recent Roof Replacements", band=False),
        reviews_section(["teresa", "cherise"], title="What Homeowners Say About Their New Roof", band=True),
    ]
    return service_page(
        "roof-replacement",
        title="Roof Replacement Madison WI | Hardtland Home Improvement",
        desc="New shingle and metal roofs for Madison and Verona homes. CertainTeed and Owens Corning certified. Free estimate, honest pricing.",
        h1="Roof Replacement in Madison, WI",
        crumb="Roof Replacement",
        eyebrow="Roofing",
        lead="New shingle and metal roofs for Madison-area homes, installed by a CertainTeed Master Shingler. Free estimate, honest pricing, and the owner on every job.",
        body=body, faqs=faqs, related=["roof-repair", "metal-roofing"],
        towns=["verona-wi", "madison-wi", "middleton-wi"], select="Roof replacement",
        schema_name="Roof Replacement")


# ==========================================================================
# ROOF REPAIR
# ==========================================================================
@add
def roof_repair():
    faqs = [
        ("Can you repair just a section of a roof?",
         "Yes, very often. If the damage is in one area, like a few blown-off shingles or a leak around a vent, we can repair that section. We match the shingles as closely as we can. If the rest of the roof is near the end of its life, we'll tell you that too."),
        ("What is the 25% rule for roofing?",
         "In some places, building codes or insurers say that if more than about 25% of a roof is repaired or replaced within a year, the whole roof has to be brought up to current code. Rules differ by town and by policy. We'll tell you what applies to your home before any work starts."),
        ("How can you tell if a roof needs to be replaced instead of repaired?",
         "If the problems are in one spot, it's usually a repair. If shingles are worn, curling or leaking in many places, a new roof is often the better value. We show you photos and explain why, so the choice is yours."),
        ("Is a roof inspection free?",
         "Yes. We inspect your roof for free, take photos and give you an honest answer. There's no pressure to buy anything."),
        ("Do you handle roof leaks in winter?",
         "Leaks don't wait for good weather, so call or text Tom. Some repairs work in the cold and some are best done as a temporary fix until it warms up. We'll tell you which is right for your roof."),
    ]
    body = [
        prose("Honest Roof Repair in Madison, WI", """
        <p>A leaking roof or a few missing shingles doesn't always mean you need a whole new roof. Hardtland fixes roofs across Madison, Verona and Fitchburg, and <strong>we'll tell you honestly if a repair is enough.</strong></p>
        <p>That's how Tom has worked since 1972. One of our Google reviewers put it this way: we "solved our problem without removing the entire roof." We'd rather earn your trust with a fair repair today than sell you something you don't need.</p>
        <p>When you call or text, Tom or the crew will come out, find the source of the problem, and show you photos before we fix anything.</p>""",
              aside=callout("Got a leak right now?",
                            "Call or text Tom. Tell us what you're seeing, and we'll get someone out to take a look.",
                            "i-alert")),
        features("Roof Repairs We Handle",
                 "From small fixes to storm repairs, we handle the common problems Wisconsin roofs run into.",
                 [("i-gutter", "Roof leaks", "We trace the leak back to its source, which is often not right above the stain on your ceiling."),
                  ("i-home", "Missing or damaged shingles", "Wind-blown, cracked or curled shingles replaced and matched as closely as possible."),
                  ("i-wrench", "Flashing repair", "Loose or rusted flashing around chimneys, walls, skylights and vents resealed or replaced."),
                  ("i-snow", "Ice dam damage", "Repairs after ice dams, plus advice on ventilation and insulation to help stop them coming back."),
                  ("i-hail", "Storm and hail damage", "Wind and hail repairs, with photos for your insurer. See our storm damage page."),
                  ("i-search", "Vents and roof boots", "Cracked plumbing vent boots and worn roof vents are a common source of small leaks.")],
                 band=True),
        prose("Signs Your Roof Needs a Repair", checklist([
            "A water stain on a ceiling or wall that grows after rain",
            "Shingles on the lawn after a windstorm",
            "Cracked, lifted or curling shingles you can see from the ground",
            "Drips or damp insulation in the attic",
            "Gaps or rust around the chimney flashing",
            "Ice dams along the edge of the roof in winter",
        ]) + '<p>If repairs keep adding up, it may be time to look at <a href="/roof-replacement/">roof replacement</a>. We\'ll give you both options and let you decide.</p>'),
        steps_section([
            ("Find the cause", "We inspect the roof and attic to find where the water is really getting in.", "i-search"),
            ("Show you photos", "You see the problem and get a clear price for the repair before we start.", "i-camera"),
            ("Fix it right", "We repair it with matching materials and seal it for Wisconsin weather.", "i-hammer"),
            ("Clean up", "We pick up every scrap and nail and check the repair with you.", "i-check-circle"),
        ], title="Our Roof Repair Process"),
        projects_section([
            ("roof-repair-madison-1.webp", "Repaired section of shingle roof after a leak fix on a home in Madison, WI", "<strong>Roof repair</strong>, Madison"),
            ("roof-repair-flashing-verona-1.webp", "New chimney flashing installed during a roof repair in Verona, WI", "<strong>Flashing repair</strong>, Verona"),
            ("roof-repair-fitchburg-1.webp", "Replaced wind-damaged shingles on a roof in Fitchburg, WI", "<strong>Shingle repair</strong>, Fitchburg"),
        ], "Recent Roof Repairs", band=True),
        reviews_section(["charles", "sally"], title="Repair-First Advice Homeowners Trust"),
    ]
    return service_page(
        "roof-repair",
        title="Roof Repair Madison WI | Leaks & Shingles Fixed Fast",
        desc="Leaking roof or missing shingles? Hardtland repairs roofs across Madison, Verona and Fitchburg. Free inspection, repair-first advice.",
        h1="Roof Repair in Madison, WI",
        crumb="Roof Repair", eyebrow="Roofing",
        lead="Leaks, missing shingles and flashing problems fixed right. We'll tell you honestly if a repair is enough.",
        body=body, faqs=faqs, related=["roof-replacement", "storm-hail-damage"],
        towns=["madison-wi", "verona-wi", "fitchburg-wi"], select="Roof repair",
        schema_name="Roof Repair")


# ==========================================================================
# STORM & HAIL DAMAGE
# ==========================================================================
@add
def storm_hail():
    faqs = [
        ("Does insurance go up if you claim hail damage?",
         "It depends on your insurer and your policy. Hail is a weather event, not something you caused, and many people find it's treated differently than other claims. Your insurance agent is the only one who can tell you for sure, so ask them before you file."),
        ("How long do I have to file a hail damage claim?",
         "Every policy sets its own deadline, and some are shorter than people expect. Check your policy or call your agent soon after the storm. The sooner damage is documented, the easier the claim usually goes."),
        ("Will insurance pay for a whole new roof after hail?",
         "Sometimes. If the damage is widespread, your insurer may cover a full replacement. If it's limited, they may only cover repairs. We document what we find with photos so your adjuster has the full picture."),
        ("Can I see hail damage from the ground?",
         "Often you can't. Hail bruises can be small and easy to miss. Dents on gutters, downspouts, vents or your car are clues. A free inspection is the safest way to know."),
        ("Are you a storm chaser?",
         "No. We've been based in Madison since 1972. We'll be here next year and the year after, long after the out-of-town crews have moved on."),
    ]
    body = [
        prose("Hail &amp; Storm Damage Roof Repair You Can Count On", """
        <p>When hail or high wind rolls through Dane County, roofs take a beating. Hardtland offers <strong>free storm inspections</strong>, a <strong>photo report for your insurer</strong>, and full help with your claim. We work with all insurance companies.</p>
        <p>After a big storm, out-of-town crews often knock on doors. Many are gone before the warranty paperwork is dry. We're not a storm chaser. Tom Degenhardt has been fixing roofs in Madison since 1972, and we'll still be here if you ever need us again.</p>""",
              aside=callout("Storm just hit?",
                            "Call or text Tom at (608) 575-9317. We'll set up a free inspection and tell you if you have damage worth a claim.",
                            "i-hail")),
        prose("What to Do in the First 48 Hours After a Storm", """
        <ol class="num-list">
          <li><strong>Stay safe.</strong> Don't climb on a wet or damaged roof. Stay clear of downed lines and branches.</li>
          <li><strong>Stop more water getting in.</strong> If it's leaking, put out buckets and move valuables. A tarp can help if it's safe to place one.</li>
          <li><strong>Take photos.</strong> Use the photo checklist below before anything is cleaned up or thrown out.</li>
          <li><strong>Call for a free inspection.</strong> We'll check the roof, siding and gutters and photograph any damage.</li>
          <li><strong>Call your insurance agent.</strong> Ask about your deductible and your deadline to file.</li>
          <li><strong>Be careful who you sign with.</strong> Don't sign anything on your doorstep. Ask for a local address and references.</li>
        </ol>""", band=True),
        features("Storm Damage Photo Checklist",
                 "Photos help your insurance claim. Take these from the ground, with the date showing if you can.",
                 [("i-home", "Roof from every side", "Wide shots of each side of the house, plus close-ups of missing or damaged shingles you can see."),
                  ("i-gutter", "Gutters and downspouts", "Hail often leaves dents in metal gutters, downspouts and vents. These are good evidence."),
                  ("i-siding", "Siding and windows", "Cracks, holes or chips in siding, window screens and trim."),
                  ("i-alert", "Inside damage", "Water stains on ceilings or walls, wet insulation, and anything damaged by leaks."),
                  ("i-hail", "The hail itself", "If it's safe, a photo of hailstones next to a coin or ruler shows their size."),
                  ("i-camera", "Your yard and cars", "Fallen branches, shingles on the lawn and dents on cars help show the storm's strength.")],
                 eyebrow="Before you clean up"),
        prose("How We Help With Your Insurance Claim", """
        <p>Insurance claims can be confusing. We make them easier:</p>
        """ + checklist([
            "A free, detailed inspection of your roof, siding and gutters",
            "Clear photos of the damage you can send to your insurer",
            "Help understanding what your adjuster's report says",
            "Work with all insurance companies",
            "A clear, written estimate for the repair or replacement",
        ]) + '<p>See our full <a href="/insurance-claims/">insurance claim help</a> page for each step.</p>', band=True),
        steps_section([
            ("Free storm inspection", "We check your roof and exterior for hail and wind damage and take photos.", "i-search"),
            ("Photo report", "You get photos of what we found to share with your insurance company.", "i-camera"),
            ("Claim help", "We help you through the claim, from the first call to the final check.", "i-file"),
            ("Repair + clean-up", "We fix or replace what's damaged and leave your yard clean.", "i-hammer"),
        ], title="Our Storm Damage Process"),
        projects_section([
            ("storm-damage-roof-middleton-1.webp", "New roof installed after hail damage on a two-story home in Middleton, WI", "<strong>Hail damage roof</strong>, Middleton"),
            ("storm-damage-siding-oregon-1.webp", "Siding replaced after wind damage on a home in Oregon, WI", "<strong>Wind damage siding</strong>, Oregon"),
            ("storm-damage-roof-verona-1.webp", "Roof replaced after a hailstorm on a home in Verona, WI", "<strong>Hail damage roof</strong>, Verona"),
        ], "Recent Storm Repairs", band=True),
        reviews_section(["teresa", "sally"], title="Neighbors Who Trusted Us After the Storm"),
    ]
    return service_page(
        "storm-hail-damage",
        title="Hail & Storm Damage Roof Repair Madison WI | Hardtland",
        desc="Hail or wind damage? Free storm inspection, photo report for your insurer and full claim help. Serving Dane County since 1972.",
        h1="Hail &amp; Storm Damage Roof Repair in Madison, WI",
        crumb="Storm & Hail Damage", eyebrow="Roofing",
        lead="Free storm inspection, photos for your insurer and help with the claim. A local roofer since 1972, not a storm chaser.",
        body=body, faqs=faqs, related=["insurance-claims", "roof-repair"],
        towns=["madison-wi", "middleton-wi", "verona-wi"], select="Storm/hail damage",
        schema_name="Storm and Hail Damage Roof Repair")


# ==========================================================================
# INSURANCE CLAIMS
# ==========================================================================
@add
def insurance_claims():
    faqs = [
        ("Will insurance help with roof replacement?",
         "If your roof was damaged by a covered event like hail or wind, insurance may pay for repairs or a full replacement. Normal wear and old age usually aren't covered. Your policy decides, and we help you show the damage clearly."),
        ("Does insurance go up if you claim hail damage?",
         "It depends on your insurer and your policy. Ask your agent before you file. They can tell you how a claim might affect your rate."),
        ("How far back can an insurance claim be made?",
         "Each policy has its own deadline for reporting damage. Some are fairly short. Check your policy or call your agent as soon as you think you have storm damage."),
        ("Will insurance cover a metal roof?",
         "Insurance usually pays to replace what you had. If you had shingles and want to upgrade to metal, you may need to pay the difference. Ask your agent, and we'll price both options for you."),
        ("Do I have to use the roofer my insurance company suggests?",
         "In most cases, you can choose your own contractor. Check your policy, but it's your home and your choice. We work with all insurance companies."),
        ("Do I have to pay my deductible?",
         "Yes. Your deductible is your share of the cost under your policy. We won't offer to skip or hide it."),
    ]
    steps_html = """
        <ol class="claim-steps">
          <li><h3>1. Call or text us for a free inspection</h3><p>We check your roof, siding and gutters for storm damage. If there's no real damage, we'll tell you, and you don't need to file.</p></li>
          <li><h3>2. Get your photo report</h3><p>We give you photos of the damage we found. These help your insurance company see what happened.</p></li>
          <li><h3>3. File the claim with your insurer</h3><p>You call your insurance company or agent to open the claim. We can help you understand what to say and what to send.</p></li>
          <li><h3>4. The adjuster visits</h3><p>Your insurer sends an adjuster to look at the damage. Ask us about being there too, so nothing gets missed.</p></li>
          <li><h3>5. Review the adjuster's report</h3><p>We go through the report with you in plain words. If something looks missing, we explain your options.</p></li>
          <li><h3>6. We do the work</h3><p>Once the claim is approved, we schedule the repair or replacement, do the job and clean up.</p></li>
          <li><h3>7. Final check</h3><p>We send the paperwork your insurer needs to close the claim and release any final payment.</p></li>
        </ol>"""
    body = [
        prose("Roof Insurance Claim Help From a Local Roofer", """
        <p>Storm damage is stressful, and insurance paperwork makes it worse. Hardtland gives Madison-area homeowners <strong>roof insurance claim help from the first call to the final check.</strong> <strong>We work with all insurance companies.</strong></p>
        <p>We're a roofer, not a lawyer or a public adjuster. What we do is find and photograph the damage, explain the process in plain language, and do quality work once your claim is approved. Tom Degenhardt has helped homeowners through claims since 1972.</p>""",
              aside=callout("Not sure you should file?",
                            "Get a free inspection first. If the damage isn't worth a claim, we'll say so.",
                            "i-file")),
        prose("Our Step-by-Step Roof Claim Process", steps_html, band=True),
        features("What We Do For You",
                 "Here's how we help, so you're never guessing about the next step.",
                 [("i-search", "Free damage inspection", "A careful look at your roof, siding, gutters and windows after a storm."),
                  ("i-camera", "Clear photos", "Photos of the damage that you can share with your insurance company."),
                  ("i-file", "Plain-English help", "We explain your adjuster's report and the claim steps without the jargon."),
                  ("i-user-check", "One local contact", "You deal with Tom, who answers his texts, not a call center."),
                  ("i-hammer", "Quality work", "Repairs or a new roof done by a CertainTeed Master Shingler."),
                  ("i-wallet", "Simple payment", "We accept insurance payments, personal checks, cash and Zelle.")]),
        steps_section(STD_STEPS, title="From Storm to Finished Roof"),
        reviews_section(["cherise", "teresa"], title="Why Homeowners Choose Hardtland", band=True),
    ]
    return service_page(
        "insurance-claims",
        title="Roof Insurance Claim Help Madison WI | Hardtland",
        desc="We work with every insurance company. Free inspection, damage photos and help from first call to final check.",
        h1="Roof Insurance Claim Help",
        crumb="Insurance Claim Help", eyebrow="Storm damage",
        lead="We work with all insurance companies. Free inspection, damage photos, and help from the first call to the final check.",
        body=body, faqs=faqs, related=["storm-hail-damage", "free-roof-inspection"],
        towns=["madison-wi", "verona-wi", "fitchburg-wi"], select="Storm/hail damage",
        schema_name="Roof Insurance Claim Help")


# ==========================================================================
# METAL ROOFING
# ==========================================================================
@add
def metal_roofing():
    faqs = [
        ("How long does a metal roof last in Wisconsin?",
         "A well-installed metal roof often lasts 40 years or more, which is usually longer than asphalt shingles. The panel type, the finish and how it's installed all matter. We'll go over what to expect for the system you choose."),
        ("Will insurance cover a metal roof?",
         "If storm damage is covered, insurance usually pays to replace what you had. Upgrading from shingles to metal may mean paying the difference. Some insurers treat certain roofs differently, so ask your agent."),
        ("Is a metal roof loud when it rains?",
         "Over a solid roof deck with underlayment and an insulated attic, most homeowners say rain noise is not a problem. It's a common worry, and we're happy to talk it through."),
        ("How much does a metal roof cost?",
         "Metal costs more up front than shingles, but it can last longer. Your price depends on the roof's size, pitch, the panel style and trim details. We give you a written estimate after a free visit."),
        ("Is metal good for snow?",
         "Metal sheds snow well. Because snow can slide off in big sheets, we talk with you about snow guards over doors, walkways and decks."),
    ]
    body = [
        prose("Metal Roofing in Madison, WI, Built for Wisconsin Winters", """
        <p>Metal roofs handle heavy snow, ice and wind well, and they can last a long time. Hardtland installs and replaces metal roofs for homes in Madison, Verona and nearby towns. We've been a local roofer since 1972, and Tom is on every job.</p>
        <p>Metal isn't right for every home or every budget. We'll give you an honest comparison with a shingle roof, so you can decide what makes sense for how long you plan to stay.</p>""",
              aside=callout("Shingles or metal?",
                            "We'll price both on the same visit so you can compare side by side.",
                            "i-layers")),
        features("Why Homeowners Choose Metal",
                 "Here's what a metal roof does well, and what to think about.",
                 [("i-snow", "Sheds snow and ice", "Smooth panels help snow slide off, which can help with ice dam problems."),
                  ("i-calendar", "Long life", "Metal often outlasts asphalt shingles when it's installed right."),
                  ("i-shield", "Stands up to wind", "Panels are fastened to resist the strong winds that come with summer storms."),
                  ("i-home", "Many colors and styles", "Painted finishes in many colors to match your siding and trim."),
                  ("i-wallet", "Higher up-front cost", "Metal usually costs more at the start. We'll help you weigh it against how long you'll stay."),
                  ("i-wrench", "Install matters", "Trim, flashing and fasteners need to be done right. That's where experience counts.")],
                 band=True, eyebrow="Pros and cons"),
        prose("Signs Metal Might Be Right for You", checklist([
            "You plan to stay in your home for many years",
            "You're tired of ice dams on your current roof",
            "Your shingle roof needs replacing and you want something that lasts longer",
            "You have a low-slope porch, garage or outbuilding roof",
            "You like the look of a metal roof on a farmhouse or modern home",
        ])),
        steps_section(STD_STEPS, title="Our Metal Roof Process"),
        projects_section([
            ("metal-roof-oregon-1.webp", "Standing seam metal roof installed on a home in Oregon, WI", "<strong>Metal roof</strong>, Oregon"),
            ("metal-roof-mount-horeb-1.webp", "Metal roof on a farmhouse-style home near Mount Horeb, WI", "<strong>Metal roof</strong>, Mount Horeb"),
            ("metal-roof-verona-1.webp", "Dark metal roof with snow guards on a home in Verona, WI", "<strong>Metal roof</strong>, Verona"),
        ], "Recent Metal Roofs", band=True),
        reviews_section(["cherise", "sally"], title="What Customers Say"),
    ]
    return service_page(
        "metal-roofing",
        title="Metal Roofing Madison WI | Installation & Replacement",
        desc="Metal roofs built for Wisconsin winters. Installed by a local roofer since 1972. Free estimate in Madison, Verona and nearby.",
        h1="Metal Roofing in Madison, WI",
        crumb="Metal Roofing", eyebrow="Roofing",
        lead="Metal roofs built for Wisconsin winters, installed by a local roofer since 1972. Free estimate and an honest comparison with shingles.",
        body=body, faqs=faqs, related=["roof-replacement", "insurance-claims"],
        towns=["oregon-wi", "mount-horeb-wi", "verona-wi"], select="Roof replacement",
        schema_name="Metal Roofing Installation")


# ==========================================================================
# FREE ROOF INSPECTION
# ==========================================================================
@add
def free_inspection():
    faqs = [
        ("Is a roof inspection free?",
         "Yes. Our roof and exterior inspections are free. There's no catch and no pressure to buy."),
        ("What does a roof inspection consist of?",
         "We check your shingles, flashing, vents, gutters and roof edges, look for storm damage, and check the attic for leaks if we can get in. We take photos and explain what we found."),
        ("How long does an inspection take?",
         "Most take well under an hour, depending on the size and pitch of your roof. We'll go over the photos with you before we leave, or send them after."),
        ("Do I need to be home?",
         "It helps if you are, so we can check the attic and answer your questions. If you can't be there, we can look at the outside and send you the photos."),
        ("What if you don't find anything?",
         "Then we'll tell you that your roof is fine. Plenty of inspections end that way, and that's good news."),
    ]
    body = [
        prose("What You Get With a Free Roof Inspection", checklist([
            "A careful look at shingles, flashing, vents and roof edges",
            "A check for hail, wind and ice damage",
            "An attic check for leaks, when we can get in",
            "A look at gutters, siding, soffit and fascia while we're there",
            "Photos of what we find",
            "An honest repair-or-replace answer, or \"you're all set\"",
        ]) + "<p>Our free roof inspections in Madison and Verona come with no pressure. Tom Degenhardt has run Hardtland since 1972, and we'd rather tell you the truth than make a sale.</p>",
              aside='<div class="form-card form-card--inline"><h3>Book Your Free Inspection</h3><p>Tom or the crew will call you back within 1 business day.</p>'
                    + form("/free-roof-inspection/", "Roof repair", "fi") + "</div>"),
        features("When to Book an Inspection",
                 "A quick look now can save a big repair later.",
                 [("i-hail", "After a storm", "Hail and wind damage is easy to miss from the ground."),
                  ("i-gutter", "When you see a leak", "Water stains on ceilings or walls mean water is getting in somewhere."),
                  ("i-calendar", "As your roof gets older", "Knowing how much life is left helps you plan and budget."),
                  ("i-home", "Before you buy or sell", "Know the roof's condition before closing day."),
                  ("i-snow", "After a hard winter", "Ice dams and heavy snow can loosen shingles and flashing."),
                  ("i-file", "Before an insurance claim", "Find out if the damage is worth filing for.")],
                 band=True, eyebrow="Good times to check"),
        prose("Why We Don't Pressure You", """
        <p>A free inspection should be just that: free, with no strings. Some contractors use \"free inspections\" to push a sale. We don't. Tom Degenhardt has run Hardtland since 1972, and a lot of our work comes from neighbors and repeat customers. One reviewer has had us replace their roof twice in 20 years. That only happens when people trust you.</p>
        <p>So if your roof has years left, we'll tell you. If a small repair will fix the problem, we'll quote the repair. If you do need a new roof, you'll see the photos that show why, and you can take your time deciding.</p>"""),
        steps_section([
            ("Book a time", "Call, text or use the form. We'll set up a time that works for you.", "i-calendar"),
            ("We inspect", "We check your roof and exterior and take photos.", "i-search"),
            ("You see the photos", "We show you what we found and explain it plainly.", "i-camera"),
            ("Honest answer", "Repair, replace, or nothing at all. No pressure either way.", "i-check-circle"),
        ], title="How the Free Inspection Works"),
        reviews_section(["cherise", "charles", "sally"], title="Honest Advice, From Real Customers", band=True),
    ]
    return service_page(
        "free-roof-inspection",
        title="Free Roof Inspection Madison & Verona WI | Hardtland",
        desc="Book a free, no-pressure roof inspection. Photos of what we find and an honest repair-or-replace answer.",
        h1="Free Roof Inspection in Madison &amp; Verona",
        crumb="Free Roof Inspection", eyebrow="Roofing",
        lead="A free, no-pressure look at your roof. You get photos of what we find and an honest repair-or-replace answer.",
        body=body, faqs=faqs, related=["roof-repair", "storm-hail-damage"],
        towns=["verona-wi", "madison-wi", "fitchburg-wi"], select="Roof repair",
        schema_name="Free Roof Inspection")


# ==========================================================================
# SIDING
# ==========================================================================
@add
def siding():
    faqs = [
        ("Siding repair or replacement?",
         "If the damage is in a few spots, like a cracked panel or a storm-damaged wall, a repair is often enough. If siding is faded, warped, loose or letting water in all over, replacement is usually the better value. We'll show you what we see and give you both options."),
        ("How much does James Hardie siding cost?",
         "Fiber cement siding like James Hardie usually costs more than vinyl, because the material and the install take more work. The price depends on your home's size, how many corners and windows it has, and trim choices. We'll give you a written estimate after a free visit."),
        ("Vinyl, fiber cement or metal: which is best?",
         "Vinyl is low-maintenance and budget-friendly. Fiber cement is heavy, tough and looks like painted wood. Metal is durable and works well for a modern look. We'll talk about your budget and style and help you pick."),
        ("Can you match my existing siding for a repair?",
         "We'll do our best. Older siding colors fade and some styles are discontinued, so a perfect match isn't always possible. We'll tell you up front what to expect."),
        ("Will insurance pay for hail-damaged siding?",
         "If your siding was damaged by a covered storm, it may be covered. We photograph the damage and help with the claim."),
    ]
    body = [
        prose("Siding Contractor in Madison, WI", """
        <p>Good siding keeps water out, helps your home stay comfortable, and makes it look cared for. Hardtland is a local siding contractor serving Madison, Verona and Dane County since 1972. We install and repair <strong>vinyl, fiber cement and metal siding</strong>, plus the <strong>soffit and fascia</strong> that finish the job.</p>
        <p>Our Google reviewers mention siding replacement a lot, and the same things come up: quick work, an efficient crew and a clean job site.</p>""",
              aside=callout("Free siding estimate",
                            "We'll look at your siding, soffit and fascia and give you a written estimate. No pressure.",
                            "i-siding")),
        features("Siding Types We Install",
                 "Each material has its strengths. We'll help you pick what fits your home and budget.",
                 [("i-siding", "Vinyl siding", "Low upkeep, many colors and a budget-friendly price. A popular choice for Madison-area homes."),
                  ("i-home", "Fiber cement siding", "Tough, heavy siding that looks like painted wood and stands up to Wisconsin weather."),
                  ("i-layers", "Metal siding", "Durable and clean-looking. Great for modern homes, garages and outbuildings."),
                  ("i-wrench", "Siding repair", "Storm-damaged, cracked or loose panels fixed and matched as closely as possible.")],
                 band=True),
        prose("Soffit and Fascia Repair", """
        <p>Soffit is the panel under your roof's overhang. Fascia is the board along the roof edge where your gutters attach. When they rot or crack, water and critters can get in, and gutters can pull loose.</p>
        """ + checklist([
            "Rotted or soft fascia boards replaced",
            "New vented soffit to help your attic breathe",
            "Aluminum or vinyl wrap to protect wood from the weather",
            "Gutters re-hung on solid fascia",
        ]) + '<p>We often handle soffit and fascia along with a <a href="/roof-replacement/">new roof</a> or <a href="/gutters/">new gutters</a>.</p>'),
        prose("Signs You Need New Siding", checklist([
            "Cracked, warped or loose panels",
            "Fading that makes the house look tired",
            "Soft spots, rot or mold on or behind the siding",
            "Peeling paint or bubbling inside on the walls",
            "Higher heating bills or drafts near outside walls",
            "Hail or wind damage after a storm",
        ]), band=True),
        steps_section(STD_STEPS, title="Our Siding Process"),
        projects_section([
            ("siding-replacement-fitchburg-1.webp", "New vinyl siding with fresh soffit and fascia on a home in Fitchburg, WI", "<strong>Siding replacement</strong>, Fitchburg"),
            ("siding-fiber-cement-madison-1.webp", "Fiber cement siding installed on a home in Madison, WI", "<strong>Fiber cement siding</strong>, Madison"),
            ("soffit-fascia-middleton-1.webp", "New soffit and fascia on a home in Middleton, WI", "<strong>Soffit &amp; fascia</strong>, Middleton"),
        ], "Recent Siding Projects", band=True),
        reviews_section(["sally", "cherise"], title="What Customers Say"),
    ]
    return service_page(
        "siding",
        title="Siding Contractor Madison WI | Vinyl & Fiber Cement",
        desc="Siding replacement and repair, plus soffit and fascia, for Madison-area homes. Free estimate from a local contractor since 1972.",
        h1="Siding Contractor in Madison, WI",
        crumb="Siding", eyebrow="Exteriors",
        lead="Vinyl, fiber cement and metal siding, plus soffit and fascia, for Madison-area homes. Free estimate from a local contractor since 1972.",
        body=body, faqs=faqs, related=["gutters", "storm-hail-damage"],
        towns=["fitchburg-wi", "madison-wi", "middleton-wi"], select="Siding",
        schema_name="Siding Installation and Repair")


# ==========================================================================
# GUTTERS
# ==========================================================================
@add
def gutters():
    faqs = [
        ("Are gutter guards worth it?",
         "For many homes, yes, especially with trees nearby. Guards cut down on clogs, overflow and ladder trips. No guard is perfectly maintenance-free, so we'll tell you honestly what to expect for your home and your trees."),
        ("Which gutter guard is best?",
         "It depends on what falls on your roof. Pine needles, maple seeds and big oak leaves each act differently. We'll look at your trees and roof and recommend a guard that fits."),
        ("What are seamless gutters?",
         "Seamless gutters are formed in one long piece to fit your home, instead of short sections joined together. Fewer seams means fewer spots to leak."),
        ("Do you repair gutters?",
         "Yes. We fix leaks, sagging gutters, loose hangers and downspouts that dump water by the foundation. If the fascia behind the gutter is rotted, we can replace that too."),
        ("Do gutters help with ice dams?",
         "Gutters move water away, but ice dams are mostly caused by heat escaping into the attic. We'll look at the whole picture, including ventilation, and give you honest advice."),
    ]
    body = [
        prose("Gutters &amp; Gutter Guards in Madison, WI", """
        <p>Your gutters protect your roof edge, siding and foundation. When they clog, sag or leak, water ends up where it shouldn't. Hardtland installs <strong>seamless gutters</strong>, <strong>leaf guards</strong> and does <strong>gutter repair</strong> for homes in Madison, Verona and Fitchburg.</p>
        <p>We've been taking care of Madison-area homes since 1972. When we work on your gutters, we also check the fascia and roof edge, so small problems get caught early.</p>""",
              aside=callout("Free gutter estimate",
                            "Tell us what's going on with your gutters. We'll take a look and give you a written estimate.",
                            "i-gutter")),
        features("Our Gutter Services",
                 "Everything you need to keep water moving away from your home.",
                 [("i-gutter", "Seamless gutters", "Made to fit your home in long runs, with fewer seams that can leak."),
                  ("i-shield", "Leaf guards and gutter covers", "Fewer clogs, less overflow and fewer trips up the ladder."),
                  ("i-wrench", "Gutter repair", "Leaks, sagging runs and loose hangers fixed."),
                  ("i-home", "Downspouts", "Placed to carry water away from your foundation and walkways."),
                  ("i-siding", "Fascia repair", "Rotted fascia replaced so your gutters have something solid to hang on."),
                  ("i-search", "Gutter cleaning", "Ask about cleaning when we're out for other work.")],
                 band=True),
        prose("Are Gutter Guards Worth It in Madison?", """
        <p>Many Madison-area neighborhoods have big, mature trees. Oaks, maples and pines drop leaves, seeds and needles all year, and gutters fill fast. Clogged gutters overflow, which can soak your fascia, stain siding and dump water next to your foundation. In winter, a clogged gutter can add to ice build-up at the roof edge.</p>
        <p>Gutter guards cut down on clogs and ladder trips. They aren't perfectly maintenance-free, and the right type depends on what falls from your trees. We'll look at your roof and trees and tell you honestly whether guards are worth it for your home.</p>"""),
        prose("Signs Your Gutters Need Attention", checklist([
            "Water spilling over the edge during rain",
            "Gutters pulling away from the house or sagging",
            "Drips from seams and corners",
            "Peeling paint or stains on the siding below",
            "Puddles or wet spots near the foundation",
            "Plants growing in your gutters",
        ])),
        steps_section(STD_STEPS, title="Our Gutter Process"),
        projects_section([
            ("gutters-mount-horeb-1.webp", "Seamless gutters with leaf guards on a home in Mount Horeb, WI", "<strong>Gutters &amp; leaf guards</strong>, Mount Horeb"),
            ("gutters-verona-1.webp", "New seamless gutters and downspouts on a home in Verona, WI", "<strong>Seamless gutters</strong>, Verona"),
            ("gutter-guards-fitchburg-1.webp", "Gutter guards installed on a home with tall trees in Fitchburg, WI", "<strong>Gutter guards</strong>, Fitchburg"),
        ], "Recent Gutter Projects", band=True),
        reviews_section(["sally", "cherise"], title="What Customers Say"),
    ]
    return service_page(
        "gutters",
        title="Gutters & Gutter Guards Madison WI | Hardtland",
        desc="Seamless gutters, leaf guards and gutter repair for Madison, Verona and Fitchburg homes. Free estimate.",
        h1="Gutters &amp; Gutter Guards in Madison, WI",
        crumb="Gutters", eyebrow="Exteriors",
        lead="Seamless gutters, leaf guards and gutter repair for Madison, Verona and Fitchburg homes. Free estimate from a local contractor.",
        body=body, faqs=faqs, related=["siding", "roof-repair"],
        towns=["verona-wi", "fitchburg-wi", "mount-horeb-wi"], select="Gutters",
        schema_name="Gutter Installation and Gutter Guards")


# ==========================================================================
# WINDOWS & DOORS
# ==========================================================================
@add
def windows_doors():
    faqs = [
        ("How do I know if my windows need replacing?",
         "Drafts, fogging between the panes, rot around the frame, and windows that stick or won't lock are common signs. If you feel cold air near your windows in winter, it's worth a look."),
        ("Will new windows lower my heating bill?",
         "Energy-efficient windows can help keep heat in and cut drafts. How much you save depends on your old windows, your home and how you heat it, so we won't promise a number."),
        ("Can you replace just a few windows?",
         "Yes. Many homeowners replace the worst windows first and do the rest later. We'll help you decide where to start."),
        ("Do you install entry doors too?",
         "Yes. We replace front, back and side entry doors and seal them well against Wisconsin wind and cold."),
        ("Can you do windows and siding at the same time?",
         "Yes, and it often makes sense. Doing both together lets us flash and trim the windows properly with the new siding."),
    ]
    body = [
        prose("Window &amp; Door Replacement in Madison, WI", """
        <p>Old windows and doors let in drafts, make rooms harder to heat, and can let water into your walls. Hardtland installs <strong>energy-efficient replacement windows</strong> and <strong>entry doors</strong> for homes in Madison, Verona and across Dane County.</p>
        <p>We're the same local crew that does roofs and siding, owner-run by Tom Degenhardt since 1972. Your estimate is free and done in your home, so we can measure and see what you need.</p>""",
              aside=callout("Free in-home estimate",
                            "We'll measure your windows and doors and walk you through options and pricing.",
                            "i-window")),
        features("What We Install",
                 "Replacement windows and doors fitted and sealed for Wisconsin weather.",
                 [("i-window", "Replacement windows", "Energy-efficient windows in common styles like double-hung, sliders and casements."),
                  ("i-home", "Entry doors", "Front, back and side entry doors that seal tight and lock securely."),
                  ("i-shield", "Proper flashing and sealing", "Careful flashing, insulation and trim so water and drafts stay out."),
                  ("i-check-circle", "Clean install", "We protect your floors, take away old windows and clean up when we're done.")],
                 band=True),
        prose("Choosing Windows for Wisconsin Weather", """
        <p>Madison winters are long and cold, and summers can be hot and humid. The right replacement windows help with both. When we meet with you, we'll talk through:</p>
        <ul>
          <li><strong>Glass.</strong> Double- or triple-pane glass with low-E coatings helps keep heat inside in winter and outside in summer.</li>
          <li><strong>Frame material.</strong> Vinyl is low-maintenance and budget-friendly. Other materials cost more but offer different looks.</li>
          <li><strong>Style.</strong> Double-hung, slider and casement windows each open differently. We'll match what works for each room.</li>
          <li><strong>Install quality.</strong> Even a great window leaks if it's installed poorly. Careful flashing and insulation matter as much as the window itself.</li>
        </ul>
        <p>We'll give you honest advice on where spending more makes sense, and where it doesn't.</p>""", band=False),
        prose("Signs It's Time for New Windows or Doors", checklist([
            "Drafts you can feel on cold or windy days",
            "Fog or moisture between the glass panes",
            "Soft or rotted wood around the frame",
            "Windows that stick, won't stay open or won't lock",
            "Frost or ice on the inside of the glass in winter",
            "An entry door that lets in light or air around the edges",
        ])),
        steps_section([
            ("Free in-home estimate", "We measure your windows and doors and talk about styles and budget.", "i-ruler"),
            ("Clear written quote", "You get a written quote with the products and work listed.", "i-file"),
            ("Professional install", "We remove the old units and install, flash and seal the new ones.", "i-hammer"),
            ("Clean-up + walk-through", "We clean up and check every window and door with you.", "i-check-circle"),
        ], title="Our Window & Door Process"),
        projects_section([
            ("windows-madison-1.webp", "New replacement windows on a home in Madison, WI", "<strong>Replacement windows</strong>, Madison"),
            ("entry-door-verona-1.webp", "New front entry door installed on a home in Verona, WI", "<strong>Entry door</strong>, Verona"),
            ("windows-middleton-1.webp", "Replacement windows with new exterior trim in Middleton, WI", "<strong>Windows &amp; trim</strong>, Middleton"),
        ], "Recent Window & Door Projects", band=True),
        reviews_section(["cherise", "sally"], title="What Customers Say"),
    ]
    return service_page(
        "windows-doors",
        title="Window & Door Replacement Madison WI | Hardtland",
        desc="Energy-efficient replacement windows and entry doors, installed by a local Madison contractor. Free in-home estimate.",
        h1="Window &amp; Door Replacement in Madison, WI",
        crumb="Windows & Doors", eyebrow="Exteriors",
        lead="Energy-efficient replacement windows and entry doors, installed by a local Madison contractor. Free in-home estimate.",
        body=body, faqs=faqs, related=["siding", "gutters"],
        towns=["madison-wi", "middleton-wi", "verona-wi"], select="Windows/doors",
        schema_name="Window and Door Replacement")
