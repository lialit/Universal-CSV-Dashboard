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
python .\scripts\validate_release.py --tag v1.0.0-smoke.1 --allow-smoke-tag
```

The validator checks:

- valid Semantic Versioning in `VERSION`;
- presence of `[Unreleased]` in `CHANGELOG.md`;
- presence of a changelog section matching `VERSION`;
- exact equality between a normal release tag and `v<VERSION>`;
- smoke tags use the restricted `v<VERSION>-smoke.N` form.

## GitHub workflow

Open **Actions → Release preparation → Run workflow**.

Provide a tag and choose the workflow mode:

- `create_draft = false`, `smoke_test = false`: validation only;
- `create_draft = true`, `smoke_test = false`: prepare a real draft release for `v<VERSION>`;
- `create_draft = true`, `smoke_test = true`: prepare a disposable draft with a tag such as `v1.0.0-smoke.1`.

Smoke-test mode exists only to verify draft creation and generated release notes without changing `VERSION` or pretending that the next product version is ready. Smoke drafts receive a prominent `DO NOT PUBLISH` title. The workflow rejects smoke tags unless smoke mode is explicitly enabled, and rejects smoke mode unless draft creation is enabled.

The workflow refuses to create a draft when the requested release already exists. Validation-only runs remain read-only and may validate an already published version.

## Draft smoke-test checklist

1. Run the workflow with `tag = v<VERSION>-smoke.1`.
2. Set `create_draft = true`.
3. Set `smoke_test = true`.
4. Confirm the workflow is green.
5. Open the draft and verify the `DO NOT PUBLISH` title, target branch and generated notes.
6. Do not publish the smoke draft.
7. Delete the smoke draft after validation.

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
