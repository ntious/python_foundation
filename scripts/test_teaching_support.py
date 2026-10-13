"""Check teaching-support examples using selected original cells, never Run All."""
import contextlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def source(name, marker):
    notebook = json.loads((ROOT / 'notebooks' / name).read_text())
    matches = [''.join(cell['source']) for cell in notebook['cells']
               if cell['cell_type'] == 'code' and marker in ''.join(cell['source'])]
    assert len(matches) == 1, (name, marker)
    return matches[0]


def run(code):
    output = io.StringIO()
    namespace = {}
    with contextlib.redirect_stdout(output):
        exec(compile(code, '<selected course example>', 'exec'), namespace)
    return output.getvalue(), namespace


def check():
    # Only these known non-interactive examples run; intentional errors stay untouched.
    logic = '06_multi_condition_logic.ipynb'
    peer = source(logic, '# Side-by-side comparison\n')
    assert run(peer)[0] == 'AND result: False\nOR result: True\n'
    assert run(peer.replace('has_admin_permission = False', 'has_admin_permission = True'))[0] == 'AND result: True\nOR result: True\n'
    walkthrough = source(logic, '# AND example: system access control')
    assert run(walkthrough)[0] == 'Access allowed\n'
    assert run(walkthrough.replace('has_active_account = True', 'has_active_account = False'))[0] == 'Access denied\n'
    boundary = source(logic, '# Review: one condition')
    assert run(boundary.replace('disk_usage = 82', 'disk_usage = 80'))[0] == ''
    assert run(boundary.replace('disk_usage = 82', 'disk_usage = 81'))[0] == 'Disk usage warning\n'
    expenses = source('04_arithmetic_and_comparison.ipynb', '# Total expenses using +')
    changed = run(expenses.replace('books = 45.50', 'books = 0'))[1]
    assert abs(changed['total_expenses'] - 31.49) < 1e-9
    loop = source('07_loops.ipynb', '# This loop repeats the indented line 3 times.')
    assert run(loop.replace('range(3)', 'range(0)'))[0] == ''
    readings = source('08_lists_as_data.ipynb', '# Mini Lab: system readings')
    single = run(readings.replace('[71, 76, 83, 79]', '[80]'))[1]
    assert single['total'] == single['average'] == 80
    original = run(readings)[1]
    assert original['total'] == sum(original['system_readings'])
    device = source('09_functions.ipynb', '# device_name is one parameter.')
    assert run(device.replace('"Printer"', '"Scanner"'))[0] == 'Scanner is ready\nRouter is ready\n'
    search = json.loads((ROOT / '.site-build/output/search/search_index.json').read_text())
    for path in ('docs/grading_overview/', 'docs/peer_learning/', 'docs/stretch_prompts/', 'templates/mid_course_reflection/'):
        assert any(entry['location'].startswith(path) for entry in search['docs']), path
    print('PASS: peer, walkthrough, and stretch examples use original cells; all teaching supports searchable.')


if __name__ == '__main__':
    check()
