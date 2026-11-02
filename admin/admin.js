/* Hardtland admin: confirm dangerous actions, show SMTP fields only when needed. */
document.addEventListener('submit', function (e) {
  var msg = e.target.getAttribute('data-confirm');
  if (msg && !window.confirm(msg)) e.preventDefault();
});
(function () {
  var sel = document.querySelector('[data-toggle-smtp]');
  var box = document.querySelector('[data-smtp]');
  if (!sel || !box) return;
  function sync() { box.hidden = sel.value !== 'smtp'; }
  sel.addEventListener('change', sync);
  sync();
})();
