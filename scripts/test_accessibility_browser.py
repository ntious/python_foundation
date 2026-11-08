"""Representative keyboard, disclosure, focus-contrast and mobile checks."""
import functools
import http.server
import threading
from playwright.sync_api import sync_playwright
from test_site_browser import Handler, ROOT


def contrast(first, second):
    def luminance(rgb):
        values = [int(v) / 255 for v in rgb.removeprefix('rgb(').removesuffix(')').split(',')]
        values = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
        return sum(a * b for a, b in zip(values, (.2126, .7152, .0722)))
    a, b = sorted((luminance(first), luminance(second)))
    return (b + .05) / (a + .05)


def check():
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Handler, directory=str(ROOT / '.site-build/output')))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/python_foundation/'
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(reduced_motion='reduce')
            page.goto(base)
            page.keyboard.press('Tab')
            assert page.locator(':focus').get_attribute('href') == '#small-steps-useful-code-growing-confidence'
            page.keyboard.press('Enter')
            for width in (1280, 320):
                page.set_viewport_size({'width': width, 'height': 900})
                page.goto(base + 'notebooks/07_loops/')
                disclosure = page.locator('.worked-example').first
                assert disclosure.count() == 1
                assert disclosure.get_attribute('open') is None
                disclosure.locator('summary').focus()
                page.keyboard.press('Space')
                assert disclosure.get_attribute('open') is not None
                pre = disclosure.locator('pre')
                assert pre.get_attribute('tabindex') == '0'
                pre.focus()
                assert page.locator(':focus').evaluate('(el) => el.tagName') == 'PRE'
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), width
            for scheme in ('default', 'slate'):
                page.evaluate('(scheme) => document.body.setAttribute("data-md-color-scheme", scheme)', scheme)
                button = page.get_by_role('button', name='Mark this lesson as done')
                button.focus()
                colors = button.evaluate('(el) => [getComputedStyle(el).outlineColor, getComputedStyle(document.body).backgroundColor]')
                assert contrast(*colors) >= 3, (scheme, colors)
                assert float(button.evaluate('(el) => parseFloat(getComputedStyle(el).outlineWidth)')) >= 2
            browser.close()
            # Native disclosures and reading paths remain available without JavaScript.
            browser = p.chromium.launch()
            page = browser.new_page(java_script_enabled=False)
            page.goto(base + 'notebooks/07_loops/')
            page.locator('.worked-example summary').first.click()
            assert page.locator('.worked-example[open] pre').is_visible()
            assert page.get_by_role('link', name='Run in Binder', exact=True).is_visible()
            browser.close()
            print('PASS: keyboard skip/disclosure/code focus, light/dark focus contrast, reduced-motion context, 320px layout, no-JavaScript fallback.')
    finally:
        server.shutdown()


if __name__ == '__main__':
    check()
