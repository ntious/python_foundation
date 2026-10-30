// Pinned runtime; loaded only after the learner asks to run Python.
import { loadPyodide } from 'https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.mjs';

self.onmessage = async ({ data }) => {
  try {
    const python = await loadPyodide();
    self.postMessage({ type: 'ready' });
    python.globals.set('_learner_source', data.source);
    const result = python.runPython(String.raw`
import sys, io, json, traceback

def _record_run(source):
    frames = []
    output = io.StringIO()
    namespace = {'__name__': '__main__'}
    limit = 500
    def snapshot(frame, line, done=False):
        values = {}
        for name, value in frame.items():
            if name.startswith('__'):
                continue
            if type(value) in (int, float, str, bool, list, tuple, type(None)):
                values[name] = repr(value)[:200]
        frames.append({'line': line, 'values': values, 'output': output.getvalue(), 'done': done})
    def trace(frame, event, arg):
        if frame.f_code.co_filename != '<explorer>':
            return None
        if event == 'line':
            if len(frames) >= limit or len(output.getvalue()) > 12000:
                raise RuntimeError('Explorer limit reached. Try fewer repetitions or less output.')
            snapshot(frame.f_locals, frame.f_lineno)
        return trace
    original_stdout, original_stderr = sys.stdout, sys.stderr
    error = None
    try:
        code = compile(source, '<explorer>', 'exec')
        sys.stdout = sys.stderr = output
        sys.settrace(trace)
        exec(code, namespace)
    except BaseException as exc:
        error = ''.join(traceback.format_exception_only(type(exc), exc)).strip()
    finally:
        sys.settrace(None)
        sys.stdout, sys.stderr = original_stdout, original_stderr
    snapshot(namespace, None, True)
    return json.dumps({'steps': frames, 'error': error})

_record_run(_learner_source)
`);
    self.postMessage({ type: 'result', result: JSON.parse(result) });
  } catch (error) {
    self.postMessage({ type: 'error', error: String(error.message || error) });
  }
};
