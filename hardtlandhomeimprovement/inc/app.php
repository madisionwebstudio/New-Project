<?php
/**
 * Hardtland — shared PHP for the lead form (lead.php) and the admin panel (admin/).
 *
 *  - Leads are saved to SQLite first, then emailed, so a mail problem never loses a lead.
 *  - Business info (hours, phone, rating...) lives in data/site.json. Saving it in the
 *    admin rewrites the matching spots in every static .html page ("publishing"),
 *    so the public site stays plain, fast HTML.
 */
declare(strict_types=1);

require __DIR__ . '/config.php';

const LEAD_NEEDS = ['Roof repair', 'Roof replacement', 'Storm/hail damage', 'Siding',
                    'Gutters', 'Windows/doors', 'Other'];
const LEAD_STATUSES = ['new' => 'New', 'contacted' => 'Contacted', 'scheduled' => 'Inspection set',
                       'won' => 'Won', 'lost' => 'Lost', 'spam' => 'Spam'];
const DAYS = ['mon' => 'Mon', 'tue' => 'Tue', 'wed' => 'Wed', 'thu' => 'Thu',
              'fri' => 'Fri', 'sat' => 'Sat', 'sun' => 'Sun'];
const DAY_SCHEMA = ['mon' => 'Monday', 'tue' => 'Tuesday', 'wed' => 'Wednesday', 'thu' => 'Thursday',
                    'fri' => 'Friday', 'sat' => 'Saturday', 'sun' => 'Sunday'];

/** Values the generated HTML is built with (build/common.py uses the same ones). */
const SEED_SITE = [
    'phone' => '(608) 575-9317',
    'email' => 'tomd@tds.net',
    'street' => '5821 Thrush Ln',
    'city' => 'Madison',
    'state' => 'WI',
    'zip' => '53711',
    'rating' => '4.7',
    'review_count' => '32',
    'google_review_url' => 'https://www.google.com/maps/search/?api=1&query=Hardtland+Home+Improvement+Inc+5821+Thrush+Ln+Madison+WI',
];

function h(?string $s): string
{
    return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function one_line(string $s): string
{
    return trim(preg_replace('/[\r\n\t\0]+/', ' ', $s));
}

function clean_text(string $v, int $max): string
{
    $v = trim(str_replace(["\r", "\0"], '', $v));
    return mb_substr(strip_tags($v), 0, $max);
}

// ---------------------------------------------------------------------------
// JSON storage (data/site.json is public business info; data/settings.json is private)
// ---------------------------------------------------------------------------
function data_path(string $file): string
{
    return rtrim(DATA_DIR, '/') . '/' . $file;
}

function read_json(string $file): array
{
    $p = data_path($file);
    if (!is_file($p)) return [];
    $d = json_decode((string)file_get_contents($p), true);
    return is_array($d) ? $d : [];
}

function write_json(string $file, array $data): void
{
    $p = data_path($file);
    $tmp = $p . '.tmp' . bin2hex(random_bytes(4));
    $json = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . "\n";
    if (@file_put_contents($tmp, $json, LOCK_EX) === false || !@rename($tmp, $p)) {
        @unlink($tmp);
        throw new RuntimeException("Could not save $file. Check that the data folder is writable.");
    }
    if ($file === 'settings.json') @chmod($p, 0600);
}

function site_defaults(): array
{
    $hours = [];
    foreach (DAYS as $k => $_) $hours[$k] = null;
    return SEED_SITE + [
        'hours' => $hours,
        'hours_note' => '[REAL HOURS FROM TOM]',
        'google_profile_url' => '',
        'facebook_url' => '',
        'yelp_url' => '',
        'notice_text' => '',
        'notice_link' => '',
        'ga4_id' => '',              // Google Analytics 4, e.g. G-ABC123XYZ
        'gsc_verification' => '',    // Google Search Console HTML-tag code
        'bing_verification' => '',   // Bing Webmaster Tools code
    ];
}

function site(): array
{
    $s = array_replace(site_defaults(), read_json('site.json'));
    $s['hours'] = array_replace(site_defaults()['hours'], (array)($s['hours'] ?? []));
    return $s;
}

function settings(): array
{
    $defaults = [
        'admin_user' => '',
        'admin_hash' => '',
        'secret' => '',
        'mail' => [
            'to' => 'tomd@tds.net',
            'from_name' => 'Hardtland Website',
            'from_email' => '',
            'method' => 'mail',          // 'mail' (PHP mail) or 'smtp'
            'smtp_host' => '',
            'smtp_port' => 587,
            'smtp_secure' => 'tls',      // 'tls' (STARTTLS), 'ssl', or 'none'
            'smtp_user' => '',
            'smtp_pass' => '',
        ],
    ];
    $s = read_json('settings.json');
    $out = array_replace($defaults, $s);
    $out['mail'] = array_replace($defaults['mail'], (array)($s['mail'] ?? []));
    if ($out['secret'] === '') {
        $out['secret'] = bin2hex(random_bytes(32));
        try { write_json('settings.json', $out); } catch (Throwable $e) { /* reported by checks */ }
    }
    return $out;
}

function save_settings(array $s): void
{
    write_json('settings.json', $s);
}

// ---------------------------------------------------------------------------
// Database (leads + rate limiting)
// ---------------------------------------------------------------------------
function db(): PDO
{
    static $pdo = null;
    if ($pdo) return $pdo;
    $pdo = new PDO('sqlite:' . data_path('hardtland.sqlite'), null, null, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);
    $pdo->exec('PRAGMA busy_timeout = 5000');
    $pdo->exec('CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at INTEGER NOT NULL,
        updated_at INTEGER NOT NULL,
        name TEXT NOT NULL, phone TEXT NOT NULL, address TEXT NOT NULL, need TEXT NOT NULL,
        source_page TEXT NOT NULL DEFAULT "/",
        status TEXT NOT NULL DEFAULT "new",
        notes TEXT NOT NULL DEFAULT "",
        email_status TEXT NOT NULL DEFAULT "pending",
        email_error TEXT NOT NULL DEFAULT "",
        ip_hash TEXT NOT NULL DEFAULT ""
    )');
    $pdo->exec('CREATE INDEX IF NOT EXISTS leads_created ON leads(created_at)');
    $pdo->exec('CREATE TABLE IF NOT EXISTS attempts (kind TEXT NOT NULL, key TEXT NOT NULL, at INTEGER NOT NULL)');
    $pdo->exec('CREATE INDEX IF NOT EXISTS attempts_k ON attempts(kind, key, at)');
    return $pdo;
}

function ip_hash(): string
{
    return hash_hmac('sha256', $_SERVER['REMOTE_ADDR'] ?? '0', settings()['secret']);
}

function count_attempts(string $kind, string $key, int $seconds): int
{
    $st = db()->prepare('SELECT COUNT(*) FROM attempts WHERE kind = ? AND key = ? AND at > ?');
    $st->execute([$kind, $key, time() - $seconds]);
    return (int)$st->fetchColumn();
}

function add_attempt(string $kind, string $key): void
{
    db()->prepare('INSERT INTO attempts (kind, key, at) VALUES (?, ?, ?)')->execute([$kind, $key, time()]);
    db()->prepare('DELETE FROM attempts WHERE at < ?')->execute([time() - 86400]);
}

function lead(int $id): ?array
{
    $st = db()->prepare('SELECT * FROM leads WHERE id = ?');
    $st->execute([$id]);
    return $st->fetch() ?: null;
}

// ---------------------------------------------------------------------------
// Email: PHP mail() or a small built-in SMTP client (STARTTLS/SSL + AUTH LOGIN)
// ---------------------------------------------------------------------------
function default_from_email(): string
{
    $host = preg_replace('/^www\./', '', (string)parse_url(SITE_URL, PHP_URL_HOST));
    return 'no-reply@' . ($host ?: 'localhost');
}

function parse_recipients(string $list): array
{
    $out = [];
    foreach (preg_split('/[,;\s]+/', $list) as $e) {
        $e = trim($e);
        if ($e !== '' && filter_var($e, FILTER_VALIDATE_EMAIL)) $out[] = $e;
    }
    return array_values(array_unique($out));
}

/** Returns '' on success, or an error message. */
function send_mail(string $subject, string $body, array $mailCfg = null): string
{
    $m = $mailCfg ?? settings()['mail'];
    $to = parse_recipients((string)$m['to']);
    if (!$to) return 'No valid "send leads to" address is set.';
    $from = filter_var($m['from_email'], FILTER_VALIDATE_EMAIL) ? $m['from_email'] : default_from_email();
    $fromName = one_line((string)$m['from_name']) ?: 'Website';
    $subjectEnc = '=?UTF-8?B?' . base64_encode(one_line($subject)) . '?=';
    $body = str_replace(["\r\n", "\r"], "\n", $body);

    $headers = [
        'From: =?UTF-8?B?' . base64_encode($fromName) . '?= <' . $from . '>',
        'Date: ' . date('r'),
        'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . substr(strrchr($from, '@'), 1) . '>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: base64',
    ];
    $encodedBody = chunk_split(base64_encode($body));

    try {
        if (($m['method'] ?? 'mail') === 'smtp') {
            smtp_send($m, $from, $to, array_merge([
                'To: ' . implode(', ', $to),
                'Subject: ' . $subjectEnc,
            ], $headers), $encodedBody);
            return '';
        }
        $ok = @mail(implode(', ', $to), $subjectEnc, $encodedBody, implode("\r\n", $headers), '-f' . $from);
        return $ok ? '' : 'PHP mail() failed. Try SMTP settings instead.';
    } catch (Throwable $e) {
        return $e->getMessage();
    }
}

function smtp_send(array $m, string $from, array $to, array $headers, string $body): void
{
    $host = trim((string)$m['smtp_host']);
    $port = (int)$m['smtp_port'] ?: 587;
    $secure = $m['smtp_secure'] ?? 'tls';
    if ($host === '') throw new RuntimeException('SMTP server is not set.');

    $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true, 'peer_name' => $host]]);
    $fp = @stream_socket_client(($secure === 'ssl' ? 'ssl://' : 'tcp://') . $host . ':' . $port,
        $errno, $errstr, 15, STREAM_CLIENT_CONNECT, $ctx);
    if (!$fp) throw new RuntimeException("Could not connect to $host:$port ($errstr)");
    stream_set_timeout($fp, 20);

    $read = function () use ($fp): string {
        $data = '';
        while (($line = fgets($fp, 1024)) !== false) {
            $data .= $line;
            if (strlen($line) < 4 || $line[3] === ' ') break;
        }
        return $data;
    };
    $expect = function ($codes) use ($read): string {
        $r = $read();
        if (!in_array((int)substr($r, 0, 3), (array)$codes, true)) {
            throw new RuntimeException('Mail server said: ' . trim($r ?: 'no response'));
        }
        return $r;
    };
    $cmd = function (string $c, $codes) use ($fp, $expect): string {
        fwrite($fp, $c . "\r\n");
        return $expect($codes);
    };

    try {
        $expect(220);
        $helo = 'EHLO ' . (preg_replace('/[^A-Za-z0-9.\-]/', '', $_SERVER['SERVER_NAME'] ?? '') ?: 'localhost');
        $cmd($helo, 250);
        if ($secure === 'tls') {
            $cmd('STARTTLS', 220);
            $method = STREAM_CRYPTO_METHOD_TLS_CLIENT;
            if (defined('STREAM_CRYPTO_METHOD_TLSv1_2_CLIENT')) $method |= STREAM_CRYPTO_METHOD_TLSv1_2_CLIENT;
            if (defined('STREAM_CRYPTO_METHOD_TLSv1_3_CLIENT')) $method |= STREAM_CRYPTO_METHOD_TLSv1_3_CLIENT;
            if (!@stream_socket_enable_crypto($fp, true, $method)) throw new RuntimeException('Could not start a secure (TLS) connection.');
            $cmd($helo, 250);
        }
        if ((string)$m['smtp_user'] !== '') {
            $cmd('AUTH LOGIN', 334);
            $cmd(base64_encode((string)$m['smtp_user']), 334);
            $cmd(base64_encode((string)$m['smtp_pass']), 235);
        }
        $cmd('MAIL FROM:<' . $from . '>', 250);
        foreach ($to as $rcpt) $cmd('RCPT TO:<' . $rcpt . '>', [250, 251]);
        $cmd('DATA', 354);
        $msg = implode("\r\n", $headers) . "\r\n\r\n" . str_replace("\n", "\r\n", rtrim($body, "\n"));
        $msg = preg_replace('/^\./m', '..', $msg);
        fwrite($fp, $msg . "\r\n.\r\n");
        $expect(250);
        @fwrite($fp, "QUIT\r\n");
    } finally {
        fclose($fp);
    }
}

function email_lead(array $lead): string
{
    $when = date('D, M j, Y \a\t g:i A', (int)$lead['created_at']);
    $digits = preg_replace('/\D/', '', $lead['phone']);
    $body = "New free inspection request from the website\n"
        . "=============================================\n\n"
        . "Name:     {$lead['name']}\n"
        . "Phone:    {$lead['phone']}\n"
        . "Address:  {$lead['address']}\n"
        . "Needs:    {$lead['need']}\n"
        . "Page:     {$lead['source_page']}\n"
        . "Received: $when\n\n"
        . "Call or text: tel:+1" . substr($digits, -10) . "\n"
        . "Map: https://www.google.com/maps/search/?api=1&query=" . rawurlencode($lead['address']) . "\n\n"
        . "Open in admin: " . SITE_URL . "/admin/?view=lead&id={$lead['id']}\n\n"
        . "Promise on the site: Tom or the crew will call back within 1 business day.\n";
    $subject = "New inspection request: {$lead['need']} - {$lead['name']}";
    return send_mail($subject, $body);
}

function record_email_result(int $id, string $err): void
{
    db()->prepare('UPDATE leads SET email_status = ?, email_error = ?, updated_at = ? WHERE id = ?')
        ->execute([$err === '' ? 'sent' : 'failed', $err, time(), $id]);
}

// ---------------------------------------------------------------------------
// Rendering business info into the static pages
// ---------------------------------------------------------------------------
function phone_parts(string $phone): array
{
    $d = substr(preg_replace('/\D/', '', $phone), -10);
    if (strlen($d) !== 10) return ['display' => $phone, 'e164' => '', 'ld' => ''];
    return [
        'display' => sprintf('(%s) %s-%s', substr($d, 0, 3), substr($d, 3, 3), substr($d, 6)),
        'e164' => '+1' . $d,
        'ld' => sprintf('+1-%s-%s-%s', substr($d, 0, 3), substr($d, 3, 3), substr($d, 6)),
    ];
}

function fmt_time(string $t): string
{
    [$hr, $mi] = array_map('intval', explode(':', $t) + [0, 0]);
    $ap = $hr >= 12 ? 'PM' : 'AM';
    $h12 = $hr % 12 ?: 12;
    return $mi ? sprintf('%d:%02d %s', $h12, $mi, $ap) : "$h12 $ap";
}

function day_open(array $site, string $day): ?array
{
    $v = $site['hours'][$day] ?? null;
    return (is_array($v) && !empty($v['open']) && !empty($v['close'])) ? $v : null;
}

function hours_are_set(array $site): bool
{
    foreach (DAYS as $k => $_) if (day_open($site, $k)) return true;
    return false;
}

/** Groups days with the same hours: [["Mon–Fri", "7 AM – 6 PM"], ["Sun", "Closed"]] */
function hours_groups(array $site): array
{
    $groups = [];
    foreach (DAYS as $k => $_) {
        $v = day_open($site, $k);
        $txt = $v ? fmt_time($v['open']) . ' – ' . fmt_time($v['close']) : 'Closed';
        $i = count($groups) - 1;
        if ($i >= 0 && $groups[$i]['text'] === $txt) $groups[$i]['end'] = $k;
        else $groups[] = ['start' => $k, 'end' => $k, 'text' => $txt];
    }
    return array_map(fn($g) => [DAYS[$g['start']] . ($g['end'] !== $g['start'] ? '–' . DAYS[$g['end']] : ''), $g['text']], $groups);
}

function render_hours(array $site): string
{
    $out = '';
    if (hours_are_set($site)) {
        foreach (hours_groups($site) as [$days, $txt]) {
            $out .= '<span class="hours-row"><span class="hours-day">' . h($days) . '</span> <span>' . h($txt) . '</span></span>';
        }
    }
    if (trim($site['hours_note']) !== '') $out .= '<span class="hours-note">' . h($site['hours_note']) . '</span>';
    if ($out === '') $out = '<span class="hours-note">Call or text for hours</span>';
    return '<span class="hours">' . $out . '</span>';
}

function render_notice(array $site): string
{
    $t = trim((string)$site['notice_text']);
    if ($t === '') return '';
    $link = trim((string)$site['notice_link']);
    $more = $link !== '' ? ' <a href="' . h($link) . '">Learn more</a>' : '';
    return '<div class="notice-bar" role="note"><div class="container">' . h($t) . $more . '</div></div>';
}

function render_business_ld(array $site): string
{
    $p = phone_parts($site['phone']);
    $ld = [
        '@context' => 'https://schema.org',
        '@type' => 'RoofingContractor',
        '@id' => SITE_URL . '/#business',
        'name' => BIZ_NAME,
        'url' => SITE_URL . '/',
        'logo' => SITE_URL . '/img/hardtland-logo.png',
        'image' => SITE_URL . '/img/hero-roof-replacement-verona-1600.webp',
        'telephone' => $p['ld'] ?: $site['phone'],
        'email' => $site['email'],
        'foundingDate' => '1972',
        'founder' => ['@type' => 'Person', 'name' => 'Tom Degenhardt'],
        'address' => [
            '@type' => 'PostalAddress',
            'streetAddress' => $site['street'],
            'addressLocality' => $site['city'],
            'addressRegion' => $site['state'],
            'postalCode' => $site['zip'],
            'addressCountry' => 'US',
        ],
        'geo' => ['@type' => 'GeoCoordinates', 'latitude' => 43.0295, 'longitude' => -89.4822],
        'areaServed' => array_merge(
            array_map(fn($t) => ['@type' => 'City', 'name' => "$t, WI"],
                ['Verona', 'Madison', 'Fitchburg', 'Middleton', 'Oregon', 'Mount Horeb']),
            array_map(fn($c) => ['@type' => 'AdministrativeArea', 'name' => "$c County, WI"], ['Dane', 'Green', 'Rock'])
        ),
        'paymentAccepted' => 'Insurance, Personal Check, Cash, Zelle',
        'currenciesAccepted' => 'USD',
        'slogan' => "Madison & Verona's Roofer Since 1972",
        'hasMap' => 'https://www.google.com/maps/search/?api=1&query=' . rawurlencode(BIZ_NAME . ', ' . $site['street'] . ', ' . $site['city'] . ', ' . $site['state'] . ' ' . $site['zip']),
        'contactPoint' => [
            '@type' => 'ContactPoint',
            'contactType' => 'customer service',
            'telephone' => $p['ld'] ?: $site['phone'],
            'email' => $site['email'],
            'areaServed' => 'US-WI',
            'availableLanguage' => 'English',
        ],
        'knowsAbout' => ['Roof replacement', 'Roof repair', 'Hail and storm damage', 'Roof insurance claims',
                         'Metal roofing', 'Siding', 'Soffit and fascia', 'Gutters and gutter guards',
                         'Window and door replacement'],
        'hasOfferCatalog' => [
            '@type' => 'OfferCatalog',
            'name' => 'Roofing and exterior services',
            'itemListElement' => array_map(fn($svc) => ['@type' => 'Offer', 'itemOffered' => [
                '@type' => 'Service', 'name' => $svc[1], 'url' => SITE_URL . '/' . $svc[0] . '/']], [
                ['roof-replacement', 'Roof Replacement'], ['roof-repair', 'Roof Repair'],
                ['storm-hail-damage', 'Storm & Hail Damage Repair'], ['insurance-claims', 'Roof Insurance Claim Help'],
                ['metal-roofing', 'Metal Roofing'], ['free-roof-inspection', 'Free Roof Inspection'],
                ['siding', 'Siding'], ['gutters', 'Gutters & Gutter Guards'], ['windows-doors', 'Window & Door Replacement'],
            ]),
        ],
    ];
    if (hours_are_set($site)) {
        $groups = [];
        foreach (DAYS as $k => $_) {
            if (!$v = day_open($site, $k)) continue;
            $key = $v['open'] . '-' . $v['close'];
            $groups[$key] ??= ['@type' => 'OpeningHoursSpecification', 'dayOfWeek' => [], 'opens' => $v['open'], 'closes' => $v['close']];
            $groups[$key]['dayOfWeek'][] = DAY_SCHEMA[$k];
        }
        $ld['openingHoursSpecification'] = array_values($groups);
    }
    if ((float)$site['rating'] > 0 && (int)$site['review_count'] > 0) {
        $ld['aggregateRating'] = ['@type' => 'AggregateRating', 'ratingValue' => (string)$site['rating'],
                                  'reviewCount' => (string)$site['review_count'], 'bestRating' => '5'];
    }
    $ld['hasCredential'] = [
        ['@type' => 'EducationalOccupationalCredential', 'name' => 'CertainTeed Master Shingler'],
        ['@type' => 'EducationalOccupationalCredential', 'name' => 'Owens Corning Certified'],
    ];
    $same = array_values(array_filter([$site['google_profile_url'], $site['facebook_url'], $site['yelp_url']]));
    if ($same) $ld['sameAs'] = $same;
    $json = json_encode($ld, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    $json = str_replace('</', '<\/', $json);
    return "<script type=\"application/ld+json\">\n$json\n</script>";
}

function render_tracking(array $site): string
{
    $out = '';
    if ($site['gsc_verification'] !== '') $out .= '<meta name="google-site-verification" content="' . h($site['gsc_verification']) . '">';
    if ($site['bing_verification'] !== '') $out .= '<meta name="msvalidate.01" content="' . h($site['bing_verification']) . '">';
    if ($site['ga4_id'] !== '') {
        $id = h($site['ga4_id']);
        $out .= '<script async src="https://www.googletagmanager.com/gtag/js?id=' . $id . '"></script>'
            . '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
            . "gtag('js',new Date());gtag('config','" . $id . "');</script>";
    }
    return $out;
}

function rendered_blocks(array $site): array
{
    return [
        'tracking' => render_tracking($site),
        'hours' => render_hours($site),
        'notice' => render_notice($site),
        'ld' => render_business_ld($site),
        'rating' => h((string)$site['rating']),
        'reviews' => h((string)$site['review_count']),
    ];
}

/** Old -> new string pairs for values that appear inside text and attributes. */
function replacement_pairs(array $old, array $new): array
{
    $pairs = [];
    $add = function (string $a, string $b) use (&$pairs) {
        if ($a !== '' && $a !== $b) $pairs[$a] = $b;
    };
    $po = phone_parts($old['phone']);
    $pn = phone_parts($new['phone']);
    foreach (['display', 'e164', 'ld'] as $k) $add($po[$k], $pn[$k]);
    $add('mailto:' . $old['email'], 'mailto:' . $new['email']);
    $add('>' . $old['email'] . '<', '>' . $new['email'] . '<');
    $add('"email": "' . $old['email'] . '"', '"email": "' . $new['email'] . '"');
    $add(h($old['google_review_url']), h($new['google_review_url']));
    // address (text, map queries and service schema)
    $add($old['street'], $new['street']);
    $add(str_replace(' ', '+', $old['street']), str_replace(' ', '+', $new['street']));
    $add("{$old['street']}, {$old['city']}, {$old['state']} {$old['zip']}", "{$new['street']}, {$new['city']}, {$new['state']} {$new['zip']}");
    $add("{$old['street']}, {$old['city']}, {$old['state']}", "{$new['street']}, {$new['city']}, {$new['state']}");
    $add("{$old['city']}, {$old['state']} {$old['zip']}", "{$new['city']}, {$new['state']} {$new['zip']}");
    $add("+{$old['city']},+{$old['state']}+{$old['zip']}", "+{$new['city']},+{$new['state']}+{$new['zip']}");
    $add('"postalCode": "' . $old['zip'] . '"', '"postalCode": "' . $new['zip'] . '"');
    $add('"addressLocality": "' . $old['city'] . '"', '"addressLocality": "' . $new['city'] . '"');
    return $pairs;
}

function site_html_files(?string $root = null): array
{
    $root = $root ?? SITE_ROOT;
    $skip = ['build', 'data', 'inc', 'admin', '.git', 'node_modules'];
    if (realpath($root) !== realpath(SITE_ROOT)) $skip[] = basename(SITE_ROOT);   // repo-root preview copy
    $files = [];
    $it = new RecursiveIteratorIterator(new RecursiveCallbackFilterIterator(
        new RecursiveDirectoryIterator($root, FilesystemIterator::SKIP_DOTS),
        function ($f) use ($skip) {
            if ($f->isDir()) return !in_array($f->getFilename(), $skip, true);
            return strtolower($f->getExtension()) === 'html';
        }
    ));
    foreach ($it as $f) $files[] = $f->getPathname();
    sort($files);
    return $files;
}

/**
 * Apply business info to every page. Returns ['changed' => n, 'total' => n, 'errors' => [...]].
 * $old is what the pages currently contain; $new is what they should say.
 */
function publish_site(array $old, array $new, ?string $root = null): array
{
    $blocks = rendered_blocks($new);
    $pairs = replacement_pairs($old, $new);
    $changed = 0;
    $errors = [];
    $files = site_html_files($root);
    foreach ($files as $file) {
        $html = (string)file_get_contents($file);
        $orig = $html;
        $html = preg_replace_callback('/<!--biz:([a-z]+)-->.*?<!--\/biz:\1-->/s', function ($m) use ($blocks) {
            return isset($blocks[$m[1]]) ? "<!--biz:{$m[1]}-->" . $blocks[$m[1]] . "<!--/biz:{$m[1]}-->" : $m[0];
        }, $html);
        if ($pairs) $html = strtr($html, $pairs);
        // rating inside <title>/<meta> (comments can't go there)
        if ((string)$old['rating'] !== (string)$new['rating'] && ($pos = stripos($html, '</head>')) !== false) {
            $head = substr($html, 0, $pos);
            $head = str_replace([$old['rating'] . ' Stars on Google', $old['rating'] . ' stars on Google'],
                                [$new['rating'] . ' Stars on Google', $new['rating'] . ' stars on Google'], $head);
            $html = $head . substr($html, $pos);
        }
        if ($html !== $orig) {
            if (@file_put_contents($file, $html, LOCK_EX) === false) {
                $errors[] = substr($file, strlen(SITE_ROOT));
            } else {
                $changed++;
            }
        }
    }
    return ['changed' => $changed, 'total' => count($files), 'errors' => $errors];
}

function system_checks(): array
{
    $checks = [];
    $checks[] = ['Data folder is writable', is_dir(DATA_DIR) && is_writable(DATA_DIR)];
    $checks[] = ['SQLite database available', class_exists('PDO') && in_array('sqlite', PDO::getAvailableDrivers(), true)];
    $notWritable = array_filter(site_html_files(), fn($f) => !is_writable($f));
    $checks[] = ['Website pages can be updated' . ($notWritable ? ' (' . count($notWritable) . ' read-only)' : ''), !$notWritable];
    $checks[] = ['Setup key changed from default', ADMIN_SETUP_KEY !== 'CHANGE-ME-BEFORE-UPLOAD'];
    $checks[] = ['Site is using HTTPS', (($_SERVER['HTTPS'] ?? '') !== '' && $_SERVER['HTTPS'] !== 'off') || PHP_SAPI === 'cli'];
    return $checks;
}
