"""Smoke-test JupyterLab and notebook access without printing authentication tokens."""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def check():
    with tempfile.TemporaryDirectory(prefix='python-course-jupyter-') as runtime:
        env = dict(os.environ, JUPYTER_RUNTIME_DIR=runtime)
        with tempfile.TemporaryFile() as log:
            process = subprocess.Popen(
                [sys.executable, '-m', 'jupyterlab', '--no-browser', '--ServerApp.port=0',
                 f'--ServerApp.root_dir={ROOT}'], env=env, stdout=log, stderr=log,
            )
            try:
                deadline = time.monotonic() + 45
                while time.monotonic() < deadline:
                    if process.poll() is not None:
                        raise AssertionError('JupyterLab exited before readiness')
                    files = list(Path(runtime).glob('jpserver-*.json'))
                    if files:
                        record = json.loads(files[0].read_text())
                        base = record['url'].replace('localhost', '127.0.0.1').rstrip('/')
                        headers = {'Authorization': 'token ' + record['token']}
                        for path in ('/lab', '/api/contents/notebooks/00_getting_started.ipynb'):
                            with urlopen(Request(base + path, headers=headers), timeout=10) as response:
                                assert response.status == 200
                                if '/api/' in path:
                                    notebook = json.load(response)
                                    assert notebook['type'] == 'notebook' and notebook['content']['cells']
                        print(f'PASS: local JupyterLab serves notebook 00 on Python {sys.version.split()[0]}; authentication retained.')
                        return
                    time.sleep(.2)
                raise AssertionError('JupyterLab readiness timed out')
            finally:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


if __name__ == '__main__':
    check()
