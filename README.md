# Hardtland Home Improvement website

The whole website is in **`hardtlandhomeimprovement/`**. Netlify publishes that
folder as-is (settings in `netlify.toml`); there is no build step on Netlify.

## Deploy on Netlify

1. Netlify > **Add new site** > **Import an existing project** > GitHub > this repo.
2. Branch: the one with this code. Netlify reads `netlify.toml`, so leave
   build command empty and publish directory as `hardtlandhomeimprovement`.
3. **Domain:** add `www.hardtlandhomeimprovement.com` as the primary domain.
   Netlify turns on HTTPS and redirects the bare domain to `www` for you.
4. **Form emails:** Site configuration > **Forms** > enable form detection, then
   **Form notifications** > Add notification > Email > form `free-inspection`
   > send to `tomd@tds.net`. Every request also shows under **Forms** in the
   Netlify dashboard, with spam filtering.
5. After the first deploy, send a test request from the live site and check
   that it appears under Forms and in Tom's inbox.

## What does not run on Netlify

Netlify hosts static files only, so the PHP parts are kept in the folder but
blocked from the web there (`/admin/`, `/lead.php`, `/inc/`, `/data/`):

- The `/admin/` panel (leads list, editing hours/phone/rating, SMTP settings).
- `lead.php` (on Netlify, Netlify Forms handles the form instead).

To change hours, phone, rating or links on Netlify: edit
`hardtlandhomeimprovement/data/site.json`, run
`python3 hardtlandhomeimprovement/build/build.py` (needs Python + PHP), commit,
and Netlify redeploys. If Tom should edit these himself in a browser, either
host on a PHP web host (set `HOSTING = "php"` in `build/common.py` and rebuild),
or add a Git-based CMS on Netlify.

Full details: `hardtlandhomeimprovement/README.md`.
