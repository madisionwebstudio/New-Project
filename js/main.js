/* Hardtland — small, dependency-free helpers for the menu. Pages work without it. */
(function () {
  var navToggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  var subToggles = document.querySelectorAll('.nav-sub-toggle');

  function closeSubs(except) {
    subToggles.forEach(function (btn) {
      if (btn === except) return;
      btn.setAttribute('aria-expanded', 'false');
      var sub = document.getElementById(btn.getAttribute('aria-controls'));
      if (sub) sub.classList.remove('is-open');
    });
  }

  function closeNav() {
    if (!navToggle || !nav) return;
    navToggle.setAttribute('aria-expanded', 'false');
    nav.classList.remove('is-open');
  }

  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var open = navToggle.getAttribute('aria-expanded') === 'true';
      navToggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
      if (open) closeSubs();
    });
  }

  subToggles.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      closeSubs(btn);
      btn.setAttribute('aria-expanded', String(!open));
      var sub = document.getElementById(btn.getAttribute('aria-controls'));
      if (sub) sub.classList.toggle('is-open', !open);
    });
  });

  // Escape closes any open menu and returns focus to its button
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var openSub = document.querySelector('.nav-sub-toggle[aria-expanded="true"]');
    if (openSub) {
      closeSubs();
      openSub.focus();
    } else if (navToggle && navToggle.getAttribute('aria-expanded') === 'true') {
      closeNav();
      navToggle.focus();
    }
  });

  // Clicking outside the header closes dropdowns
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.site-header')) {
      closeSubs();
      closeNav();
    }
  });
})();
