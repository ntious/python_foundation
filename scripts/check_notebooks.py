"""Execute disposable notebook copies; compare every error to an explicit expectation.

This validates distributed starters, not students' completed assignments. Original
files and saved outputs are never changed. Each notebook gets a fresh kernel.
"""
import argparse
import copy
import json
import tempfile
from collections import Counter
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def verify_output(cell, expected_error=None):
    errors = [out.get('ename') for out in cell.get('outputs', []) if out['output_type'] == 'error']
    expected = [expected_error] if expected_error else []
    if errors != expected:
        raise AssertionError(f'Expected errors {expected}; observed {errors}')


def run_notebook(path, spec, kernel):
    raw = json.loads(path.read_text(encoding='utf-8'))
    # Validate at the notebook's declared schema, including older notebooks without IDs.
    schema_copy = copy.deepcopy(raw)
    if schema_copy.get('nbformat_minor', 0) >= 5:
        for i, cell in enumerate(schema_copy['cells']):
            cell.setdefault('id', f'validation-{i}')
    nbformat.validate(schema_copy)
    rules = spec.get('cells', {})
    code_indices = [i for i, c in enumerate(raw['cells']) if c['cell_type'] == 'code']
    assert len(code_indices) == spec['code_cells'], f'{path.name}: update the reviewed cell inventory'
    assert all(int(i) in code_indices for i in rules), f'{path.name}: stale expectations'
    cells, checks, counts = [], [], Counter()
    for index in code_indices:
        source = ''.join(raw['cells'][index]['source'])
        rule = rules.get(str(index), {})
        if 'starts_with' in rule:
            assert source.startswith(rule['starts_with']), f'{path.name}:{index}: expectation no longer matches source'
        if rule.get('error'):
            assert 'starts_with' in rule, 'Expected errors require a source marker'
        answers = rule.get('input', [])
        # A new/unclassified input call fails rather than hanging waiting for stdin.
        setup = (
            'import builtins\n'
            f'_course_answers = {answers!r}\n'
            'def _course_input(prompt=""):\n'
            '    if not _course_answers:\n'
            '        raise AssertionError("Unexpected input prompt; add a reviewed fixture")\n'
            '    return _course_answers.pop(0)\n'
            'builtins.input = _course_input\n'
        )
        cells.append(nbformat.v4.new_code_cell(setup))
        # IPykernel temporarily rebinds builtins.input for each execution request.
        # Set the fixture inside the same request as the original source.
        cells.append(nbformat.v4.new_code_cell('builtins.input = _course_input\n' + source))
        checks.append((len(cells) - 1, index, rule.get('error')))
        cells.append(nbformat.v4.new_code_cell('assert not _course_answers, "Unused input fixture"\n' + rule.get('assert', '')))
        kind = rule.get('kind') or ('expected-error' if rule.get('error') else 'input-example' if answers else 'exercise' if 'TODO' in source or 'Mini Lab' in source else 'working-example')
        counts[kind] += 1
    notebook = nbformat.v4.new_notebook(cells=cells)
    with tempfile.TemporaryDirectory(prefix='python-course-kernel-') as workspace:
        NotebookClient(notebook, kernel_name=kernel, timeout=30, allow_errors=True,
                       resources={'metadata': {'path': workspace}}).execute()
    # allow_errors is only transport: every original and helper cell is checked.
    expected_by_index = {i: error for i, _, error in checks}
    for i, cell in enumerate(notebook.cells):
        try:
            verify_output(cell, expected_by_index.get(i))
        except AssertionError as exc:
            original = next((index for ci, index, _ in checks if ci == i), 'fixture/assertion')
            raise AssertionError(f'{path.name}, cell {original}: {exc}\n{cell.source}') from exc
    print(f'PASS {path.name}: {len(code_indices)} original cells; {dict(counts)}', flush=True)
    return len(code_indices)


def check(kernel='python3'):
    specs = json.loads((ROOT / 'tests/notebook_expectations.json').read_text())['notebooks']
    paths = sorted((ROOT / 'notebooks').glob('*.ipynb'))
    assert {p.name for p in paths} == set(specs), 'Every core notebook needs a reviewed inventory'
    originals = {p: p.read_bytes() for p in paths}
    total = sum(run_notebook(p, specs[p.name], kernel) for p in paths)
    templates = sorted((ROOT / 'templates').glob('*.ipynb'))
    for p in templates:
        template = json.loads(p.read_text())
        if template.get('nbformat_minor', 0) >= 5:
            for i, cell in enumerate(template['cells']):
                cell.setdefault('id', f'validation-{i}')
        nbformat.validate(template)
    assert all(p.read_bytes() == content for p, content in originals.items())
    print(f'PASS: {total} core code cells executed; {len(templates)} template schemas checked; no source files changed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--kernel', default='python3')
    check(parser.parse_args().kernel)
