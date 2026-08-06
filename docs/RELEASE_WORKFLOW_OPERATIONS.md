# Release Workflow Operations

The **Release preparation** workflow uses one explicit `mode` choice instead of two independent boolean inputs. This prevents invalid combinations and makes each run easier to audit.

## Modes

### `validate-only`

Use this to validate a normal release tag without creating a GitHub Release.

- The tag must not contain `-smoke.`.
- No draft or published release is created.

### `create-draft`

Use this to validate a normal release tag and create an unpublished draft release with generated notes.

- The tag must not contain `-smoke.`.
- Review the draft before publishing it manually.

### `smoke-draft`

Use this only for release-automation regression tests.

- The tag must match the guarded smoke form, for example `v1.0.0-smoke.3`.
- The workflow creates an unpublished draft named with the prefix `[SMOKE TEST — DO NOT PUBLISH]`.
- Never publish a smoke draft.

## Smoke cleanup

After inspecting a smoke draft:

1. Open **Releases**.
2. Open the draft marked `[SMOKE TEST — DO NOT PUBLISH]`.
3. Choose **Edit**.
4. Select **Delete this release** and confirm.
5. Verify that the smoke tag no longer appears in the releases list.

Deleting the draft is part of the smoke-test completion criteria. Stable and prerelease releases must remain untouched.

## Run summary

Every workflow run records the requested tag and mode in the GitHub Actions job summary. Draft-producing modes also record the draft URL. Smoke mode adds an explicit cleanup reminder.

## Final regression checklist

Before considering release automation ready:

- `validate-only` accepts the current normal release tag format without creating a release;
- a smoke tag is rejected in `validate-only` and `create-draft` modes;
- a normal tag is rejected in `smoke-draft` mode;
- `smoke-draft` creates an unpublished draft with the warning prefix;
- generated notes use the categories from `.github/release.yml`;
- the smoke draft is deleted after inspection.
