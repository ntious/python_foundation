"""Focused structural checks, not an accessibility-conformance certification."""
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Content(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_article = False
        self.headings = []
        self.errors = []
        self.lang = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'article':
            self.in_article = True
        if tag == 'img' and 'alt' not in attrs:
            self.errors.append('Image is missing alt (use an empty alt only when decorative)')
        if self.in_article and tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.headings.append(int(tag[1]))

    def handle_endtag(self, tag):
        if tag == 'article':
            self.in_article = False


def check():
    errors = []
    pages = list((ROOT / '.site-build/output').rglob('*.html'))
    for path in pages:
        if path.name == '404.html':
            continue
        content = Content()
        content.feed(path.read_text())
        if not content.lang:
            content.errors.append('Document language missing')
        if content.headings.count(1) != 1:
            content.errors.append('Content needs exactly one top-level heading')
        for previous, current in zip(content.headings, content.headings[1:]):
            if current > previous + 1:
                content.errors.append(f'Heading skips from h{previous} to h{current}')
        errors.extend(f'{path.relative_to(ROOT)}: {e}' for e in content.errors)
    assert pages, 'Build the website first'
    assert not errors, '\n'.join(errors)
    print(f'PASS: image alt attributes, document language, and content heading hierarchy across {len(pages)} pages.')


if __name__ == '__main__':
    check()
