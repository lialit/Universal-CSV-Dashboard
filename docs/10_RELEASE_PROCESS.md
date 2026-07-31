# Release Process

This procedure is the executable release checklist for Universal CSV
Dashboard. It covers release candidates, final releases and rollback.

The first stable release is `1.0.0`, promoted from `1.0.0-rc.1`. A release is
not complete because the version exists in source code: validation, a tag and
a GitHub Release are separate, intentional steps.

## Release roles and sources of truth

| Source | Responsibility |
|---|---|
| `app_core/version.py` | Canonical product version |
| `CHANGELOG.md` | Shipped user-visible history |
| `releases/v1.0/release_notes.md` | Frozen scope, validation and release record |
| `releases/v1.0/readiness_audit.md` | Current repository evidence |
| `ROADMAP.md` | Product direction and current stage |
| Git tag | Immutable published version marker |
| GitHub Release | Public notes and downloadable release record |

The release owner performs the steps below. A second person should review a
stable public release when another maintainer is available.

## 1. Freeze the scope

Before final validation:

- [ ] confirm the candidate version in `app_core/version.py`;
- [ ] move unfinished capabilities out of the release scope;
- [ ] update README, roadmap, changelog and release notes;
- [ ] confirm known limitations and non-goals;
- [ ] stop feature work on the release branch;
- [ ] allow only launch-blocking fixes after the freeze.

For `1.0.0-rc.1`, the frozen scope is listed in
[`releases/v1.0/release_notes.md`](../releases/v1.0/release_notes.md).

## 2. Prepare a clean release candidate

Start from an up-to-date `main`:

```bash
git switch main
git pull --ff-only origin main
git status --short
```

`git status --short` must produce no output.

Create a dedicated branch:

```bash
git switch -c release/1.0.0-rc.1
```

Do not reuse a branch that contains unrelated work.

## 3. Verify a clean install

Use Python 3.11 and a new virtual environment. Do not validate against the
development environment.

### Windows PowerShell

```powershell
if (Test-Path .venv-release) {
    throw "Remove the existing .venv-release before clean-install validation."
}

py -3.11 -m venv .venv-release
.\.venv-release\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-security.txt
```

### macOS or Linux

```bash
test ! -e .venv-release
python3.11 -m venv .venv-release
source .venv-release/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-security.txt
```

If dependency installation fails, stop. Do not create a tag from a partially
installed environment.

## 4. Run automated validation

Run every command from the repository root:

```bash
python -m pip check
python -m pip_audit -r requirements.txt --strict
python -m ruff check .
python scripts/security_review.py --root .
python -m pytest -q
python scripts/release_readiness.py --root . --strict
```

Required result:

- dependency compatibility passes;
- no known audited dependency vulnerability remains;
- Ruff passes;
- every security and privacy control passes;
- pytest passes;
- the strict release-readiness audit exits successfully.

Record the date, Python version, test count and readiness result in
`releases/v1.0/readiness_audit.md`.

## 5. Run manual release validation

Use representative, non-sensitive files from `sample_data/` and `examples/`.

- [ ] upload a supported CSV;
- [ ] review and edit detected fields;
- [ ] verify Executive Overview totals;
- [ ] inspect Business Insights evidence and limitations;
- [ ] inspect the Data Quality Score breakdown;
- [ ] ask each available Analysis Assistant question;
- [ ] reopen a saved project against the matching CSV;
- [ ] export and open all three Excel/PDF themes;
- [ ] confirm the Excel workbook contains row-level data warnings;
- [ ] confirm the PDF omits the complete row-level dataset;
- [ ] review empty, warning and unsupported-question states;
- [ ] review keyboard navigation, focus, contrast and 200% zoom;
- [ ] verify the final screenshots and demo GIF match the candidate.

Record defects before continuing. Release-blocking defects return the process
to step 2 after a focused fix.

## 6. Open and validate the release-candidate pull request

The pull request must:

- target `main`;
- contain only release-candidate changes;
- describe scope, exclusions and validation;
- have a green GitHub Actions run;
- have no unresolved release-blocking review comments.

Merge only after the candidate commit has been reviewed.

## 7. Create the release candidate tag

After the release-candidate pull request is merged:

```bash
git switch main
git pull --ff-only origin main
git status --short
git tag -a v1.0.0-rc.1 -m "Universal CSV Dashboard 1.0.0-rc.1"
git push origin v1.0.0-rc.1
```

Create a GitHub Release from `v1.0.0-rc.1` and mark it as a **pre-release**.
Copy the factual scope, limitations and validation result from
`releases/v1.0/release_notes.md`.

Do not move or recreate a published tag.

## 8. Promote the candidate to the final release

After candidate validation:

1. change the canonical version to `1.0.0`;
2. mark the v1.0 notes `Released`;
3. add the release date and final test evidence;
4. add or finalize the `[1.0.0]` changelog section;
5. update roadmap and Release Hub status;
6. run steps 3–6 again;
7. merge the final release pull request;
8. create and push the annotated `v1.0.0` tag;
9. publish the GitHub Release;
10. verify installation from the published tag.

Example tag commands:

```bash
git switch main
git pull --ff-only origin main
git tag -a v1.0.0 -m "Universal CSV Dashboard 1.0.0"
git push origin v1.0.0
```

## Rollback

### Before a tag is published

Close the release pull request or revert its release-only commit. Fix the
problem on a new branch and repeat validation. An unpublished local tag may be
deleted:

```bash
git tag -d v1.0.0-rc.1
```

### After a tag or GitHub Release is published

Never move or silently replace the published tag.

1. mark the affected GitHub Release as withdrawn or clearly deprecated;
2. document the reason and affected behavior;
3. revert the faulty merge on `main` through a reviewed pull request when
   necessary;
4. create a corrected patch or new candidate version;
5. repeat the complete validation process;
6. publish a new immutable tag, for example `v1.0.0-rc.2` or `v1.0.1`;
7. link the replacement release from the withdrawn release.

If saved-project or export compatibility is affected, document the impact and
recovery steps before publishing the replacement.

## Release record

After publication, complete all fields in
`releases/v1.0/release_notes.md`:

- release date;
- exact Git tag;
- GitHub Release link;
- supported Python version;
- migration requirement;
- final commit;
- validation result.

The release is complete only when the repository, tag, GitHub Release and
documentation describe the same product state.
