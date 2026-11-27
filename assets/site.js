/* 1848 Blooms & Designs, v2 behaviour. No dependencies. */
(function () {
  'use strict';

  /* ---- Form delivery ------------------------------------------------------
     Set FORM_ENDPOINT to a form service URL (for example a Formspree endpoint
     like "https://formspree.io/f/xxxxxxx") and both forms will send their
     answers there as JSON. While it is empty, the forms run in preview mode:
     nothing is sent, and a notice tells the visitor so. */
  var FORM_ENDPOINT = '';

  var doc = document, body = doc.body;
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };

  /* ---- Header ---- */
  var header = $('.hd');
  function onHeader() { if (header) header.classList.toggle('is-scrolled', window.scrollY > 30); }

  /* ---- Full-screen menu ---- */
  var btn = $('.menu-btn'), mnav = $('.mnav');
  function setMenu(open) {
    body.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    $('span', btn).textContent = open ? 'Close' : 'Menu';
    if (open) { mnav.querySelector('a').focus({ preventScroll: true }); }
  }
  window.addEventListener('resize', function () { if (window.innerWidth > 900 && body.classList.contains('menu-open')) setMenu(false); });
  if (btn && mnav) {
    btn.addEventListener('click', function () { setMenu(!body.classList.contains('menu-open')); });
    $$('a', mnav).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && body.classList.contains('menu-open')) { setMenu(false); btn.focus(); }
    });
  }

  /* ---- Scroll-filled titles: letters fade in as the title crosses the screen ---- */
  var titles = $$('.rv');
  titles.forEach(function (el) {
    var text = el.textContent.replace(/\s+/g, ' ').trim();
    el.setAttribute('aria-label', text);
    el.textContent = '';
    text.split(' ').forEach(function (word, i, arr) {
      var w = doc.createElement('span');
      w.className = 'w'; w.setAttribute('aria-hidden', 'true');
      word.split('').forEach(function (c) {
        var s = doc.createElement('span'); s.className = 'ch'; s.textContent = c; w.appendChild(s);
      });
      el.appendChild(w);
      if (i < arr.length - 1) el.appendChild(doc.createTextNode(' '));
    });
    el._chars = $$('.ch', el);
  });
  function paintTitles() {
    var vh = window.innerHeight;
    titles.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var p = reduce ? 1 : clamp((vh * 0.92 - r.top) / (vh * 0.5), 0, 1);
      var n = el._chars.length, k = p * (n + 10);
      el._chars.forEach(function (c, i) { c.style.opacity = (0.14 + 0.86 * clamp((k - i) / 10, 0, 1)).toFixed(3); });
    });
  }

  /* ---- Fan of photo prints ---- */
  var fans = $$('.fan');
  function paintFans() {
    var vh = window.innerHeight;
    fans.forEach(function (f) {
      var r = f.getBoundingClientRect();
      var p = reduce ? 1 : clamp((vh * 0.95 - r.top) / (vh * 0.55), 0, 1);
      f.style.setProperty('--p', (0.08 + 0.92 * p).toFixed(3));
    });
  }

  var ticking = false;
  function onScroll() {
    onHeader();
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { paintTitles(); paintFans(); ticking = false; });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onHeader(); paintTitles(); paintFans();

  /* ---- Photo rail: previous / next ---- */
  $$('[data-rail]').forEach(function (rail) {
    var wrap = rail.parentNode;
    var step = function (d) { var f = $('figure', rail); rail.scrollBy({ left: d * (f.getBoundingClientRect().width + 20), behavior: reduce ? 'auto' : 'smooth' }); };
    var pv = $('[data-prev]', wrap), nx = $('[data-next]', wrap);
    if (pv) pv.addEventListener('click', function () { step(-1); });
    if (nx) nx.addEventListener('click', function () { step(1); });
  });


  /* ---- ?debug overlay: shows which font the headings actually use ---- */
  if (/[?&]debug/.test(location.search)) {
    var h = $('h1') || $('h2'), cs = h && getComputedStyle(h);
    var box = doc.createElement('pre');
    box.style.cssText = 'position:fixed;z-index:999;left:8px;bottom:8px;right:8px;background:#fff;color:#000;font:12px/1.4 monospace;padding:10px;border:2px solid red;white-space:pre-wrap';
    var fs = []; doc.fonts.forEach(function (f) { fs.push(f.family + ' ' + f.weight + ' ' + f.style + ' ' + f.status); });
    box.textContent = 'h1 family: ' + (cs && cs.fontFamily) + '\nh1 weight: ' + (cs && cs.fontWeight) + '\nh1 size: ' + (cs && cs.fontSize) + '\nurl: ' + location.href + '\nfonts: ' + fs.join(' | ') + '\ncss rules: ' + (doc.styleSheets.length) + ' sheet(s)';
    body.appendChild(box);
    doc.fonts.ready.then(function () { var f2 = []; doc.fonts.forEach(function (f) { f2.push(f.family + ' ' + f.weight + ' ' + f.status); }); box.textContent = box.textContent.replace(/fonts: .*/, 'fonts: ' + f2.join(' | ')); });
  }

  /* ---- Year ---- */
  $$('[data-year]').forEach(function (n) { n.textContent = new Date().getFullYear(); });

  /* ---- Portfolio filters + lightbox ---- */
  var gallery = $('.gallery');
  if (gallery) {
    var shots = $$('.shot', gallery);
    var fbtns = $$('.filters button');
    fbtns.forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-filter');
        fbtns.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        shots.forEach(function (s) {
          s.hidden = !(f === 'all' || (s.getAttribute('data-cat') || '').split(' ').indexOf(f) > -1);
        });
        if (history.replaceState) history.replaceState(null, '', f === 'all' ? location.pathname : '#' + f);
      });
    });
    var hash = location.hash.replace('#', '');
    var start = fbtns.filter(function (b) { return b.getAttribute('data-filter') === hash; })[0];
    if (start) start.click();

    var lb = $('#lightbox');
    var lbImg = $('img', lb), lbCap = $('.lb__cap', lb);
    var idx = 0;
    var visible = function () { return shots.filter(function (s) { return !s.hidden; }); };
    var show = function (i) {
      var list = visible();
      if (!list.length) return;
      idx = (i + list.length) % list.length;
      var im = $('img', list[idx]);
      lbImg.src = im.getAttribute('data-full') || im.src;
      lbImg.alt = im.alt;
      lbCap.textContent = im.alt;
    };
    shots.forEach(function (s) {
      s.addEventListener('click', function () {
        show(visible().indexOf(s));
        if (typeof lb.showModal === 'function') lb.showModal(); else lb.setAttribute('open', '');
      });
    });
    $('.pv', lb).addEventListener('click', function () { show(idx - 1); });
    $('.nx', lb).addEventListener('click', function () { show(idx + 1); });
    $('.x', lb).addEventListener('click', function () { lb.close(); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lb__in')) lb.close(); });
    lb.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  /* ---- Forms ---- */
  var form = $('form[data-form]');
  if (form) {
    var type = form.getAttribute('data-form'); // inquiry | reservation
    var notice = $('.notice', form);

    var qs = new URLSearchParams(location.search);
    var pre = qs.get('experience');
    if (pre) {
      var radio = $('input[name="experience"][value="' + pre + '"]', form);
      if (radio) radio.checked = true;
    }
    /* contact.html?type=wedding (or any option text) preselects "What are you planning?" */
    var preType = (qs.get('type') || '').toLowerCase();
    var kind = $('select[name="event_type"]', form);
    if (preType && kind) {
      $$('option', kind).forEach(function (o) { if (o.value && o.value.toLowerCase().indexOf(preType) === 0) kind.value = o.value; });
    }

    var validate = function () {
      var ok = true, first = null;
      $$('.field', form).forEach(function (f) {
        var inp = $('input,select,textarea', f);
        if (!inp || !inp.required) return;
        var bad;
        if (inp.type === 'radio') {
          bad = !$$('input[name="' + inp.name + '"]', f).some(function (r) { return r.checked; });
        } else {
          bad = !inp.value.trim() || (inp.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(inp.value));
        }
        f.classList.toggle('invalid', bad);
        if (bad) { ok = false; if (!first) first = inp; }
      });
      if (first) first.focus();
      return ok;
    };

    var go = function () {
      var name = (form.elements.name && form.elements.name.value || '').trim().split(' ')[0];
      var p = new URLSearchParams({ type: type });
      if (name) p.set('name', name);
      location.href = 'thank-you.html?' + p.toString();
    };

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.elements.website && form.elements.website.value) return; // honeypot
      if (!validate()) return;

      if (FORM_ENDPOINT) {
        var data = {};
        new FormData(form).forEach(function (v, k) { data[k] = v; });
        delete data.website;
        var b = $('button[type=submit]', form);
        b.disabled = true; b.textContent = 'Sending';
        fetch(FORM_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
          .then(function (r) { if (!r.ok) throw new Error(); go(); })
          .catch(function () {
            b.disabled = false; b.textContent = type === 'reservation' ? 'Reserve my spot' : 'Send inquiry';
            notice.textContent = 'Your message did not send. Check your connection and try again, or email us directly.';
            notice.classList.add('on');
          });
      } else {
        notice.innerHTML = 'Preview mode: this form is not connected to email yet, so nothing was sent. ';
        var c = doc.createElement('a');
        c.href = '#'; c.className = 'link'; c.textContent = 'Continue to the thank-you page';
        c.addEventListener('click', function (ev) { ev.preventDefault(); go(); });
        notice.appendChild(c);
        notice.classList.add('on');
        notice.scrollIntoView({ block: 'center', behavior: reduce ? 'auto' : 'smooth' });
      }
    });

    $$('input,select,textarea', form).forEach(function (i) {
      i.addEventListener('input', function () { var f = i.closest('.field'); if (f) f.classList.remove('invalid'); });
    });
  }

  /* ---- Thank-you page ---- */
  var ty = $('[data-thanks]');
  if (ty) {
    var q = new URLSearchParams(location.search);
    var nm = q.get('name');
    var t = q.get('type') === 'reservation' ? 'reservation' : 'inquiry';
    var h = $('[data-ty-title]', ty);
    h.textContent = nm ? 'Thank you, ' + nm : 'Thank you';
    $$('[data-ty]', ty).forEach(function (n) { n.hidden = n.getAttribute('data-ty') !== t; });
  }
})();
