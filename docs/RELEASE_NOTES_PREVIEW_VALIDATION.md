# Release Notes Preview Validation

GH-04E validates the generated release-note category precedence with a guarded smoke draft.

## Prepared pull request labels

- PR #29: `enhancement`, `area: github`, `area: docs`
- PR #30: `testing`, `area: github`, `area: docs`
- PR #31: `bug`, `area: github`
- PR #32: `bug`, `area: github`

## Expected generated-note placement

- PR #29 appears under **Features and improvements**.
- PR #30 appears under **Testing and quality**.
- PR #31 and PR #32 appear under **Fixes**.
- None of PR #29–#32 appears under **Other changes**.

Semantic change-type categories intentionally precede path-based area categories. This prevents a testing or bug-fix pull request from being classified as documentation or repository infrastructure only because it changed files in those areas.

## Smoke draft

After this configuration is merged, run the guarded release workflow with:

- tag: `v1.0.0-smoke.2`
- create_draft: `true`
- smoke_test: `true`

Inspect the generated sections, record the result, then delete the unpublished smoke draft.
