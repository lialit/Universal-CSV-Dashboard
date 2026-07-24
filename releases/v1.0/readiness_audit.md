# v1.0 Release Readiness Audit

**Audit date:** 2026-07-24

**Baseline commit:** `24825fa`

**Latest checkpoint:** L-04A — README & Changelog Alignment

**Overall status:** **Not ready**

## Result

| Status | Count |
|---|---:|
| PASS | 18 |
| WARN | 0 |
| FAIL | 3 |

The full automated test suite, including the readiness checker tests, passes:

```text
145 passed
```

This means the implemented product logic is stable under the current automated
tests. It does **not** mean the repository is ready for a public `v1.0` release.
The remaining failures concern release-candidate status, the repeatable release
process and the final demo asset.

## Automated findings

| ID | Category | Check | Status | Evidence |
|---|---|---|---|---|
| DOC-001 | Documentation | Required public documents | PASS | README, onboarding, changelog, contribution, license and security files exist |
| APP-001 | Product | Core application structure | PASS | All launch-critical pages and analytical modules exist |
| DATA-001 | Product | Safe representative sample | PASS | `sample_sales.csv` contains date, region and sales |
| DATA-002 | Product | Varied examples | PASS | Five example CSV files are present |
| TEST-001 | Engineering | Automated test structure | PASS | Eighteen test modules are present after L-03 |
| CI-001 | Engineering | CI installs dependencies | PASS | GitHub Actions installs the bounded requirements |
| CI-002 | Engineering | CI runs pytest | PASS | GitHub Actions executes the complete test suite |
| CI-003 | Engineering | CI runs static checks | PASS | Ruff checks syntax-level and Pyflakes failures |
| DEP-001 | Engineering | Dependencies bounded | PASS | Requirements have intentional lower and upper bounds |
| DEP-002 | Engineering | Python support defined | PASS | README and CI reference Python 3.11 |
| DEP-003 | Engineering | Dependency vulnerability gate | PASS | Strict `pip-audit` runs in CI with a bounded tool version |
| REPO-001 | Repository | Generated artifacts untracked | PASS | Tracked `.pyc` files were removed and ignore rules hardened |
| SEC-001 | Security | No obvious tracked secrets | PASS | No credential-like tracked values detected |
| SEC-002 | Security | Actionable security policy | PASS | Private reporting, supported versions and response process are documented |
| SEC-003 | Security | Local-first privacy controls | PASS | Upload flow, runtime clients, errors and privacy documentation pass review |
| DOC-002 | Documentation | README matches shipped UI | PASS | README includes every current navigation page and the delivered 0.3–0.6 capabilities |
| REL-001 | Release | Changelog covers 0.3–0.6 | PASS | Understand, Explain, Share and Assist are documented as delivered, untagged milestones |
| REL-002 | Release | v1.0 release-candidate status | FAIL | v1.0 is still marked as planned |
| REL-003 | Release | Valid v1.0 demo GIF | FAIL | The current file is placeholder text |
| REL-004 | Release | Canonical product version | PASS | `1.0.0-rc.1` is reused in project, Excel and PDF metadata |
| REL-005 | Release | Repeatable release process | FAIL | Clean install, pytest, RC, tag and rollback steps are missing |

## Blocker priority

### Completed in L-02 — Engineering trust

1. Replaced placeholder CI with dependency installation, compatibility checks,
   Ruff, pytest and release-readiness evidence.
2. Removed tracked bytecode and hardened `.gitignore`.
3. Added `app_core/version.py` as the canonical product-version source.
4. Reused version `1.0.0-rc.1` in project, Excel and PDF metadata.
5. Added focused Ruff rules (`E9`, `F`) without rewriting stable legacy code.

### Completed in L-03 — Security and privacy

1. Added an actionable private vulnerability-reporting process.
2. Documented uploaded-data flow, session state, temporary-file behavior,
   exports, deployment boundaries and external-processing consent.
3. Added a strict `pip-audit` vulnerability gate and weekly Dependabot updates.
4. Added a deterministic local-first privacy review to CI.
5. Added a visible privacy notice beside CSV upload.

### Completed in L-04A — Public product history

1. Updated README capabilities and onboarding to match the complete shipped
   navigation.
2. Documented Executive Overview, Business Insights, Analysis Assistant, Data
   Quality and Export & Share without implying external AI processing.
3. Added factual changelog sections for delivered milestones `0.3` through
   `0.6`.
4. Recorded that these milestones reached `main` on 2026-07-24 as part of
   `1.0.0-rc.1` and were not published as separate Git tags.

### P0 — Release process

1. Replace the short release guidance with a repeatable release procedure.
2. Keep v1.0 in `Planned` until all launch blockers are resolved.

### P1 — Release-document alignment

1. Freeze the v1.0 scope.
2. Align release notes, roadmap and Release Hub with the frozen scope.

### P1 — Launch assets and manual validation

1. Replace the placeholder demo GIF with a verified final-product recording.
2. Capture final screenshots.
3. Test a clean installation on the supported environment.
4. Review keyboard navigation, focus, contrast and zoom.
5. Measure behavior at the intended maximum CSV size.
6. Review export appearance.

## Recommended launch sequence

| Block | Outcome |
|---|---|
| L-02 | Complete — real CI, repository hygiene and version metadata |
| L-03 | Complete — security, privacy and dependency review |
| L-04 | In progress — README and changelog aligned; scope and release documents remain |
| L-05 | Manual UX, performance and clean-install validation |
| L-06 | Final assets, release candidate, tag and GitHub Release |

## Re-run the audit

From the project root:

```powershell
python scripts/release_readiness.py --root .
```

To return a failing process exit code while blockers remain:

```powershell
python scripts/release_readiness.py --root . --strict
```

## Scope note

The checker validates evidence stored in the repository. It does not claim to
replace manual UX, accessibility, performance, clean-install or security
review. A future `Ready` result is necessary for launch, but it is not the only
release decision input.
