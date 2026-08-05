# Release Automation

Universal CSV Dashboard uses a guarded, manual release-preparation workflow. Repository changes still go through a protected pull request; the release workflow only runs after release metadata is present in `main`.

## Canonical version

`VERSION` is the single canonical project version and must contain a valid Semantic Versioning value such as `1.1.0`.

The same version must have a matching section in `CHANGELOG.md`:

```text
## [1.1.0] — YYYY-MM-DD
```

## Local validation

```powershell
python .\scripts\validate_release.py
python .\scripts\validate_release.py --tag v1.0.0
```

The validator checks:

- valid Semantic Versioning in `VERSION`;
- presence of `[Unreleased]` in `CHANGELOG.md`;
- presence of a changelog section matching `VERSION`;
- exact equality between the requested tag and `v<VERSION>`.

## GitHub workflow

Open **Actions → Release preparation → Run workflow**.

Provide a tag such as `v1.0.0` and choose whether to create a draft release.

- With `create_draft = false`, the workflow performs validation only.
- With `create_draft = true`, it creates a draft GitHub Release targeting `main` with generated notes.

The workflow refuses to continue if the release already exists or the tag does not match `VERSION`.

## Release checklist

1. Complete the release milestone and required issues.
2. Update `VERSION` through a protected pull request.
3. Move entries from `[Unreleased]` into the matching dated version section.
4. Wait for the complete CI and Project automation checks.
5. Merge the release-preparation PR.
6. Run the release workflow in validation-only mode.
7. Run it again with draft creation enabled.
8. Review generated notes, links and compatibility information.
9. Publish the draft manually only after final smoke testing.

The workflow intentionally does not publish releases automatically.
