"""Generate a reading website from canonical course files. Never execute notebooks."""
import json
import re
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / '.site-build/source'
REPO = 'https://github.com/ntious/python_foundation'


def notebook_markdown(path):
    notebook = json.loads(path.read_text(encoding='utf-8'))
    relative = path.relative_to(ROOT).as_posix()
    chunks = []
    for cell in notebook['cells']:
        source = ''.join(cell['source'])
        if cell['cell_type'] == 'code':
            # Choose a fence longer than any backtick sequence in the cell.
            fence = '`' * max(3, max((len(s) + 1 for s in re.findall(r'`+', source)), default=3))
            chunks.append(f'{fence}python\n{source}\n{fence}')
        else:
            chunks.append(source)
    actions = (
        f'[Run in Binder](https://mybinder.org/v2/gh/ntious/python_foundation/HEAD?urlpath=lab/tree/{relative}){{ .md-button .md-button--primary }} '
        f'[Open in Colab](https://colab.research.google.com/github/ntious/python_foundation/blob/main/{relative}){{ .md-button }} '
        f'[Download notebook]({path.name}){{ .md-button }}\n\n'
        '!!! tip "Read here. Practice in a notebook."\n'
        '    This page shows the original notebook. Open Binder or Colab to run and edit cells. '
        'Work one cell at a time: some examples are deliberately broken for debugging practice. '
        'Download your work before leaving Binder; its sessions are temporary.\n\n'
        f'[View original source]({REPO}/blob/main/{relative})'
    )
    chunks.insert(1, actions)
    return '\n\n'.join(chunks) + '\n'


def rewrite_links(text):
    # Notebook links become reading pages; original downloads remain available separately.
    def replace(match):
        target = match.group(1)
        if '://' in target:
            return match.group(0)
        target = target.replace('.ipynb', '.md')
        if target == 'setup/':
            target = 'setup/index.md'
        return '](' + target + ')'
    return re.sub(r'\]\(([^)]+)\)', replace, text)


def build():
    if SOURCE.exists():
        shutil.rmtree(SOURCE)  # Only our generated source directory.
    SOURCE.mkdir(parents=True)
    paths = list(ROOT.glob('*.md'))
    for folder in ('docs', 'setup', 'templates', 'data'):
        paths.extend((ROOT / folder).glob('*.md'))
    for path in paths:
        destination = SOURCE / path.relative_to(ROOT)
        if path == ROOT / 'README.md':
            destination = SOURCE / 'repository.md'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rewrite_links(path.read_text(encoding='utf-8')), encoding='utf-8')
    for folder in ('notebooks', 'templates'):
        for path in sorted((ROOT / folder).glob('*.ipynb')):
            destination = SOURCE / path.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, destination)
            destination.with_suffix('.md').write_text(rewrite_links(notebook_markdown(path)).replace(
                f'[Download notebook]({path.stem}.md)', f'[Download notebook]({path.name})'), encoding='utf-8')
    # Explicit public assets only: never publish arbitrary repository files.
    for path in [ROOT / 'docs/course_map.png', ROOT / 'LICENSE', ROOT / 'CITATION.cff', *sorted((ROOT / 'data').glob('*.csv'))]:
        if path.exists():
            destination = SOURCE / path.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, destination)
    shutil.copytree(ROOT / 'website/stylesheets', SOURCE / 'stylesheets')
    lessons = sorted((ROOT / 'notebooks').glob('*.ipynb'))
    titles = []
    for path in lessons:
        first = ''.join(json.loads(path.read_text())['cells'][0]['source']).splitlines()[0]
        title = re.sub(r'^#\s*(?:Module \d+:\s*|\d+\s+)?', '', first)
        titles.append((path, title))
    cards = '\n\n'.join(f'- **{i:02d} · [{title}]({p.relative_to(ROOT).with_suffix(".md").as_posix()})**' for i, (p, title) in enumerate(titles))
    home = (ROOT / 'website/home.md').read_text().replace('<!-- LESSONS -->', cards)
    (SOURCE / 'index.md').write_text(home)
    for folder, title in [('setup', 'Choose your notebook environment'), ('templates', 'Practice templates'), ('data', 'Optional sample data')]:
        if folder == 'data':
            continue
        entries = sorted((SOURCE / folder).glob('*.md'))
        (SOURCE / folder / 'index.md').write_text(f'# {title}\n\n' + '\n'.join(f'- [{p.stem.replace("_", " ").title()}]({p.name})' for p in entries))
    config = yaml.safe_load((ROOT / 'mkdocs.yml').read_text())
    config['nav'] = [
        {'Welcome': 'index.md'},
        {'Lessons': [{'Start here': 'QUICKSTART.md'}] + [{f'{i:02d} · {title}': p.relative_to(ROOT).with_suffix('.md').as_posix()} for i, (p, title) in enumerate(titles)]},
        {'Student guide': [{'Using notebooks': 'docs/how_to_use_notebooks.md'}, {'Course map': 'COURSE_MAP.md'}, {'Assessment': 'ASSESSMENT_OVERVIEW.md'}, {'Submitting work': 'docs/assignment_submission_guide.md'}, {'AI and your learning': 'docs/ai_usage_guidelines.md'}, {'Frequently asked questions': 'docs/faq.md'}, {'Templates': 'templates/index.md'}]},
        {'Setup & help': [{'Environments': 'setup/index.md'}, {'Binder': 'setup/binder_instructions.md'}, {'Colab': 'setup/colab_instructions.md'}, {'Replit (optional)': 'setup/replit_instructions.md'}, {'Troubleshooting': 'setup/troubleshooting.md'}]},
        {'For instructors': [{'Teaching guide': 'INSTRUCTOR_GUIDE.md'}, {'Program overview': 'PROGRAM_OVERVIEW.md'}, {'Impact metrics': 'IMPACT_METRICS.md'}, {'Repository overview': 'repository.md'}, {'Reuse and licensing': 'OER_LICENSE.md'}]},
    ]
    # Absolute paths keep the generated config independent of its own location.
    config['docs_dir'] = str(SOURCE)
    config['site_dir'] = str(ROOT / '.site-build/output')
    (ROOT / '.site-build/mkdocs.yml').write_text(yaml.safe_dump(config, sort_keys=False))
    print(f'Prepared {len(lessons)} lessons directly from notebooks; originals unchanged.')


if __name__ == '__main__':
    build()
