# Hardtland Home Improvement — website

Static HTML site: one shared stylesheet (`css/styles.css`), one small script
(`js/main.js`), no framework. Every page is its own folder with an
`index.html`, so URLs are clean (`/roof-repair/`, `/verona-wi/`, ...).

## Admin panel (`/admin/`)

Tom logs in at `https://www.hardtlandhomeimprovement.com/admin/` (works on a phone).

- **Leads:** every free inspection request, newest first. Call, text or map with
  one tap, set a status (New, Contacted, Inspection set, Won, Lost, Spam), add
  private notes, re-send the email, export to CSV.
- **Business info:** hours, phone, public email, address, Google rating and
  review count, Google review link, Google/Facebook/Yelp links, and an optional
  notice bar across the top of every page. **Save** updates every page on the
  live site right away (footer, contact page, review sections, and the business
  details Google reads).
- **Email:** who gets lead emails (several addresses allowed), the "from"
  address, and how mail is sent: the web host's built-in mail, or an SMTP
  account (more reliable). **Save and send test email** checks it works.
- **Account:** change username and password.

Every request is **saved first, then emailed**, so a mail problem never loses a
lead. Failed emails are flagged in red on the Leads page.

### Hosting requirements

PHP 8.1+ with PDO SQLite (standard on most shared hosts), Apache or LiteSpeed
(for `.htaccess`). The `data/` folder and every `.html` file must be writable by
PHP. The Business info page has a **System check** that confirms all of this.

### First-time setup

1. In `inc/config.php`, change `ADMIN_SETUP_KEY` to a long secret phrase.
2. Upload everything **except** the `build/` folder.
3. Open `/admin/`, enter the setup key, choose a username and password.
4. On the Email page, enter the SMTP details and press **Save and send test email**.
5. On Business info, enter Tom's real hours and press **Save**.
6. Uncomment the HTTPS redirect in `.htaccess` once SSL is on.

`data/` and `inc/` are blocked from the web by `.htaccess`. On Nginx, add
equivalent `deny all` rules for `/data/`, `/inc/` and `/build/`.

Protections: hashed password, login lock after 5 failed tries (15 min),
CSRF tokens on every form, 8-hour idle logout, honeypot + timing check + rate
limit on the public form, and no lead data in the public pages.

## SEO built in

| Area | What's done |
| --- | --- |
| Pages | 22 indexable pages, one keyword each (homepage, 9 services, 6 towns, 6 supporting), unique titles under 60 characters and descriptions under 155 |
| On-page | One H1 per page, keyword in H1, title, first paragraph and an H2; breadcrumbs; internal links (each service links to 2 services + 3 towns, each town links to all services) |
| Structured data | `RoofingContractor` (hours, rating, services, map, contact point), `WebSite`, a typed `WebPage` on every page, `Service` (each service + each town), `FAQPage`, `BreadcrumbList`, `Person` (Tom), `ImageGallery` |
| Sharing | Open Graph + Twitter/X cards with a 1200x630 share image (`img/og-hardtland.jpg`) |
| Crawling | `sitemap.xml` with images and real per-page dates, `robots.txt`, `llms.txt` for AI assistants, `noindex` on thank-you/404/admin/form handler |
| Speed | Static HTML, hero image preloaded, other images lazy-loaded with width/height, fonts load without blocking, caching + compression in `.htaccess` |
| Redirects | Old site URLs (`/Accessibility`, `/Home/PrivacyPolicy`, `/About`...) 301 to the new pages; `/page` -> `/page/`; `index.html` -> clean URL; http/bare domain -> `https://www.` (uncomment once SSL is live) |
| Local | Same name, address and phone everywhere (edited in one place in the admin), geo tags, town pages, service-area schema |
| Tracking | Admin > Business info: Google Analytics 4 ID, Search Console and Bing verification codes. Calls, texts and form requests are tracked as GA4 events |

`build/sitemap-state.json` remembers each page's last real change so
`lastmod` dates stay honest. Commit it with the pages.

### After launch (off-site, not code)

1. Search Console + Bing Webmaster Tools: verify (paste codes in the admin), submit `/sitemap.xml`.
2. Google Business Profile: name "Hardtland Home Improvement, Inc.", real hours (same as admin), website link with UTM tags, all services and towns.
3. Citations: make name/address/phone match exactly on Yelp, Facebook, BBB, Angi, Bing Places, Apple Business Connect, Nextdoor, CertainTeed and Owens Corning contractor finders.
4. Reviews: ask every customer (text template + QR code on invoices). Update the rating in the admin as it grows.
5. Swap the placeholder photos for real job photos (biggest win for image search and trust).
6. Phase 2 articles from the plan: roof cost in Madison, roof lifespan in Wisconsin, repair vs replace, hail claims step by step, gutter guards, best time to replace.

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

The build also writes `sitemap.xml` and `robots.txt`, then runs
`php inc/publish-cli.php` to apply `data/site.json` (the admin's business info)
to the fresh pages. Don't deploy the `build/` folder itself.

**Once the site is live, Tom's admin edits live in `data/site.json` on the
server.** Before rebuilding pages locally, download that file from the server
into `data/`, or the rebuild will put back the old hours and rating.

## Photos

`/img/` holds 29 real job photos, the van and trailer, and the real logo, all
taken from Tom's old website gallery (converted to WebP, with location data
removed). The old site had **no captions**, so captions and alt text describe
only what is visible ("Two-story home, gray siding").

To label a photo once Tom confirms it, edit `CONFIRMED` in `build/photos.py`:

```python
CONFIRMED = {"tearoff": ("Roof replacement", "Verona", "roofing")}
```

and rebuild. The caption becomes "Roof replacement, Verona", the alt text gets
the town, and the gallery filter buttons appear once photos have categories.

Still placeholders: the two certification badges. Not used from the old site:
promo banners, 3 stock-looking images, and the trailer close-up that shows the
old (608) 845-9100 number.

## Before launch (search the code for `TODO` and `[`)

- [ ] Ask Tom the job type + town for each photo (`CONFIRMED` in `build/photos.py`), and for a photo of himself
- [ ] Town-specific jobs for each town page (`build/towns.py`)
- [ ] Real hours: enter in the admin under Business info
- [ ] Origin story on the About page (`[CONFIRMED STORY FROM TOM]` in `build/pages.py`)
- [ ] Set `ADMIN_SETUP_KEY`, create the admin login, set up SMTP and send a test email
- [ ] Confirm the Google Place ID `ChIJ9YIRPSixB4gRX6Hj33m4fFA` is Tom's listing (taken from a public directory; review buttons use it)
- [ ] Check for a duplicate old Google listing, "The Hardtland Company, Inc." near Verona (linked from the old site); merge or remove it
- [ ] CertainTeed and Owens Corning badge files (logo is in `img/hardtland-logo.png`)
- [ ] Full review text from Google (currently excerpts) in `build/common.py`
- [ ] Confirm domain (`DOMAIN` in `build/common.py`) and set up 301s from old URLs
- [ ] Optional: replace `/img/og-hardtland.jpg` with a branded version using a real job photo (1200x630)
- [ ] Uncomment the HTTPS + www redirect in `.htaccess` once SSL is live
- [ ] Have the privacy policy reviewed
