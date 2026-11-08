/* Optional execution explorer. Text from Python is always rendered as text. */
(function () {
  const scriptURL = document.currentScript.src;
  function setup() {
    document.querySelectorAll('.python-visualizer').forEach(function (root) {
      if (root.dataset.ready) return;
      root.dataset.ready = '1';
      const editor = root.querySelector('textarea');
      const original = editor.value;
      const controls = root.querySelector('.trace-controls');
      const status = root.querySelector('.trace-status');
      const view = root.querySelector('.trace-view');
      let worker, timer, steps = [], position = 0, error = null, source = '';
      function node(tag, text, parent) {
        const el = document.createElement(tag);
        if (text !== undefined) el.textContent = text;
        if (parent) parent.appendChild(el);
        return el;
      }
      function button(label, action) {
        const el = node('button', label, controls);
        el.type = 'button'; el.addEventListener('click', action); return el;
      }
      function stopWorker() {
        clearTimeout(timer);
        if (worker) worker.terminate();
        worker = null; stop.disabled = true; run.disabled = false;
      }
      function invalidate(message) {
        stopWorker(); steps = []; view.hidden = true;
        back.disabled = next.disabled = restart.disabled = true;
        status.textContent = message;
      }
      function render() {
        const step = steps[position];
        view.replaceChildren(); view.hidden = false;
        const final = step.done;
        status.textContent = final ? (error ? 'Execution stopped: ' + error : 'Program finished.') :
          'Step ' + (position + 1) + ' of ' + steps.length + ': line ' + step.line + ' runs next.';
        node('h4', final ? 'Code — execution ended' : 'Code — highlighted line runs next', view);
        const code = node('pre', undefined, view);
        code.tabIndex = 0;
        code.setAttribute('aria-label', 'Execution trace code; use arrow keys to scroll');
        source.split('\n').forEach(function (line, i) {
          const row = node('span', (i + 1) + '  ' + line + '\n', code);
          if (step.line === i + 1) { row.className = 'trace-current'; row.setAttribute('aria-current', 'step'); }
        });
        node('h4', 'Variables at this moment', view);
        const values = Object.entries(step.values);
        if (!values.length) node('p', 'No variables created yet.', view);
        else {
          const table = node('table', undefined, view);
          const header = node('tr', undefined, node('thead', undefined, table));
          node('th', 'Name', header).scope = 'col'; node('th', 'Value', header).scope = 'col';
          const body = node('tbody', undefined, table);
          values.forEach(([name, value]) => { const row = node('tr', undefined, body); node('td', name, row); node('td', value, row); });
        }
        node('h4', 'Output so far', view);
        const output = node('pre', step.output || '(No output yet.)', view);
        output.tabIndex = 0;
        output.setAttribute('aria-label', 'Output so far; use arrow keys to scroll');
        if (final && error) node('pre', error, view).className = 'trace-error';
        back.disabled = position === 0; next.disabled = position === steps.length - 1;
        restart.disabled = false;
      }
      const run = button('Run and visualize', function () {
        invalidate('Loading Python. The first run may take a moment…');
        source = editor.value;
        if (source.length > 6000) { status.textContent = 'Please keep this explorer example under 6,000 characters.'; return; }
        run.disabled = true; stop.disabled = false;
        try {
          worker = new Worker(new URL('trace-worker.js', scriptURL), { type: 'module' });
          timer = setTimeout(() => invalidate('Python could not load in time. Check your connection and try again, or use Binder or Colab.'), 60000);
          worker.onmessage = function ({ data }) {
            if (data.type === 'ready') {
              clearTimeout(timer);
              status.textContent = 'Running your code…';
              timer = setTimeout(() => invalidate('Execution stopped after 5 seconds. Try a smaller loop.'), 5000);
            } else if (data.type === 'result') {
              stopWorker(); steps = data.result.steps; error = data.result.error; position = 0; render();
            } else if (data.type === 'error') invalidate('Unable to run Python: ' + data.error);
          };
          worker.onerror = function () { invalidate('Python could not load. Check your connection and try again, or use Binder or Colab.'); };
          worker.postMessage({ source });
        } catch (e) { invalidate('This browser could not start Python. Use Binder or Colab to try the example.'); }
      });
      const stop = button('Stop', () => invalidate('Stopped. Edit your code or run again.'));
      const back = button('Previous step', () => { position--; render(); });
      const next = button('Next step', () => { position++; render(); });
      const restart = button('Restart steps', () => { position = 0; render(); });
      button('Restore example', () => { editor.value = original; invalidate('Original example restored. Predict, then run.'); });
      stop.disabled = back.disabled = next.disabled = restart.disabled = true;
      editor.addEventListener('input', () => invalidate('Code changed. Run and visualize again to update the steps.'));
      window.addEventListener('pagehide', stopWorker);
    });
  }
  if (window.document$ && window.document$.subscribe) window.document$.subscribe(setup);
  else if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup);
  else setup();
})();
