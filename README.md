# Hardtland Home Improvement website

This repo holds **two copies** of the same site, built from one source:

| Where | What it's for | Form | Search engines |
|---|---|---|---|
| **repo root** (this folder) | **Netlify preview** for the client, now | Netlify Forms | blocked (`noindex`, `robots.txt`) |
| **`hardtlandhomeimprovement/`** | **Real domain** on a PHP host, once the client agrees | `lead.php` + `/admin/` panel | open (sitemap, schema, SEO) |

Edit content only in `hardtlandhomeimprovement/build/`, then rebuild both:

```
python3 hardtlandhomeimprovement/build/build.py           # both copies
python3 hardtlandhomeimprovement/build/build.py netlify   # just the preview
python3 hardtlandhomeimprovement/build/build.py php       # just the real-domain folder
```

(Needs Python 3 with Pillow, and PHP 8.1+.) Commit, and Netlify redeploys.

## Netlify preview setup

1. Netlify > **Add new site** > **Import an existing project** > GitHub > this repo
   and branch. `netlify.toml` sets everything: publish the repo root, no build command.
2. Use the free `*.netlify.app` address (rename it under Site configuration if you like).
   Don't point the real domain here; the preview is `noindex` on purpose.
3. **Form emails:** Site configuration > **Forms** > enable form detection, then
   **Form notifications** > Email > form `free-inspection` > `tomd@tds.net`.
   Requests also show under **Forms** in the Netlify dashboard.
4. Send a test request from the preview and check Forms + the inbox.

The `/admin/` panel does not exist on the preview (Netlify can't run PHP).

## Going live on the real domain

Upload the **contents of `hardtlandhomeimprovement/`** (everything except its
`build/` folder) to a PHP web host for www.hardtlandhomeimprovement.com, then
follow "First-time setup" in `hardtlandhomeimprovement/README.md` (admin login,
email/SMTP, real hours). That copy is fully indexable, with the sitemap,
redirects and admin panel.
