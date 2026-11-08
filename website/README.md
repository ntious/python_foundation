# Course website maintenance

The website uses MkDocs Material navigation approach with a beginner-focused design. Notebook and Markdown files in the repository remain the authoritative teaching materials. Do not edit generated pages.

From the repository root, in a separate website virtual environment:

```sh
python -m pip install -r requirements-site.txt
python scripts/build_site.py
mkdocs build --strict -f .site-build/mkdocs.yml
python scripts/check_site.py
python scripts/test_teaching_support.py
python scripts/test_oer_identity.py
python scripts/check_accessibility.py
mkdocs serve -f .site-build/mkdocs.yml
```

The generator copies only public course Markdown, notebooks, sample data, licenses, and approved assets. It renders every notebook cell in order without executing Python or publishing stored outputs. It creates navigation from the numbered notebooks. Downloaded notebooks are byte-for-byte copies of the source files.

Edit `website/home.md` for the welcome page and `website/stylesheets/course.css` for appearance. Course objectives, examples, and instructions belong in the existing course files. Website dependencies are separate from Binder requirements.

Grading and optional learning supports live in `docs/` and `templates/`; the generator publishes those same files and lists them under Student guide. Edit the source once, not a second website copy. `test_teaching_support.py` checks the selected peer/walkthrough/stretch examples against original notebook cells and verifies search coverage. It never executes entire notebooks, which contain intentional errors.

GitHub Actions builds and checks links on pull requests. A successful build on `main` publishes to GitHub Pages using the `github-pages` environment. In repository Settings → Pages, the source must be GitHub Actions.

For optional browser interaction checks, install `playwright` in the website environment, run `playwright install chromium`, then `python scripts/test_site_browser.py`. The check starts its own local server under `/python_foundation/` and tests search, copying, downloads, lesson navigation, and mobile layouts. Browser libraries may be needed on Linux. Screenshots go to the operating system temporary directory.

## Notebook and browser validation

Maintainer tools are pinned separately in `requirements-test.txt`; they are not student requirements. In a clean Python 3.11 environment, install `.binder/requirements.txt` and `requirements-test.txt`, then run:

```sh
python -m ruff check
python -m unittest discover -s tests
python scripts/check_notebooks.py
python scripts/check_local_setup.py
```

`tests/notebook_expectations.json` records each core notebook's code-cell count and special cases. Every original code cell is executed in a disposable notebook; each notebook gets a fresh kernel. Input answers and selected semantic assertions are injected only into this disposable test copy. Every observed error must match its explicit expected error type. Missing expected errors also fail. Placeholder/logic-error starters are not silently repaired or graded as completed work. Update the reviewed inventory when changing notebooks; do not auto-approve new errors. Source files are never rewritten. Templates receive schema checks only.

After building the site, also run `python scripts/test_accessibility_browser.py` and `python scripts/test_visualizer.py`. The first runs in Pages CI; the latter downloads the real pinned Pyodide runtime and runs in a separate weekly/manual workflow so a CDN outage does not block every documentation deployment. Both start their own local server. Browser checks require `python -m playwright install --with-deps chromium` on CI Linux hosts. These focused checks do not certify full accessibility.

The generator wraps existing worked Parsons arrangements in native disclosures. Notebook paths, contents, and downloads remain unchanged. Internal review and release-policy notes are local-only and are not published on the course website.
