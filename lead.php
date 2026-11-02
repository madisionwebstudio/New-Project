<?php
/**
 * Hardtland — free inspection form handler.
 * Saves the lead, then emails it. Works with the site's fetch() submit
 * (JSON reply) and with a plain form post (redirect to /thank-you/).
 */
declare(strict_types=1);

require __DIR__ . '/inc/app.php';

$isAjax = ($_SERVER['HTTP_X_REQUESTED_WITH'] ?? '') === 'fetch';

function lead_respond(bool $ok, string $error = '', string $name = ''): void
{
    global $isAjax;
    if ($isAjax) {
        header('Content-Type: application/json; charset=utf-8');
        header('Cache-Control: no-store');
        http_response_code($ok ? 200 : 400);
        echo json_encode($ok ? ['ok' => true, 'name' => $name] : ['ok' => false, 'error' => $error]);
        exit;
    }
    if ($ok) {
        header('Location: /thank-you/', true, 303);
        exit;
    }
    http_response_code(400);
    $site = site();
    $p = phone_parts($site['phone']);
    echo '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        . '<meta name="viewport" content="width=device-width, initial-scale=1">'
        . '<meta name="robots" content="noindex"><title>Please check the form | Hardtland</title>'
        . '<link rel="stylesheet" href="/css/styles.css"></head><body>'
        . '<main class="section"><div class="container"><div class="prose">'
        . '<h1>Almost there</h1><p>' . h($error) . '</p>'
        . '<p><a class="btn btn--primary" href="javascript:history.back()">Go back to the form</a></p>'
        . '<p>Or call or text Tom at <a href="tel:' . h($p['e164']) . '">' . h($p['display']) . '</a>.</p>'
        . '</div></div></main></body></html>';
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    header('Allow: POST');
    exit('Method not allowed');
}

// ---- Spam checks (bots get a fake "success" so they don't retry) ----
if (!empty($_POST['website'])) lead_respond(true);
$ts = (int)($_POST['ts'] ?? 0);
if ($ts > 0 && (time() - intdiv($ts, 1000)) < 3) lead_respond(true);

$phoneFallback = phone_parts(site()['phone'])['display'];

try {
    $ip = ip_hash();
    if (count_attempts('lead', $ip, 60) >= 1 || count_attempts('lead', $ip, 3600) >= 6) {
        lead_respond(false, 'Thanks! We already got a request from you a moment ago. Please wait a minute before sending another.');
    }
} catch (Throwable $e) {
    error_log('Hardtland lead DB error: ' . $e->getMessage());
    lead_respond(false, "Sorry, something went wrong on our end. Please call or text $phoneFallback.");
}

// ---- Validate ----
$name = clean_text((string)($_POST['name'] ?? ''), 80);
$phone = clean_text((string)($_POST['phone'] ?? ''), 30);
$address = clean_text((string)($_POST['address'] ?? ''), 200);
$need = clean_text((string)($_POST['need'] ?? ''), 40);
$source = (string)($_POST['source_page'] ?? '/');
if (!preg_match('#^/[a-z0-9\-/.]{0,80}$#', $source)) $source = '/';

if (mb_strlen($name) < 2) lead_respond(false, 'Please enter your name.');
if (strlen(preg_replace('/\D/', '', $phone)) < 10) lead_respond(false, 'Please enter a phone number with area code.');
if (mb_strlen($address) < 5) lead_respond(false, 'Please enter the address of the home.');
if (!in_array($need, LEAD_NEEDS, true)) $need = 'Other';

// ---- Save, then email ----
try {
    $now = time();
    db()->prepare('INSERT INTO leads (created_at, updated_at, name, phone, address, need, source_page, ip_hash)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
        ->execute([$now, $now, $name, $phone, $address, $need, $source, $ip]);
    $id = (int)db()->lastInsertId();
    add_attempt('lead', $ip);
} catch (Throwable $e) {
    error_log('Hardtland lead save error: ' . $e->getMessage());
    lead_respond(false, "Sorry, your request could not be saved. Please call or text $phoneFallback.");
}

$err = email_lead(lead($id));
record_email_result($id, $err);
if ($err !== '') error_log("Hardtland lead #$id email failed: $err");

// The lead is safely saved even if the email failed, so the visitor still gets a success message.
lead_respond(true, '', $name);
