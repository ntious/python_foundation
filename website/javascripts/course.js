/* Small enhancements: the hero "run" cell and per-browser lesson progress.
   Everything works without JavaScript or storage; these only add to it. */
(function () {
  var KEY = 'pf-lessons-done';

  function readDone() {
    try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; }
  }
  function saveDone(list) {
    try { localStorage.setItem(KEY, JSON.stringify(list)); return true; } catch (e) { return false; }
  }
  function slugOf(href) {
    var match = /notebooks\/(\d\d_[^/.]+)/.exec(href || '');
    return match ? match[1] : null;
  }

  function setupCell() {
    var cell = document.querySelector('[data-cell]');
    if (!cell || cell.dataset.ready) return;
    cell.dataset.ready = '1';
    var out = cell.querySelector('[data-out]');
    var predict = cell.querySelector('[data-predict]');
    out.hidden = true;
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'cell-run';
    button.textContent = 'Run cell';
    button.addEventListener('click', function () {
      var running = out.hidden;
      out.hidden = !running;
      cell.classList.toggle('has-run', running);
      button.textContent = running ? 'Hide output' : 'Run cell';
      predict.textContent = running ? 'Did it match your guess? That is the whole method.' :
        'What will this print? Make a guess, then run it.';
    });
    predict.appendChild(document.createTextNode(' '));
    predict.after(button);
  }

  function setupLessonPage() {
    var slug = slugOf(location.pathname);
    var title = document.querySelector('.md-content h1');
    if (!slug || !title || document.querySelector('.lesson-done')) return;
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'lesson-done';
    function render() {
      var done = readDone().indexOf(slug) !== -1;
      button.setAttribute('aria-pressed', String(done));
      button.textContent = done ? 'Done ✓  (tap to undo)' : 'Mark this lesson as done';
    }
    button.addEventListener('click', function () {
      var list = readDone();
      var at = list.indexOf(slug);
      if (at === -1) list.push(slug); else list.splice(at, 1);
      if (!saveDone(list)) {
        button.textContent = 'Progress can’t be saved in this browser';
        return;
      }
      render();
    });
    render();
    title.after(button);
  }

  function setupPath() {
    var path = document.querySelector('.lesson-path');
    var meter = document.querySelector('[data-progress]');
    if (!path || !meter) return;
    var links = Array.prototype.slice.call(path.querySelectorAll('a'));
    var done = readDone();
    var count = 0;
    var next = null;
    links.forEach(function (link) {
      var item = link.closest('li');
      var finished = done.indexOf(slugOf(link.getAttribute('href'))) !== -1;
      item.classList.toggle('is-done', finished);
      if (finished) count++; else if (!next) next = link;
    });
    if (!count) { meter.hidden = true; return; }
    var total = links.length;
    meter.innerHTML = '';
    var text = document.createElement('p');
    text.className = 'progress-text';
    text.textContent = count === total ? 'You finished every lesson. Nice work.' :
      'You have finished ' + count + ' of ' + total + ' lessons.';
    var bar = document.createElement('div');
    bar.className = 'progress-bar';
    bar.setAttribute('role', 'progressbar');
    bar.setAttribute('aria-valuemin', '0');
    bar.setAttribute('aria-valuemax', String(total));
    bar.setAttribute('aria-valuenow', String(count));
    bar.setAttribute('aria-label', 'Lessons finished');
    var fill = document.createElement('span');
    fill.style.width = (100 * count / total) + '%';
    bar.appendChild(fill);
    meter.appendChild(text);
    meter.appendChild(bar);
    if (next) {
      var resume = document.createElement('a');
      resume.className = 'md-button md-button--primary progress-next';
      resume.href = next.getAttribute('href');
      resume.textContent = 'Continue with ' + next.closest('li').textContent.trim();
      meter.appendChild(resume);
    }
    var note = document.createElement('p');
    note.className = 'progress-note';
    note.textContent = 'Progress is saved in this browser only.';
    meter.appendChild(note);
    meter.hidden = false;
  }

  function init() { setupCell(); setupLessonPage(); setupPath(); }
  if (window.document$ && window.document$.subscribe) window.document$.subscribe(init);
  else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
