<?php
/**
 * Command line only: apply data/site.json (hours, phone, rating...) to freshly
 * built pages. build/build.py runs this automatically after generating HTML.
 *     php inc/publish-cli.php [folder]
 */
declare(strict_types=1);
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }

require __DIR__ . '/app.php';

if (!is_file(data_path('site.json'))) write_json('site.json', site());
$seed = array_replace(site_defaults(), SEED_SITE);   // what a fresh build contains
$dir = $argv[1] ?? SITE_ROOT;          // folder with the built pages (default: this site)
$r = publish_site($seed, site(), $dir);
echo "Applied data/site.json to {$r['changed']} of {$r['total']} pages.\n";
if ($r['errors']) { fwrite(STDERR, "Could not write: " . implode(', ', $r['errors']) . "\n"); exit(1); }
