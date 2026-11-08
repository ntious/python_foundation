# Releases and archival

`v1.0.0` is already published and archived on Zenodo. Do not move its tag or replace its archived source. Ordinary commits update the working repository and website, not the archived release.

Track working changes in the [changelog](CHANGELOG.md), then turn the relevant entries into release notes when publishing a tested version.

## Version policy

- Patch (`1.0.1`): corrections to wording, links, or working examples that preserve the learning contract.
- Minor (`1.1.0`): compatible learning supports or site features without removing existing paths or requirements.
- Major (`2.0.0`): deliberately incompatible paths, learning requirements, or adoption contracts. Avoid these changes without a migration plan.

## Maintainer checklist

1. Review the diff, component licensing, citation metadata, and source/download preservation. Keep private student or instructor records out of releases.
2. Run notebook, site, and browser checks described in [website maintenance](website/README.md). Test setup from a clean environment; record which Python/OS was used. A dependency install is not an actual Binder launch.
3. Review [accessibility and limitations](docs/accessibility.md). Document outstanding manual checks honestly.
4. Write release notes describing the final user-visible changes and validation. Use the next version that matches the scope. Do not release every documentation commit automatically.
5. Create a GitHub release from the tested commit. The enabled Zenodo integration archives it and assigns its version DOI.
6. Verify the archive, authorship, license scopes, and DOI. Update `CITATION.cff` and citation instructions with the new version DOI after it exists. Use the all-versions DOI for general sharing. Do not label an old DOI as a newer release or reuse it as the textbook's DOI.

PR workflows report checks. Repository administrators should require the relevant checks in branch rules if they want to prevent unchecked merges; a workflow alone does not enforce that policy. Protecting branches is a repository administration decision, not something this guide silently enables.
