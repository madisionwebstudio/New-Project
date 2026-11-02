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

Every image in `/img/` is currently a grey **PHOTO PLACEHOLDER**. To add a real
photo, save it as WebP with the **same file name** and drop it into `/img/`.
The build never overwrites a real photo. Captions and alt text live in the
build files; update a caption if the real job's town or type differs.

Quick list of all placeholder names: `ls img/`

## Before launch (search the code for `TODO` and `[`)

- [ ] Real job photos (homepage, service pages, town pages, gallery, Tom photos)
- [ ] Real jobs from Tom for each town page (`build/towns.py`)
- [ ] Real hours: enter in the admin under Business info
- [ ] Origin story on the About page (`[CONFIRMED STORY FROM TOM]` in `build/pages.py`)
- [ ] Set `ADMIN_SETUP_KEY`, create the admin login, set up SMTP and send a test email
- [ ] Google, Facebook, Yelp links and the direct Google review link: admin, Business info
- [ ] Logo file, CertainTeed and Owens Corning badge files
- [ ] Full review text from Google (currently excerpts) in `build/common.py`
- [ ] Confirm domain (`DOMAIN` in `build/common.py`) and set up 301s from old URLs
- [ ] Open Graph image `/img/og-hardtland.jpg` (1200x630)
- [ ] Have the privacy policy reviewed
