"""Real Hardtland photos (from Tom's old website gallery, Nov 2026).

The old site had no captions, so the town and job type of each photo are not
known yet. Captions and alt text only describe what is visible. When Tom
confirms a photo's job and town, fill in "job" and "town" below and rebuild:
the caption and alt text pick them up automatically, and the gallery filter
appears once photos have a "cat" (roofing / siding / gutters / windows).
"""

# key: file in /img/, width, height, what is visible, short caption, job, town, cat
PHOTOS = {
    "hero":   dict(file="hero-roof-replacement-verona-1600.webp", w=1600, h=900,
                   alt="Two-story home with brick front, gray siding and an architectural shingle roof, a recent Hardtland project"),
    "trailer": dict(file="hardtland-trailer-lift-job-site.webp", w=720, h=404,
                    alt="Hardtland trailer and lift set up at a job site"),
    "van":    dict(file="hardtland-work-van.webp", w=720, h=404,
                   alt="Hardtland work van loaded with ladders"),
}

JOBS = [
    # (key, source no., visible description, short caption)
    ("tearoff",   1,  "Roof job in progress with new underlayment on the roof deck and house wrap on the walls", "Roof and wall wrap, work in progress"),
    ("gray2",     2,  "Two-story home with gray vinyl siding, black shutters and a dark shingle roof", "Two-story home, gray siding"),
    ("tan2",      3,  "Two-story home with tan siding, plum shutters and a covered front porch", "Two-story home, tan siding"),
    ("ranchbeige",4,  "Ranch home with beige siding, stone accents and a shingle roof", "Ranch home, beige siding"),
    ("graybay",   5,  "Two-story home with gray siding, a bay window and a shingle roof", "Two-story home with bay window"),
    ("gray2b",    7,  "Two-story home with gray siding, an arched window and a white garage door", "Two-story home, gray siding"),
    ("split",     12, "Split-level home with white siding and a gray shingle roof", "Split-level home, white siding"),
    ("ranchbrick",13, "Ranch home with a brick front, gray siding and a shingle roof", "Ranch home, brick and siding"),
    ("backwhite", 14, "Back of a two-story home with white siding and new windows", "Two-story home, white siding"),
    ("deck",      15, "Back of a ranch home with white siding, a dark shingle roof and a deck", "Ranch home, white siding"),
    ("brick2",    18, "Two-story home with a brick front, gray siding and an architectural shingle roof", "Two-story home, brick and siding"),
    ("whitearch", 19, "White multi-level home with an arched window and a brown shingle roof", "Multi-level home, white siding"),
    ("yellow",    20, "Yellow ranch home with a ladder and work truck in the driveway during a job", "Ranch home, job in progress"),
    ("bungalow",  21, "Bungalow with tan siding, white trim and a front entry porch", "Bungalow, tan siding"),
    ("stone2",    23, "Two-story home with white siding above a stone lower level", "Two-story home, white siding"),
    ("pergola",   25, "White home with a rounded bay, tall windows and a pergola", "Custom home, white siding"),
    ("backdeck",  27, "Back of a two-story home with white siding and a wood deck", "Two-story home, white siding"),
    ("tudor",     28, "Tudor-style two-story home with brick and a shingle roof", "Tudor-style home"),
    ("brownlong", 30, "Long two-story home with brown siding and a dark shingle roof", "Two-story home, brown siding"),
    ("teal",      31, "Two-story home with tan siding, teal shutters and a front porch", "Two-story home, tan siding"),
    ("colonial",  32, "Colonial-style home with white siding, green shutters and a shingle roof", "Colonial home, white siding"),
    ("ranchgray", 33, "Ranch home with gray siding and an asphalt shingle roof", "Ranch home, gray siding"),
    ("cream",     34, "Two-story home with cream siding, a front porch and a red work truck", "Two-story home, cream siding"),
    ("hill",      36, "Two-story home with gray siding on a sloped lot", "Two-story home, gray siding"),
    ("sunroom",   39, "White home with a sunroom, arched window and a shingle roof", "Home with sunroom, white siding"),
    ("porch2",    40, "Two-story home with white siding, a long front porch and a red work truck", "Two-story home, white siding"),
    ("bilevel",   41, "Bi-level home with tan siding and a red garage door", "Bi-level home, tan siding"),
    ("chimney",   42, "Chimney and roof edge on a home with tan siding", "Chimney and roof edge"),
    ("blue",      38, "Two-story home with blue siding, white trim and a long front porch", "Two-story home, blue siding"),
]

# Fill these in as Tom confirms each job, e.g. "tearoff": ("Roof replacement", "Verona", "roofing")
CONFIRMED = {}

for key, _no, alt, cap in JOBS:
    job, town, cat = CONFIRMED.get(key, (None, None, None))
    PHOTOS[key] = dict(file=f"hardtland-project-{key}.webp", alt=alt, cap=cap, job=job, town=town, cat=cat)


def project(key):
    """(file, alt, caption_html) for common.project_grid."""
    p = PHOTOS[key]
    if p.get("job") and p.get("town"):
        cap = f"<strong>{p['job']}</strong>, {p['town']}"
        alt = f"{p['job']} in {p['town']}, WI: {p['alt'][0].lower()}{p['alt'][1:]}"
    else:
        cap = f"<strong>{p['cap']}</strong>"
        alt = p["alt"] + ", a recent Hardtland project"
    return (p["file"], alt, cap)
