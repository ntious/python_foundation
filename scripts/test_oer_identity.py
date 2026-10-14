"""Keep the OER identity separate from institutional catalog text."""
import json
import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TITLE = 'Introduction to Python: A Guided Beginner Course'


def check():
    # Split historical identifiers so the check itself does not republish them.
    excluded = ('IT' + '1009C',
                'Apply fundamental ' + 'Python constructs (variables, data types, control structures) to solve simple problems',
                'Develop and debug ' + 'basic Python programs addressing real-world scenarios')
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    sources = [ROOT / name for name in names if name and (ROOT / name).is_file()]
    generated = [p for p in (ROOT / '.site-build/output').rglob('*') if p.is_file()]
    for path in sources + generated:
        try:
            content = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        assert not any(term in content for term in excluded), path.relative_to(ROOT)
    config = yaml.safe_load((ROOT / 'mkdocs.yml').read_text())
    citation = yaml.safe_load((ROOT / 'CITATION.cff').read_text())
    assert config['site_name'] == citation['title'] == TITLE
    # Do not imply that users can choose either license for the entire resource.
    assert 'license' not in citation
    assert 'MIT' in citation['abstract'] and 'CC BY 4.0' in citation['abstract']
    outcomes = (ROOT / 'LEARNING_OUTCOMES.md').read_text()
    assert len(re.findall(r'^\d\. \*\*', outcomes, re.MULTILINE)) == 5
    for name in ('README.md', 'PROGRAM_OVERVIEW.md', 'COURSE_MAP.md'):
        assert '(LEARNING_OUTCOMES.md)' in (ROOT / name).read_text(), name
    search = json.loads((ROOT / '.site-build/output/search/search_index.json').read_text())
    assert any(entry['location'].startswith('LEARNING_OUTCOMES/') for entry in search['docs'])
    print('PASS: current sources/site exclude institutional code and catalog outcomes; title, citation scopes, and OER outcome links agree.')


if __name__ == '__main__':
    check()
