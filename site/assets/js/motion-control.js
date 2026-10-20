// Pause / resume the theme's looping GSAP animations (typewriter tagline,
// floating hero shapes). Paused state is remembered, and visitors whose OS
// asks for reduced motion start paused.
(function () {
  var KEY = 'motionPaused';

  function readPref() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function savePref(value) {
    try { localStorage.setItem(KEY, value); } catch (e) { /* storage blocked */ }
  }

  // Show the final, readable state of everything the entrance animation hides.
  // Inline styles are written directly: gsap.set() does not render while the
  // global timeline is paused, which left these elements at opacity 0.
  function showStaticContent() {
    document.querySelectorAll('[data-animation], .quick-fact-card').forEach(function (el) {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
    document.querySelectorAll('.typewriter').forEach(function (el) {
      el.textContent = el.getAttribute('data-original-text') || el.textContent;
      el.style.color = 'inherit';
    });
  }

  function updateButtons(paused) {
    document.querySelectorAll('.motion-toggle').forEach(function (btn) {
      btn.setAttribute('aria-pressed', paused ? 'true' : 'false');
      var label = paused ? btn.dataset.labelPlay : btn.dataset.labelPause;
      btn.setAttribute('aria-label', label);
      btn.setAttribute('title', label);
      var text = btn.querySelector('.motion-toggle-text');
      if (text) text.textContent = label;
      var icon = btn.querySelector('i');
      if (icon) icon.className = paused ? 'fas fa-play' : 'fas fa-pause';
    });
  }

  function pause() {
    if (window.gsap) gsap.globalTimeline.pause();
    showStaticContent();
    document.documentElement.classList.add('motion-paused');
    updateButtons(true);
  }

  function play() {
    if (window.gsap) gsap.globalTimeline.resume();
    document.documentElement.classList.remove('motion-paused');
    updateButtons(false);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var pref = readPref();
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (pref === 'true' || (pref === null && reduce)) {
      pause();
    } else {
      updateButtons(false);
    }

    document.querySelectorAll('.motion-toggle').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var paused = document.documentElement.classList.contains('motion-paused');
        if (paused) { play(); savePref('false'); } else { pause(); savePref('true'); }
      });
    });
  });
})();
