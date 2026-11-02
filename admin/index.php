<?php
/**
 * Hardtland admin panel: /admin/
 *  - Leads: every inspection request, with status, notes and CSV export
 *  - Business info: hours, phone, email, address, Google rating, links, notice bar
 *  - Email: where leads go, and how the site sends mail (PHP mail or SMTP)
 *  - Account: change username / password
 */
declare(strict_types=1);

require dirname(__DIR__) . '/inc/app.php';

header('X-Frame-Options: DENY');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: same-origin');
header('Cache-Control: no-store');
header("Content-Security-Policy: default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; form-action 'self'; frame-ancestors 'none'");

$https = (($_SERVER['HTTPS'] ?? '') !== '' && $_SERVER['HTTPS'] !== 'off');
session_name('hl_admin');
session_set_cookie_params(['lifetime' => 0, 'path' => '/admin/', 'secure' => $https, 'httponly' => true, 'samesite' => 'Strict']);
session_start();

const IDLE_LIMIT = 8 * 3600;

// ---------------------------------------------------------------------------
// helpers
// ---------------------------------------------------------------------------
function csrf(): string
{
    $_SESSION['csrf'] ??= bin2hex(random_bytes(32));
    return $_SESSION['csrf'];
}

function csrf_field(): string
{
    return '<input type="hidden" name="csrf" value="' . h(csrf()) . '">';
}

function check_csrf(): void
{
    if (!hash_equals(csrf(), (string)($_POST['csrf'] ?? ''))) {
        http_response_code(400);
        exit('Your session expired. Go back, reload the page and try again.');
    }
}

function flash(string $msg, string $type = 'ok'): void
{
    $_SESSION['flash'][] = [$type, $msg];
}

function go(string $query = ''): never
{
    header('Location: /admin/' . ($query !== '' ? '?' . $query : ''), true, 303);
    exit;
}

function logged_in(): bool
{
    if (empty($_SESSION['uid'])) return false;
    if (time() - ($_SESSION['seen'] ?? 0) > IDLE_LIMIT) {
        session_unset();
        return false;
    }
    $_SESSION['seen'] = time();
    return true;
}

function post(string $k, int $max = 500): string
{
    return trim(mb_substr((string)($_POST[$k] ?? ''), 0, $max));
}

function fmt_date(int $t): string
{
    return date('M j, Y g:i A', $t);
}

function ago(int $t): string
{
    $d = time() - $t;
    if ($d < 60) return 'just now';
    if ($d < 3600) return floor($d / 60) . ' min ago';
    if ($d < 86400) return floor($d / 3600) . ' hr ago';
    if ($d < 86400 * 7) return floor($d / 86400) . ' days ago';
    return date('M j', $t);
}

function icon(string $name): string
{
    $p = [
        'inbox' => '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
        'store' => '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
        'mail' => '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
        'user' => '<circle cx="12" cy="8" r="4"/><path d="M4 21v-1a6 6 0 0 1 6-6h4a6 6 0 0 1 6 6v1"/>',
        'phone' => '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
        'message' => '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
        'map' => '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
        'download' => '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
        'external' => '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
        'logout' => '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5"/><path d="M21 12H9"/>',
        'back' => '<path d="m15 18-6-6 6-6"/>',
    ][$name] ?? '';
    return '<svg class="i" viewBox="0 0 24 24" aria-hidden="true">' . $p . '</svg>';
}

// ---------------------------------------------------------------------------
// layout
// ---------------------------------------------------------------------------
function page(string $title, string $body, string $active = ''): never
{
    $flash = '';
    foreach ($_SESSION['flash'] ?? [] as [$type, $msg]) {
        $flash .= '<div class="flash flash--' . h($type) . '" role="status">' . h($msg) . '</div>';
    }
    unset($_SESSION['flash']);

    $nav = '';
    if (logged_in()) {
        $newCount = (int)db()->query("SELECT COUNT(*) FROM leads WHERE status = 'new'")->fetchColumn();
        $items = [
            'leads' => ['Leads', 'inbox', $newCount ? '<span class="count">' . $newCount . '</span>' : ''],
            'business' => ['Business info', 'store', ''],
            'email' => ['Email', 'mail', ''],
            'account' => ['Account', 'user', ''],
        ];
        foreach ($items as $k => [$label, $ic, $extra]) {
            $cur = $k === $active ? ' aria-current="page"' : '';
            $nav .= '<a href="/admin/?view=' . $k . '"' . $cur . '>' . icon($ic) . '<span>' . $label . '</span>' . $extra . '</a>';
        }
        $nav = '<nav class="nav" aria-label="Admin">' . $nav . '</nav>'
            . '<div class="top-actions"><a class="btn-ghost" href="/" target="_blank" rel="noopener">' . icon('external') . '<span>View site</span></a>'
            . '<form method="post" action="/admin/?view=logout">' . csrf_field() . '<button class="btn-ghost" type="submit">' . icon('logout') . '<span>Log out</span></button></form></div>';
    }

    echo '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        . '<meta name="viewport" content="width=device-width, initial-scale=1">'
        . '<meta name="robots" content="noindex, nofollow">'
        . '<title>' . h($title) . ' | Hardtland Admin</title>'
        . '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
        . '<link rel="stylesheet" href="/admin/admin.css">'
        . '<script src="/admin/admin.js" defer></script>'
        . '</head><body>'
        . '<header class="top"><div class="wrap top-inner">'
        . '<a class="brand" href="/admin/"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#E8282B" d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg><span>Hardtland <small>Admin</small></span></a>'
        . $nav . '</div></header>'
        . '<main class="wrap main">' . $flash . $body . '</main>'
        . '</body></html>';
    exit;
}

// ---------------------------------------------------------------------------
// routing
// ---------------------------------------------------------------------------
$view = (string)($_GET['view'] ?? 'leads');
$cfg = settings();

// --- first-time setup ---
if ($cfg['admin_hash'] === '') {
    $err = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        check_csrf();
        $ip = ip_hash();
        if (count_attempts('setup', $ip, 900) >= 5) {
            $err = 'Too many tries. Wait 15 minutes and try again.';
        } elseif (ADMIN_SETUP_KEY === 'CHANGE-ME-BEFORE-UPLOAD') {
            $err = 'Set ADMIN_SETUP_KEY in inc/config.php first.';
        } elseif (!hash_equals(ADMIN_SETUP_KEY, post('setup_key'))) {
            add_attempt('setup', $ip);
            $err = 'That setup key is not right.';
        } elseif (!preg_match('/^[A-Za-z0-9._@-]{3,40}$/', post('username', 40))) {
            $err = 'Username: 3 to 40 letters, numbers or . _ @ -';
        } elseif (mb_strlen((string)($_POST['password'] ?? '')) < 10) {
            $err = 'Password must be at least 10 characters.';
        } elseif (($_POST['password'] ?? '') !== ($_POST['password2'] ?? '')) {
            $err = 'The two passwords do not match.';
        } else {
            $cfg['admin_user'] = post('username', 40);
            $cfg['admin_hash'] = password_hash((string)$_POST['password'], PASSWORD_DEFAULT);
            save_settings($cfg);
            session_regenerate_id(true);
            $_SESSION['uid'] = $cfg['admin_user'];
            $_SESSION['seen'] = time();
            flash('Your admin login is ready. Next, check the Email settings and send a test.');
            go('view=email');
        }
    }
    $keyNote = ADMIN_SETUP_KEY === 'CHANGE-ME-BEFORE-UPLOAD'
        ? '<div class="flash flash--err">Before you can set up, open <code>inc/config.php</code> and change <code>ADMIN_SETUP_KEY</code> to your own secret phrase.</div>' : '';
    page('Set up', '<div class="auth card"><h1>Set up your admin login</h1>'
        . '<p class="muted">This only happens once. You will need the setup key from <code>inc/config.php</code>.</p>' . $keyNote
        . ($err ? '<div class="flash flash--err" role="alert">' . h($err) . '</div>' : '')
        . '<form method="post">' . csrf_field()
        . '<label>Setup key<input name="setup_key" type="password" required autocomplete="off"></label>'
        . '<label>Username<input name="username" required autocomplete="username" value="' . h(post('username', 40)) . '"></label>'
        . '<label>Password <small>(10+ characters)</small><input name="password" type="password" required minlength="10" autocomplete="new-password"></label>'
        . '<label>Confirm password<input name="password2" type="password" required minlength="10" autocomplete="new-password"></label>'
        . '<button class="btn" type="submit">Create login</button></form></div>');
}

// --- login ---
if (!logged_in()) {
    $err = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && $view === 'login') {
        check_csrf();
        $ip = ip_hash();
        if (count_attempts('login', $ip, 900) >= 5) {
            $err = 'Too many failed tries. Wait 15 minutes and try again.';
        } elseif (hash_equals(strtolower($cfg['admin_user']), strtolower(post('username', 40)))
            && password_verify((string)($_POST['password'] ?? ''), $cfg['admin_hash'])) {
            if (password_needs_rehash($cfg['admin_hash'], PASSWORD_DEFAULT)) {
                $cfg['admin_hash'] = password_hash((string)$_POST['password'], PASSWORD_DEFAULT);
                save_settings($cfg);
            }
            session_regenerate_id(true);
            $_SESSION['uid'] = $cfg['admin_user'];
            $_SESSION['seen'] = time();
            go();
        } else {
            add_attempt('login', $ip);
            $err = 'Wrong username or password.';
        }
    }
    page('Log in', '<div class="auth card"><h1>Log in</h1>'
        . ($err ? '<div class="flash flash--err" role="alert">' . h($err) . '</div>' : '')
        . '<form method="post" action="/admin/?view=login">' . csrf_field()
        . '<label>Username<input name="username" required autocomplete="username" autofocus></label>'
        . '<label>Password<input name="password" type="password" required autocomplete="current-password"></label>'
        . '<button class="btn" type="submit">Log in</button></form></div>');
}

// --- logged in from here ---
switch ($view) {
    case 'logout':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            check_csrf();
            session_unset();
            session_destroy();
        }
        header('Location: /admin/', true, 303);
        exit;

    case 'lead':
        view_lead((int)($_GET['id'] ?? 0));

    case 'export':
        export_csv();

    case 'business':
        view_business();

    case 'email':
        view_email();

    case 'account':
        view_account();

    default:
        view_leads();
}

// ---------------------------------------------------------------------------
// Leads
// ---------------------------------------------------------------------------
function status_pill(string $s): string
{
    return '<span class="pill pill--' . h($s) . '">' . h(LEAD_STATUSES[$s] ?? $s) . '</span>';
}

function email_badge(array $l): string
{
    return match ($l['email_status']) {
        'sent' => '<span class="mail-ok" title="Email sent">Emailed</span>',
        'failed' => '<span class="mail-bad" title="' . h($l['email_error']) . '">Email failed</span>',
        default => '<span class="muted">Email pending</span>',
    };
}

function lead_filters(): array
{
    $status = (string)($_GET['status'] ?? 'open');
    $q = trim(mb_substr((string)($_GET['q'] ?? ''), 0, 80));
    $where = [];
    $args = [];
    if ($status === 'open') $where[] = "status IN ('new','contacted','scheduled')";
    elseif (isset(LEAD_STATUSES[$status])) { $where[] = 'status = ?'; $args[] = $status; }
    else $status = 'all';
    if ($q !== '') {
        $where[] = '(name LIKE ? OR phone LIKE ? OR address LIKE ? OR notes LIKE ?)';
        array_push($args, "%$q%", "%$q%", "%$q%", "%$q%");
    }
    return [$status, $q, $where ? 'WHERE ' . implode(' AND ', $where) : '', $args];
}

function view_leads(): never
{
    [$status, $q, $where, $args] = lead_filters();
    $pageNo = max(1, (int)($_GET['p'] ?? 1));
    $per = 50;

    $st = db()->prepare("SELECT COUNT(*) FROM leads $where");
    $st->execute($args);
    $total = (int)$st->fetchColumn();

    $st = db()->prepare("SELECT * FROM leads $where ORDER BY created_at DESC LIMIT $per OFFSET " . (($pageNo - 1) * $per));
    $st->execute($args);
    $rows = $st->fetchAll();

    $n = fn(string $sql, array $a = []) => (function () use ($sql, $a) {
        $s = db()->prepare($sql);
        $s->execute($a);
        return (int)$s->fetchColumn();
    })();
    $stats = [
        ['New', $n("SELECT COUNT(*) FROM leads WHERE status='new'")],
        ['Last 7 days', $n('SELECT COUNT(*) FROM leads WHERE created_at > ?', [time() - 7 * 86400])],
        ['This month', $n('SELECT COUNT(*) FROM leads WHERE created_at >= ?', [strtotime('first day of this month 00:00')])],
        ['Won', $n("SELECT COUNT(*) FROM leads WHERE status='won'")],
    ];
    $failed = $n("SELECT COUNT(*) FROM leads WHERE email_status='failed'");

    $html = '<div class="page-head"><h1>Leads</h1>'
        . '<a class="btn btn--light" href="/admin/?view=export&status=' . h($status) . '&q=' . h(urlencode($q)) . '">' . icon('download') . 'Export CSV</a></div>';
    if ($failed) {
        $html .= '<div class="flash flash--err">' . $failed . ' lead email(s) failed to send. The leads are saved below. Check the <a href="/admin/?view=email">Email settings</a>.</div>';
    }
    $html .= '<div class="stats">';
    foreach ($stats as [$label, $val]) $html .= '<div class="stat"><span>' . h($label) . '</span><strong>' . $val . '</strong></div>';
    $html .= '</div>';

    $tabs = ['open' => 'Open', 'new' => 'New', 'contacted' => 'Contacted', 'scheduled' => 'Inspection set',
             'won' => 'Won', 'lost' => 'Lost', 'spam' => 'Spam', 'all' => 'All'];
    $html .= '<div class="toolbar"><nav class="tabs" aria-label="Filter by status">';
    foreach ($tabs as $k => $label) {
        $cur = $k === $status ? ' aria-current="page"' : '';
        $html .= '<a href="/admin/?view=leads&status=' . $k . ($q !== '' ? '&q=' . h(urlencode($q)) : '') . '"' . $cur . '>' . $label . '</a>';
    }
    $html .= '</nav><form class="search" method="get" role="search"><input type="hidden" name="view" value="leads">'
        . '<input type="hidden" name="status" value="' . h($status) . '">'
        . '<input type="search" name="q" aria-label="Search leads" placeholder="Search name, phone, address" value="' . h($q) . '">'
        . '<button class="btn btn--light" type="submit">Search</button></form></div>';

    if (!$rows) {
        $html .= '<div class="empty card"><p><strong>No leads here yet.</strong></p><p class="muted">New inspection requests from the website show up here, and are emailed to you.</p></div>';
    } else {
        $html .= '<div class="lead-list">';
        foreach ($rows as $l) {
            $digits = preg_replace('/\D/', '', $l['phone']);
            $html .= '<article class="lead-row' . ($l['status'] === 'new' ? ' is-new' : '') . '">'
                . '<a class="lead-main" href="/admin/?view=lead&id=' . (int)$l['id'] . '">'
                . '<span class="lead-name">' . h($l['name']) . '</span>'
                . '<span class="lead-need">' . h($l['need']) . '</span>'
                . '<span class="lead-addr">' . h($l['address']) . '</span>'
                . '<span class="lead-meta">' . h(ago((int)$l['created_at'])) . ' · ' . email_badge($l) . '</span>'
                . '</a>'
                . '<div class="lead-side">' . status_pill($l['status'])
                . '<a class="btn btn--light btn--sm" href="tel:+1' . h(substr($digits, -10)) . '">' . icon('phone') . h($l['phone']) . '</a></div>'
                . '</article>';
        }
        $html .= '</div>';
        $pages = (int)ceil($total / $per);
        if ($pages > 1) {
            $html .= '<nav class="pager" aria-label="Pages">';
            for ($i = 1; $i <= $pages; $i++) {
                $cur = $i === $pageNo ? ' aria-current="page"' : '';
                $html .= '<a href="/admin/?view=leads&status=' . h($status) . '&q=' . h(urlencode($q)) . '&p=' . $i . '"' . $cur . '>' . $i . '</a>';
            }
            $html .= '</nav>';
        }
    }
    page('Leads', $html, 'leads');
}

function view_lead(int $id): never
{
    $l = lead($id);
    if (!$l) {
        flash('That lead was not found.', 'err');
        go();
    }
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        check_csrf();
        $action = post('action', 20);
        if ($action === 'save') {
            $status = post('status', 20);
            if (!isset(LEAD_STATUSES[$status])) $status = $l['status'];
            db()->prepare('UPDATE leads SET status = ?, notes = ?, updated_at = ? WHERE id = ?')
                ->execute([$status, post('notes', 5000), time(), $id]);
            flash('Lead saved.');
        } elseif ($action === 'resend') {
            $err = email_lead($l);
            record_email_result($id, $err);
            flash($err === '' ? 'Lead email sent again.' : 'Email failed: ' . $err, $err === '' ? 'ok' : 'err');
        } elseif ($action === 'delete') {
            db()->prepare('DELETE FROM leads WHERE id = ?')->execute([$id]);
            flash('Lead deleted.');
            go();
        }
        go('view=lead&id=' . $id);
    }
    // opening a new lead marks it as seen? Keep "new" until Tom changes it — clearer for follow-up.
    $digits = substr(preg_replace('/\D/', '', $l['phone']), -10);
    $opts = '';
    foreach (LEAD_STATUSES as $k => $label) {
        $opts .= '<option value="' . $k . '"' . ($k === $l['status'] ? ' selected' : '') . '>' . $label . '</option>';
    }
    $html = '<p><a class="back" href="/admin/">' . icon('back') . 'All leads</a></p>'
        . '<div class="page-head"><h1>' . h($l['name']) . '</h1>' . status_pill($l['status']) . '</div>'
        . '<div class="quick">'
        . '<a class="btn" href="tel:+1' . h($digits) . '">' . icon('phone') . 'Call</a>'
        . '<a class="btn btn--navy" href="sms:+1' . h($digits) . '">' . icon('message') . 'Text</a>'
        . '<a class="btn btn--light" href="https://www.google.com/maps/search/?api=1&amp;query=' . h(rawurlencode($l['address'])) . '" target="_blank" rel="noopener">' . icon('map') . 'Map</a>'
        . '</div>'
        . '<div class="grid2"><section class="card"><h2>Request</h2><dl class="dl">'
        . '<dt>Phone</dt><dd>' . h($l['phone']) . '</dd>'
        . '<dt>Address</dt><dd>' . h($l['address']) . '</dd>'
        . '<dt>Needs</dt><dd>' . h($l['need']) . '</dd>'
        . '<dt>Received</dt><dd>' . h(fmt_date((int)$l['created_at'])) . ' <span class="muted">(' . h(ago((int)$l['created_at'])) . ')</span></dd>'
        . '<dt>Sent from page</dt><dd><a href="' . h($l['source_page']) . '" target="_blank" rel="noopener">' . h($l['source_page']) . '</a></dd>'
        . '<dt>Email</dt><dd>' . email_badge($l) . ($l['email_status'] === 'failed' ? '<br><small class="muted">' . h($l['email_error']) . '</small>' : '') . '</dd>'
        . '</dl>'
        . '<form method="post" class="inline">' . csrf_field() . '<input type="hidden" name="action" value="resend"><button class="btn btn--light btn--sm" type="submit">' . icon('mail') . 'Email this lead again</button></form>'
        . '</section>'
        . '<section class="card"><h2>Follow-up</h2><form method="post">' . csrf_field() . '<input type="hidden" name="action" value="save">'
        . '<label>Status<select name="status">' . $opts . '</select></label>'
        . '<label>Notes <small>(only you see these)</small><textarea name="notes" rows="7" placeholder="Called Tuesday, inspection set for Thursday 10am...">' . h($l['notes']) . '</textarea></label>'
        . '<button class="btn" type="submit">Save</button></form></section></div>'
        . '<form method="post" class="danger-zone" data-confirm="Delete this lead for good?">' . csrf_field() . '<input type="hidden" name="action" value="delete">'
        . '<button class="btn-link danger" type="submit">Delete this lead</button></form>';
    page($l['name'], $html, 'leads');
}

function export_csv(): never
{
    [$status, $q, $where, $args] = lead_filters();
    $st = db()->prepare("SELECT * FROM leads $where ORDER BY created_at DESC");
    $st->execute($args);
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="hardtland-leads-' . date('Y-m-d') . '.csv"');
    $out = fopen('php://output', 'w');
    fwrite($out, "\xEF\xBB\xBF");
    $safe = fn($v) => preg_match('/^[=+\-@\t\r]/', (string)$v) ? "'" . $v : (string)$v;
    fputcsv($out, ['ID', 'Received', 'Name', 'Phone', 'Address', 'Needs', 'Status', 'Notes', 'Page', 'Email'], ',', '"', '');
    while ($l = $st->fetch()) {
        fputcsv($out, array_map($safe, [$l['id'], date('Y-m-d H:i', (int)$l['created_at']), $l['name'], $l['phone'],
            $l['address'], $l['need'], LEAD_STATUSES[$l['status']] ?? $l['status'], $l['notes'], $l['source_page'],
            $l['email_status']]), ',', '"', '');
    }
    exit;
}

// ---------------------------------------------------------------------------
// Business info
// ---------------------------------------------------------------------------
function valid_url(string $u): bool
{
    return $u === '' || (bool)preg_match('#^https://[^\s<>"]+$#i', $u);
}

function view_business(): never
{
    $site = site();
    $errors = [];
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        check_csrf();
        $new = $site;
        $new['phone'] = post('phone', 30);
        $new['email'] = post('email', 120);
        $new['street'] = one_line(post('street', 120));
        $new['city'] = one_line(post('city', 60));
        $new['state'] = strtoupper(one_line(post('state', 2)));
        $new['zip'] = one_line(post('zip', 10));
        $new['hours_note'] = one_line(post('hours_note', 160));
        $new['rating'] = post('rating', 4);
        $new['review_count'] = post('review_count', 6);
        foreach (['google_review_url', 'google_profile_url', 'facebook_url', 'yelp_url', 'notice_link'] as $k) {
            $new[$k] = post($k, 400);
        }
        $new['notice_text'] = one_line(post('notice_text', 160));
        foreach (DAY_SCHEMA as $k => $label) {
            $open = post("open_$k", 5);
            $close = post("close_$k", 5);
            if (!empty($_POST["closed_$k"]) || ($open === '' && $close === '')) {
                $new['hours'][$k] = null;
            } elseif (!preg_match('/^\d{2}:\d{2}$/', $open) || !preg_match('/^\d{2}:\d{2}$/', $close)) {
                $errors[] = "$label: enter both an opening and a closing time, or tick Closed.";
            } elseif ($close <= $open) {
                $errors[] = "$label: closing time must be after opening time.";
            } else {
                $new['hours'][$k] = ['open' => $open, 'close' => $close];
            }
        }
        if (strlen(phone_parts($new['phone'])['e164']) !== 12) $errors[] = 'Phone: enter a 10-digit phone number.';
        else $new['phone'] = phone_parts($new['phone'])['display'];
        if (!filter_var($new['email'], FILTER_VALIDATE_EMAIL)) $errors[] = 'Public email: enter a valid email address.';
        if ($new['street'] === '' || $new['city'] === '' || !preg_match('/^[A-Z]{2}$/', $new['state']) || !preg_match('/^\d{5}(-\d{4})?$/', $new['zip'])) {
            $errors[] = 'Address: fill in street, city, 2-letter state and ZIP.';
        }
        if (!preg_match('/^[1-5](\.\d)?$/', $new['rating'])) $errors[] = 'Google rating: a number like 4.7 (1 to 5).';
        if (!preg_match('/^\d{1,5}$/', $new['review_count'])) $errors[] = 'Review count: a whole number.';
        foreach (['google_review_url' => 'Google review link', 'google_profile_url' => 'Google profile link',
                  'facebook_url' => 'Facebook link', 'yelp_url' => 'Yelp link'] as $k => $label) {
            if (!valid_url($new[$k])) $errors[] = "$label must start with https://";
        }
        if ($new['google_review_url'] === '') $errors[] = 'Google review link is required (it is used for the review buttons).';
        if ($new['notice_link'] !== '' && !valid_url($new['notice_link']) && !preg_match('#^/[a-z0-9\-/]*$#', $new['notice_link'])) {
            $errors[] = 'Notice link must be a page on this site (like /storm-hail-damage/) or start with https://';
        }

        if (!$errors) {
            try {
                $result = publish_site($site, $new);
                write_json('site.json', $new);
                if ($result['errors']) {
                    flash('Saved, but ' . count($result['errors']) . ' page(s) could not be updated (read-only files): '
                        . implode(', ', array_slice($result['errors'], 0, 5)), 'err');
                } else {
                    flash('Saved. ' . $result['changed'] . ' of ' . $result['total'] . ' pages were updated on the live site.');
                }
                go('view=business');
            } catch (Throwable $e) {
                $errors[] = $e->getMessage();
            }
        }
        $site = $new;
    }

    $f = fn(string $k) => h((string)$site[$k]);
    $hoursRows = '';
    foreach (DAYS as $k => $label) {
        $v = day_open($site, $k);
        $hoursRows .= '<tr><th scope="row">' . DAY_SCHEMA[$k] . '</th>'
            . '<td><label class="sr" for="open_' . $k . '">' . $label . ' opens</label><input id="open_' . $k . '" type="time" name="open_' . $k . '" value="' . h($v['open'] ?? '') . '" step="900"></td>'
            . '<td><label class="sr" for="close_' . $k . '">' . $label . ' closes</label><input id="close_' . $k . '" type="time" name="close_' . $k . '" value="' . h($v['close'] ?? '') . '" step="900"></td>'
            . '<td><label class="check"><input type="checkbox" name="closed_' . $k . '" value="1"' . ($v ? '' : ' checked') . '> Closed</label></td></tr>';
    }
    $preview = hours_are_set($site)
        ? implode(' · ', array_map(fn($g) => h($g[0] . ' ' . $g[1]), hours_groups($site)))
        : '<em>No hours set yet. The site shows the note below instead.</em>';

    $checks = '';
    foreach (system_checks() as [$label, $ok]) {
        $checks .= '<li class="' . ($ok ? 'ok' : 'bad') . '">' . ($ok ? '✓ ' : '✗ ') . h($label) . '</li>';
    }

    $html = '<div class="page-head"><h1>Business info</h1></div>'
        . '<p class="muted lead">Changes here update every page of the website when you press Save.</p>'
        . ($errors ? '<div class="flash flash--err" role="alert"><strong>Please fix:</strong><ul><li>' . implode('</li><li>', array_map('h', $errors)) . '</li></ul></div>' : '')
        . '<form method="post" class="stack">' . csrf_field()

        . '<section class="card"><h2>Business hours</h2><p class="muted">Shown in the footer of every page, on the Contact page, and to Google. Should match your Google Business Profile exactly.</p>'
        . '<p class="hours-preview"><strong>Shows as:</strong> ' . $preview . '</p>'
        . '<div class="table-wrap"><table class="hours-table"><thead><tr><th>Day</th><th>Opens</th><th>Closes</th><th></th></tr></thead><tbody>' . $hoursRows . '</tbody></table></div>'
        . '<label>Hours note <small>(optional, e.g. "Storm damage? Call or text anytime.")</small><input name="hours_note" maxlength="160" value="' . $f('hours_note') . '"></label>'
        . '</section>'

        . '<section class="card"><h2>Contact details</h2><div class="cols">'
        . '<label>Phone (call or text)<input name="phone" type="tel" required value="' . $f('phone') . '"></label>'
        . '<label>Public email<input name="email" type="email" required value="' . $f('email') . '"></label>'
        . '</div><div class="cols cols--addr">'
        . '<label>Street<input name="street" required value="' . $f('street') . '"></label>'
        . '<label>City<input name="city" required value="' . $f('city') . '"></label>'
        . '<label>State<input name="state" required maxlength="2" value="' . $f('state') . '"></label>'
        . '<label>ZIP<input name="zip" required inputmode="numeric" value="' . $f('zip') . '"></label>'
        . '</div></section>'

        . '<section class="card"><h2>Google reviews</h2><p class="muted">Update these when your Google rating or review count changes. Shown on the homepage, review sections and to Google.</p><div class="cols">'
        . '<label>Rating<input name="rating" inputmode="decimal" required value="' . $f('rating') . '"></label>'
        . '<label>Number of reviews<input name="review_count" inputmode="numeric" required value="' . $f('review_count') . '"></label>'
        . '</div><label>Google review link <small>(the "write a review" link from your Google Business Profile)</small><input name="google_review_url" type="url" required value="' . $f('google_review_url') . '"></label>'
        . '</section>'

        . '<section class="card"><h2>Profile links</h2><p class="muted">Used by Google to connect your website with your listings. Leave blank if you don\'t have one.</p>'
        . '<label>Google Business Profile<input name="google_profile_url" type="url" placeholder="https://..." value="' . $f('google_profile_url') . '"></label>'
        . '<label>Facebook page<input name="facebook_url" type="url" placeholder="https://www.facebook.com/..." value="' . $f('facebook_url') . '"></label>'
        . '<label>Yelp page<input name="yelp_url" type="url" placeholder="https://www.yelp.com/biz/..." value="' . $f('yelp_url') . '"></label>'
        . '</section>'

        . '<section class="card"><h2>Notice bar <small class="muted">(optional)</small></h2><p class="muted">A short message across the top of every page, like after a big storm or for a seasonal offer. Leave blank to hide it.</p>'
        . '<label>Message<input name="notice_text" maxlength="160" placeholder="Hail in Verona this week? Free storm inspections. Call or text Tom." value="' . $f('notice_text') . '"></label>'
        . '<label>Link <small>(optional, e.g. /storm-hail-damage/)</small><input name="notice_link" value="' . $f('notice_link') . '"></label>'
        . '</section>'

        . '<div class="savebar"><button class="btn btn--big" type="submit">Save and update website</button></div>'
        . '</form>'
        . '<section class="card"><h2>System check</h2><ul class="checks">' . $checks . '</ul></section>';
    page('Business info', $html, 'business');
}

// ---------------------------------------------------------------------------
// Email settings
// ---------------------------------------------------------------------------
function view_email(): never
{
    $cfg = settings();
    $m = $cfg['mail'];
    $errors = [];
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        check_csrf();
        $m['to'] = post('to', 400);
        $m['from_name'] = one_line(post('from_name', 80));
        $m['from_email'] = post('from_email', 120);
        $m['method'] = post('method', 10) === 'smtp' ? 'smtp' : 'mail';
        $m['smtp_host'] = post('smtp_host', 120);
        $m['smtp_port'] = (int)post('smtp_port', 5) ?: 587;
        $m['smtp_secure'] = in_array(post('smtp_secure', 4), ['tls', 'ssl', 'none'], true) ? post('smtp_secure', 4) : 'tls';
        $m['smtp_user'] = post('smtp_user', 120);
        if (($_POST['smtp_pass'] ?? '') !== '') $m['smtp_pass'] = (string)$_POST['smtp_pass'];
        if (!empty($_POST['clear_pass'])) $m['smtp_pass'] = '';

        if (!parse_recipients($m['to'])) $errors[] = 'Add at least one valid email under "Send leads to".';
        if ($m['from_email'] !== '' && !filter_var($m['from_email'], FILTER_VALIDATE_EMAIL)) $errors[] = '"From" email is not valid.';
        if ($m['method'] === 'smtp' && !preg_match('/^[a-z0-9.\-]+$/i', $m['smtp_host'])) $errors[] = 'Enter the SMTP server name (like smtp.gmail.com).';

        if (!$errors) {
            $cfg['mail'] = $m;
            save_settings($cfg);
            if (post('action', 10) === 'test') {
                $err = send_mail('Test email from your Hardtland website',
                    "This is a test from the Hardtland website admin.\n\nIf you're reading this, new inspection requests will reach you here.\n\nSent " . date('M j, Y g:i A') . "\n", $m);
                flash($err === '' ? 'Settings saved and a test email was sent to ' . implode(', ', parse_recipients($m['to'])) . '. Check the inbox (and spam folder).' : 'Settings saved, but the test email failed: ' . $err, $err === '' ? 'ok' : 'err');
            } else {
                flash('Email settings saved.');
            }
            go('view=email');
        }
    }
    $sel = fn($a, $b) => $a === $b ? ' selected' : '';
    $html = '<div class="page-head"><h1>Email</h1></div>'
        . '<p class="muted lead">Every inspection request is saved under Leads first, then emailed to the addresses below.</p>'
        . ($errors ? '<div class="flash flash--err" role="alert">' . implode('<br>', array_map('h', $errors)) . '</div>' : '')
        . '<form method="post" class="stack">' . csrf_field()
        . '<section class="card"><h2>Who gets lead emails</h2>'
        . '<label>Send leads to <small>(separate more than one with commas)</small><input name="to" required value="' . h($m['to']) . '"></label>'
        . '<div class="cols"><label>"From" name<input name="from_name" value="' . h($m['from_name']) . '"></label>'
        . '<label>"From" email <small>(should be on your website\'s domain)</small><input name="from_email" type="email" placeholder="' . h(default_from_email()) . '" value="' . h($m['from_email']) . '"></label></div>'
        . '</section>'
        . '<section class="card"><h2>How the website sends email</h2>'
        . '<label>Sending method<select name="method" data-toggle-smtp>'
        . '<option value="mail"' . $sel($m['method'], 'mail') . '>Web host\'s built-in mail (simplest)</option>'
        . '<option value="smtp"' . $sel($m['method'], 'smtp') . '>SMTP email account (most reliable)</option></select></label>'
        . '<div class="smtp" data-smtp>'
        . '<p class="muted">Use the outgoing mail settings from your email provider or web host. For Gmail or Google Workspace, use smtp.gmail.com, port 587, TLS, and an App Password.</p>'
        . '<div class="cols"><label>SMTP server<input name="smtp_host" placeholder="smtp.example.com" value="' . h($m['smtp_host']) . '"></label>'
        . '<label>Port<input name="smtp_port" inputmode="numeric" value="' . h((string)$m['smtp_port']) . '"></label></div>'
        . '<label>Security<select name="smtp_secure"><option value="tls"' . $sel($m['smtp_secure'], 'tls') . '>TLS / STARTTLS (port 587)</option>'
        . '<option value="ssl"' . $sel($m['smtp_secure'], 'ssl') . '>SSL (port 465)</option><option value="none"' . $sel($m['smtp_secure'], 'none') . '>None</option></select></label>'
        . '<div class="cols"><label>Username<input name="smtp_user" autocomplete="off" value="' . h($m['smtp_user']) . '"></label>'
        . '<label>Password <small>' . ($m['smtp_pass'] !== '' ? '(saved, leave blank to keep)' : '') . '</small><input name="smtp_pass" type="password" autocomplete="new-password"></label></div>'
        . ($m['smtp_pass'] !== '' ? '<label class="check"><input type="checkbox" name="clear_pass" value="1"> Remove saved password</label>' : '')
        . '</div></section>'
        . '<div class="savebar"><button class="btn" type="submit" name="action" value="save">Save</button>'
        . '<button class="btn btn--light" type="submit" name="action" value="test">' . icon('mail') . 'Save and send test email</button></div>'
        . '</form>';
    page('Email', $html, 'email');
}

// ---------------------------------------------------------------------------
// Account
// ---------------------------------------------------------------------------
function view_account(): never
{
    $cfg = settings();
    $errors = [];
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        check_csrf();
        $user = post('username', 40);
        $pass = (string)($_POST['password'] ?? '');
        if (!password_verify((string)($_POST['current'] ?? ''), $cfg['admin_hash'])) $errors[] = 'Your current password is not right.';
        if (!preg_match('/^[A-Za-z0-9._@-]{3,40}$/', $user)) $errors[] = 'Username: 3 to 40 letters, numbers or . _ @ -';
        if ($pass !== '' && mb_strlen($pass) < 10) $errors[] = 'New password must be at least 10 characters.';
        if ($pass !== ($_POST['password2'] ?? '')) $errors[] = 'The two new passwords do not match.';
        if (!$errors) {
            $cfg['admin_user'] = $user;
            if ($pass !== '') $cfg['admin_hash'] = password_hash($pass, PASSWORD_DEFAULT);
            save_settings($cfg);
            session_regenerate_id(true);
            flash('Account updated.');
            go('view=account');
        }
    }
    $html = '<div class="page-head"><h1>Account</h1></div>'
        . ($errors ? '<div class="flash flash--err" role="alert">' . implode('<br>', array_map('h', $errors)) . '</div>' : '')
        . '<form method="post" class="card narrow">' . csrf_field()
        . '<label>Username<input name="username" required autocomplete="username" value="' . h($cfg['admin_user']) . '"></label>'
        . '<label>New password <small>(leave blank to keep the current one)</small><input name="password" type="password" minlength="10" autocomplete="new-password"></label>'
        . '<label>Confirm new password<input name="password2" type="password" minlength="10" autocomplete="new-password"></label>'
        . '<label>Current password <small>(required to save)</small><input name="current" type="password" required autocomplete="current-password"></label>'
        . '<button class="btn" type="submit">Save</button></form>';
    page('Account', $html, 'account');
}
