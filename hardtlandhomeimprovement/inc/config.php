<?php
/**
 * Hardtland site config. This folder is blocked from the web by inc/.htaccess.
 *
 * BEFORE UPLOAD: change ADMIN_SETUP_KEY to a long random phrase. You type it
 * once at /admin/ to create the admin login, then it's no longer used.
 */
declare(strict_types=1);

const ADMIN_SETUP_KEY = 'CHANGE-ME-BEFORE-UPLOAD';

const BIZ_NAME = 'Hardtland Home Improvement, Inc.';
const SITE_URL = 'https://www.hardtlandhomeimprovement.com';

// Web root (where index.html lives) and the private data folder.
// For extra safety you can move DATA_DIR outside the web root.
define('SITE_ROOT', dirname(__DIR__));
define('DATA_DIR', SITE_ROOT . '/data');

date_default_timezone_set('America/Chicago');
