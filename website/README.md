# Course website maintenance

The website uses the IT4065C site's MkDocs Material navigation approach with a beginner-focused design. Notebook and Markdown files in the repository remain the authoritative teaching materials. Do not edit generated pages.

From the repository root, in a separate website virtual environment:

```sh
python -m pip install -r requirements-site.txt
python scripts/build_site.py
mkdocs build --strict -f .site-build/mkdocs.yml
python scripts/check_site.py
mkdocs serve -f .site-build/mkdocs.yml
```

The generator copies only public course Markdown, notebooks, sample data, licenses, and approved assets. It renders every notebook cell in order without executing Python or publishing stored outputs. It creates navigation from the numbered notebooks. Downloaded notebooks are byte-for-byte copies of the source files.

Edit `website/home.md` for the welcome page and `website/stylesheets/course.css` for appearance. Course objectives, examples, and instructions belong in the existing course files. Website dependencies are separate from Binder requirements.

GitHub Actions builds and checks links on pull requests. A successful build on `main` publishes to GitHub Pages using the `github-pages` environment. In repository Settings → Pages, the source must be GitHub Actions.

For optional browser interaction checks, install `playwright` in the website environment, run `playwright install chromium`, then `python scripts/test_site_browser.py`. The check starts its own local server under `/python_foundation/` and tests search, copying, downloads, lesson navigation, and mobile layouts. Browser libraries may be needed on Linux. Screenshots go to the operating system temporary directory.
