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
  // Gallery filter (gallery page only). Without JS every photo shows.
  var filterBtns = document.querySelectorAll('.filter-btn');
  var grid = document.getElementById('gallery-grid');
  var status = document.getElementById('gallery-status');
  if (filterBtns.length && grid) {
    filterBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var f = btn.getAttribute('data-filter');
        var shown = 0;
        filterBtns.forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
        grid.querySelectorAll('li[data-cat]').forEach(function (li) {
          var match = f === 'all' || li.getAttribute('data-cat') === f;
          li.hidden = !match;
          if (match) shown++;
        });
        if (status) status.textContent = 'Showing ' + shown + ' projects';
      });
    });
  }
  // Free inspection forms: send without leaving the page. Without JS (or if
  // fetch fails to load) the form posts normally and lands on /thank-you/.
  document.querySelectorAll('form[data-lead-form]').forEach(function (form) {
    var ts = form.querySelector('input[name="ts"]');
    if (ts) ts.value = String(Date.now());
    if (!window.fetch || !window.FormData) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      var status = form.querySelector('.form-status');
      var label = btn.textContent;
      btn.disabled = true;
      btn.textContent = 'Sending...';
      if (status) { status.textContent = ''; status.classList.remove('is-error'); }

      function fail(msg) {
        btn.disabled = false;
        btn.textContent = label;
        if (status) { status.textContent = msg; status.classList.add('is-error'); }
      }

      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'X-Requested-With': 'fetch' } })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (!d || !d.ok) return fail((d && d.error) || 'Sorry, something went wrong. Please call or text us.');
          var done = document.createElement('div');
          done.className = 'form-done';
          done.setAttribute('role', 'status');
          done.setAttribute('tabindex', '-1');
          var h = document.createElement('p');
          h.className = 'form-done__title';
          h.textContent = 'Thanks' + (d.name ? ', ' + d.name.split(' ')[0] : '') + '! We got your request.';
          var p = document.createElement('p');
          p.textContent = 'Tom or the crew will call you back within 1 business day.';
          done.appendChild(h);
          done.appendChild(p);
          form.replaceWith(done);
          done.focus();
          if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { form_page: location.pathname });
        })
        .catch(function () {
          fail('We could not send your request. Please check your connection, or call or text us.');
        });
    });
  });
})();
