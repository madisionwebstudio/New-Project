# Hardtland Home Improvement — website

Static HTML site: one shared stylesheet (`css/styles.css`), one small script
(`js/main.js`), no framework. Every page is its own folder with an
`index.html`, so URLs are clean (`/roof-repair/`, `/verona-wi/`, ...).

## Editing pages

Pages are generated from shared templates so the header, footer and form stay
identical everywhere. Edit the content in `build/`, then run:

```
python3 build/build.py
```

| File | What's in it |
| --- | --- |
| `build/common.py` | Header, footer, form, icons, reviews, phone/hours/form URL |
| `build/home_main.html` | Homepage content |
| `build/services.py` | The 9 service pages |
| `build/towns.py` | The 6 town pages |
| `build/pages.py` | Service areas, reviews, about, gallery, FAQ, contact, privacy, accessibility, 404 |

The build also writes `sitemap.xml` and `robots.txt`. Don't deploy the
`build/` folder itself.

## Photos

Every image in `/img/` is currently a grey **PHOTO PLACEHOLDER**. To add a real
photo, save it as WebP with the **same file name** and drop it into `/img/`.
The build never overwrites a real photo. Captions and alt text live in the
build files; update a caption if the real job's town or type differs.

Quick list of all placeholder names: `ls img/`

## Before launch (search the code for `TODO` and `[`)

- [ ] Real job photos (homepage, service pages, town pages, gallery, Tom photos)
- [ ] Real jobs from Tom for each town page (`build/towns.py`)
- [ ] Real hours: `HOURS` in `build/common.py`, plus `openingHoursSpecification` in `build/home_ld_business.json`
- [ ] Origin story on the About page (`[CONFIRMED STORY FROM TOM]` in `build/pages.py`)
- [ ] Form handler URL: `FORM_ACTION` in `build/common.py` (should email tomd@tds.net)
- [ ] Google, Facebook, Yelp URLs in `sameAs` (`build/home_ld_business.json`)
- [ ] Direct Google review link: `GOOGLE_REVIEWS` in `build/common.py`
- [ ] Logo file, CertainTeed and Owens Corning badge files
- [ ] Full review text from Google (currently excerpts) in `build/common.py`
- [ ] Confirm domain (`DOMAIN` in `build/common.py`) and set up 301s from old URLs
- [ ] Open Graph image `/img/og-hardtland.jpg` (1200x630)
- [ ] Have the privacy policy reviewed
