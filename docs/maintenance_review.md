# Maintenance review and improvement scope

This is a maintainer review, not an additional student assignment. The approximately 12 guided hours remain estimates; effectiveness and independent workload need learner evidence.

## Current state and benchmark

The OER already has a numbered beginner sequence, Binder/Colab support, assessment guidance, online-teaching and adoption notes, website checks, and editable execution explorers. Version 1.0.0 is already archived on Zenodo.

[Berkeley D-Lab Python Fundamentals](https://github.com/dlab-berkeley/Python-Fundamentals) is a useful organizational benchmark: separate lessons/solutions, setup instructions, glossary, and a project. Its six-part workshop includes Pandas and data-science analysis/visualization. This OER serves a different IT/CIS and non-CS programming-literacy purpose. Repository stars and forks do not establish student learning or institutional adoption.

## Risks and priorities

| Priority | Finding | Response |
|---|---|---|
| High | Blanket notebook execution rejects intentional errors and waits at input prompts | Fresh-kernel execution with explicit error types, input fixtures, and semantic assertions |
| High | Setup claims and website execution wording can mislead | Correct launch wording and distinguish reading blocks, explorers, and full notebooks |
| Medium | Students and adopters must search a long README | Put student, instructor, online, and local entry points first |
| Medium | Local installation and accessibility options need a clear home | Publish local setup and accessibility guides in navigation |
| Medium | Worked Parsons arrangements are immediately visible | Native, keyboard-operable disclosures on reading pages; original notebooks preserved |
| Optional | Glossary and a real learner screenshot improve orientation | Short concept glossary and a screenshot of the actual explorer |

No critical defect was established by this scoped maintenance review. This is not an exhaustive security audit or accessibility certification.

## Architecture and files

Keep `notebooks/`, `templates/`, `docs/`, and `setup/` stable. Add maintainer-only `tests/notebook_expectations.json`, `scripts/check_notebooks.py`, and a notebook workflow. Reuse the site generator; do not create another copy of teaching content. New learner references are `setup/local_instructions.md`, `docs/glossary.md`, and `docs/accessibility.md`. `RELEASING.md` documents subsequent versions. No notebooks are removed, renamed, or split into competing editions.

The README now prioritizes entry points and a real screenshot. Citation, optional textbook, and reuse notices remain available. Existing institutional exclusions and component licenses remain in force.

## CI and execution policy

- Notebook workflow: called by the site workflow on pull requests and main pushes, with a manual option. Python 3.11, constrained learner dependencies, pinned maintainer tools, schema checks, 129 original core code cells in fresh notebook kernels, known-error checks, supplied input fixtures, and selected semantic assertions. No source notebook is overwritten. Templates get schema validation, not automatic grading. Website deployment waits for both notebook and site checks.
- Site workflow: strict build, link/search/download preservation, teaching-support and identity checks, plus representative accessibility and browser checks. Local-only browser checks also exist for the full explorers; scheduled/manual checks exercise their network-dependent runtime.
- Maintainer Ruff checks target syntax and undefined names in scripts/tests, not deliberate lesson errors. Adding every suggested tool would duplicate checks without improving this contract.
- Starter logic mistakes and placeholders stay classified as such. A passing smoke test is not evidence that a student's task is completed. Assertions test documented starter behavior and selected corrected/boundary examples separately.

## Reproducibility and honest limits

Validation outcomes for this maintenance change are recorded below after execution. A clean Python installation is distinct from Binder's hosted build and launch. Dependency constraints are compatibility bounds, not an exact lock of all transitive dependencies. The runtime used by browser explorers is separate from the learner notebook environment.

Manual work remains: assistive-technology testing, school-network behavior, beginner timing feedback, and ongoing hosted-service reliability. Windows/macOS instructions should be checked on actual devices; a Linux run alone does not prove both platforms.

### Validation record — November 8, 2026

- Fresh Linux Python 3.11.18 environment: installed the unchanged learner dependency bounds plus separate pinned test tools. Resolved learner tools were Notebook 7.6.5, JupyterLab 4.6.6, and ipykernel 7.4.0; validation used nbclient 0.10.2 and nbformat 5.10.4. All 129 core code cells executed in fresh notebook kernels with reviewed inputs, 14 expected runtime/syntax errors, and selected semantic assertions. Three template schemas passed. Original notebook files were preserved.
- The first test-harness run exposed ipykernel's per-request rebinding of `input()`. The harness now applies its fixture in the same execution request as the source. This was a test integration issue; the educational examples were not repaired or changed to make tests pass.
- The local authenticated JupyterLab server served its interface and notebook 00 successfully. This tests Linux; it does not establish Windows/macOS installation success.
- A direct Binder API request returned HTTP 400. The normal browser launch of source commit `c652f69` reached hosted JupyterLab, and its contents API returned notebook 00 with HTTP 200. The Binder configuration and core notebooks are unchanged in this maintenance work. No claim of perpetual availability or a clean uncached hosted build is made.
- Structural checks passed for image text alternatives, document language, and content heading hierarchy. Browser checks passed for keyboard skip/disclosure/code navigation, light/dark focus-ring contrast, 320-pixel layout, and the reading/disclosure fallback without JavaScript. This does not establish full screen-reader accessibility.

Site preservation checks passed for the generated pages and all 16 original notebook downloads. Desktop/mobile navigation, search, clipboard, theme, and progress checks passed. The mobile-search harness was changed to type actual key events after a synthetic fill raced Material's search observers. Explorer checks cover edited values and calculations, decision boundaries, list snapshots, errors, stopping, timeout, and mobile keyboard controls. Publication results are available in the maintenance commit's GitHub Actions runs. No separate Python course edition or extra student assessment was introduced.

## Changes deliberately avoided

Do not add Pandas or advanced topics to match the benchmark; increase required assessment; move stable notebook URLs; publish private answer keys; treat the textbook as a prerequisite; change archived release tags; claim measured impact from repository traffic; or advertise instant execution, guaranteed Binder availability, or full WCAG compliance.
