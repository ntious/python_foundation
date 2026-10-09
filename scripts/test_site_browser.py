"""Optional UI smoke test: pip install playwright; playwright install chromium."""
import functools
import http.server
import threading
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/python_foundation/'):
            self.path = self.path.removeprefix('/python_foundation')
        super().do_GET()

    def log_message(self, *args):
        pass


def check():
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Handler, directory=str(ROOT / '.site-build/output')))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/python_foundation/'
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(permissions=['clipboard-read', 'clipboard-write'])
            page = context.new_page()
            page.set_default_timeout(10000)
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(base)
            page.get_by_role('link', name='Start your first lesson', exact=True).click()
            page.wait_for_url('**/notebooks/00_getting_started/')
            page.wait_for_load_state('networkidle')
            page.get_by_role('button', name='Copy to clipboard').first.click()
            copied = page.evaluate('navigator.clipboard.readText()')
            assert 'print("Hello, world!")' in copied
            assert page.get_by_role('link', name='Run in Binder', exact=True).get_attribute('href').endswith('.ipynb')
            with page.expect_download() as download:
                page.get_by_role('link', name='Download notebook', exact=True).click()
            assert download.value.suggested_filename == '00_getting_started.ipynb'
            page.get_by_role('link', name='Next: 01 · Python in the Real World', exact=True).click()
            page.wait_for_url('**/notebooks/01_python_in_the_real_world/')
            search = page.get_by_role('textbox', name='Search')
            search.fill('Fix Log')
            page.locator('.md-search-result__link').first.wait_for(state='visible')
            assert page.locator('.md-search-result').inner_text().find('Fix Log') >= 0
            page.keyboard.press('Escape')
            page.goto(base)
            page.screenshot(path=str(Path(tempfile.gettempdir()) / 'python-foundation-desktop.png'), full_page=True)
            for width in (390, 320):
                page.set_viewport_size({'width': width, 'height': 844})
                page.goto(base)
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), width
                page.locator('.md-header label[for="__drawer"]').click()
                assert page.locator('#__drawer').is_checked()
                page.locator('#__nav_2_label').click()
                page.locator('.md-sidebar--primary').get_by_role('link', name='00 · Getting Started with Python', exact=True).click()
                page.wait_for_url('**/notebooks/00_getting_started/')
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), width
            page.screenshot(path=str(Path(tempfile.gettempdir()) / 'python-foundation-mobile.png'), full_page=True)
            assert not errors, errors
            browser.close()
            print('PASS: desktop/mobile navigation, search, code clipboard, notebook download, 320/390px layout, no JavaScript errors.')
    finally:
        server.shutdown()


if __name__ == '__main__':
    check()
