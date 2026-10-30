"""Optional real-browser regression checks; requires Playwright and Chromium."""
import functools
import http.server
import threading
import json
from playwright.sync_api import sync_playwright
from test_site_browser import Handler, ROOT


def check():
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Handler, directory=str(ROOT / '.site-build/output')))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_default_timeout(90000)
            requests = []
            page.on('request', lambda r: requests.append(r.url))
            page.goto(f'http://127.0.0.1:{server.server_port}/python_foundation/notebooks/07_loops/')
            root = page.locator('.python-visualizer')
            editor = root.get_by_label('Your Python code')
            status = root.locator('.trace-status')
            assert not any('pyodide' in r for r in requests), 'Runtime must load on demand'

            def run(source=None):
                if source is not None:
                    editor.fill(source)
                root.get_by_role('button', name='Run and visualize', exact=True).click()
                root.locator('.trace-view:not([hidden])').wait_for()

            def finish():
                next_step = root.get_by_role('button', name='Next step', exact=True)
                for _ in range(510):
                    if next_step.is_disabled():
                        return
                    next_step.click()
                raise AssertionError('Trace never ended')

            original = editor.input_value()
            cells = json.loads((ROOT / 'notebooks/07_loops.ipynb').read_text())['cells']
            assert original == next(''.join(c['source']) for c in cells if ''.join(c['source']).startswith('# Watch the loop steps appear one at a time'))
            run()
            assert 'line 2 runs next' in status.inner_text()
            root.get_by_role('button', name='Next step', exact=True).click()
            assert 'step' in root.locator('table').inner_text()
            finish()
            assert 'Program finished' in status.inner_text()
            assert 'Loop step: 3\nLoop finished' in root.locator('.trace-view').inner_text()
            root.get_by_role('button', name='Previous step', exact=True).click()
            assert 'runs next' in status.inner_text()
            root.get_by_role('button', name='Restart steps', exact=True).click()
            assert 'Step 1 of' in status.inner_text()

            run(original.replace('range(3)', 'range(5)').replace('step + 1', 'step'))
            finish()
            assert 'Loop step: 4' in root.locator('.trace-view').inner_text()
            assert 'Loop step: 5' not in root.locator('.trace-view').inner_text()
            run('for step in range(0):\n    print(step)\nprint("Finished")')
            finish()
            assert 'Finished' in root.locator('.trace-view').inner_text()
            assert 'Program finished' in status.inner_text()
            run('for step in range(3)\n    print(step)')
            finish()
            assert 'SyntaxError' in status.inner_text()
            run('print(missing_variable)')
            finish()
            assert 'NameError' in status.inner_text()
            run('for step in range(1000):\n    print(step)')
            assert 'of 501:' in status.inner_text(), status.inner_text()
            run('print("<img src=x onerror=alert(1)>")')
            finish()
            assert root.locator('.trace-view img').count() == 0
            assert '<img src=x' in root.locator('.trace-view').inner_text()
            editor.fill('while True:\n    pass')
            assert root.locator('.trace-view').is_hidden()
            assert 'Code changed' in status.inner_text()
            root.get_by_role('button', name='Run and visualize', exact=True).click()
            root.get_by_role('button', name='Stop', exact=True).click()
            assert 'Stopped' in status.inner_text()
            root.get_by_role('button', name='Restore example', exact=True).click()
            assert editor.input_value() == original
            editor.fill('import time\ntime.sleep(20)')
            root.get_by_role('button', name='Run and visualize', exact=True).click()
            page.wait_for_function('document.querySelector(".trace-status").textContent.includes("Execution stopped after 5 seconds")')
            assert root.get_by_role('button', name='Run and visualize', exact=True).is_enabled()
            root.get_by_role('button', name='Restore example', exact=True).click()
            for width in (390, 320):
                page.set_viewport_size({'width': width, 'height': 844})
                run()
                root.get_by_role('button', name='Next step', exact=True).focus()
                page.keyboard.press('Enter')
                assert 'Step 2 of' in status.inner_text()
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), width
            root.screenshot(path='/tmp/python-loop-explorer-mobile.png')
            page.set_viewport_size({'width': 1280, 'height': 900})
            page.locator('label[title="Switch to dark mode"]').click()
            root.screenshot(path='/tmp/python-loop-explorer-desktop.png')
            page.route('**/pyodide/**', lambda route: route.abort())
            root.get_by_role('button', name='Run and visualize', exact=True).click()
            page.wait_for_function('document.querySelector(".trace-status").textContent.includes("could not load")')
            assert root.get_by_role('button', name='Run and visualize', exact=True).is_enabled()
            # Fresh page has no failed-download route from the previous check.
            page = browser.new_page()
            page.set_default_timeout(90000)
            base = f'http://127.0.0.1:{server.server_port}/python_foundation/notebooks/'
            for filename, marker in (
                ('05_decision_making', '# Single condition example: disk usage warning'),
                ('08_lists_as_data', '# Mini Lab: system readings'),
            ):
                page.goto(base + filename + '/')
                root = page.locator('.python-visualizer')
                assert root.count() == 1
                editor = root.get_by_label('Your Python code')
                status = root.locator('.trace-status')
                original = editor.input_value()
                cells = json.loads((ROOT / 'notebooks' / (filename + '.ipynb')).read_text())['cells']
                assert original == next(''.join(c['source']) for c in cells if ''.join(c['source']).startswith(marker))
                if filename.startswith('05'):
                    for value in (70, 80, 85, 95):
                        run(original.replace('disk_usage = 85', f'disk_usage = {value}'))
                        executed = []
                        while root.get_by_role('button', name='Next step', exact=True).is_enabled():
                            executed.append(root.locator('.trace-current').inner_text())
                            root.get_by_role('button', name='Next step', exact=True).click()
                        output = root.locator('.trace-view > pre').nth(1).inner_text()
                        assert ('Warning: disk usage is high' in output) == (value > 80)
                        assert any('print("Warning:' in line for line in executed) == (value > 80)
                        assert 'Disk check complete' in output
                    run(original.replace('> 80', '> 99'))
                    finish()
                    assert 'Warning:' not in root.locator('.trace-view > pre').nth(1).inner_text()
                else:
                    run()
                    totals = []
                    while root.get_by_role('button', name='Next step', exact=True).is_enabled():
                        for row in root.locator('tbody tr').all():
                            if row.locator('td').first.inner_text() == 'total':
                                totals.append(row.locator('td').nth(1).inner_text())
                        root.get_by_role('button', name='Next step', exact=True).click()
                    assert {'0', '71', '147', '230', '309'}.issubset(totals), totals
                    assert 'Average: 77.25' in root.locator('.trace-view > pre').nth(1).inner_text()
                    for values, expected in (('[10, 20, 30]', 'Average: 20.0'), ('[42]', 'Average: 42.0'), ('[-5, 0, 5, 10, 15]', 'Average: 5.0')):
                        run(original.replace('[71, 76, 83, 79]', values))
                        finish()
                        assert expected in root.locator('.trace-view > pre').nth(1).inner_text()
                    run(original.replace('total + reading', 'total + reading * 2'))
                    finish()
                    assert 'Total: 618' in root.locator('.trace-view > pre').nth(1).inner_text()
                    run(original.replace('[71, 76, 83, 79]', '[]'))
                    finish()
                    assert 'ZeroDivisionError' in status.inner_text()
                root.get_by_role('button', name='Restore example', exact=True).click()
                assert editor.input_value() == original
                page.set_viewport_size({'width': 320, 'height': 844})
                run()
                root.get_by_role('button', name='Next step', exact=True).focus()
                page.keyboard.press('Enter')
                assert 'Step 2 of' in status.inner_text()
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), filename
                root.screenshot(path=f'/tmp/python-{filename}-explorer.png')
                page.set_viewport_size({'width': 1280, 'height': 900})
            print('PASS: decision boundaries and edited threshold; list snapshots, edited values/calculation, empty list error; both mobile explorers.')
            print('PASS: real Python edits, step state, output, zero iterations, errors, text safety, stop/timeout, mobile layout and keyboard controls.')
            browser.close()
    finally:
        server.shutdown()


if __name__ == '__main__':
    check()
