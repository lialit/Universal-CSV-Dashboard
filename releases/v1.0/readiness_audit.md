# v1.0 Release Readiness Audit

**Audit date:** 2026-07-24

**Baseline commit:** `68ec6cf`

**Latest checkpoint:** L-02 — Engineering Trust & CI

**Overall status:** **Not ready**

## Result

| Status | Count |
|---|---:|
| PASS | 13 |
| WARN | 0 |
| FAIL | 6 |

The full automated test suite, including the readiness checker tests, passes:

```text
138 passed
```

This means the implemented product logic is stable under the current automated
tests. It does **not** mean the repository is ready for a public `v1.0` release.
The remaining failures are release engineering, repository hygiene,
documentation, security-process and launch-asset blockers.

## Automated findings

| ID | Category | Check | Status | Evidence |
|---|---|---|---|---|
| DOC-001 | Documentation | Required public documents | PASS | README, onboarding, changelog, contribution, license and security files exist |
| APP-001 | Product | Core application structure | PASS | All launch-critical pages and analytical modules exist |
| DATA-001 | Product | Safe representative sample | PASS | `sample_sales.csv` contains date, region and sales |
| DATA-002 | Product | Varied examples | PASS | Five example CSV files are present |
| TEST-001 | Engineering | Automated test structure | PASS | Seventeen test modules are present after L-02 |
| CI-001 | Engineering | CI installs dependencies | PASS | GitHub Actions installs the bounded requirements |
| CI-002 | Engineering | CI runs pytest | PASS | GitHub Actions executes the complete test suite |
| CI-003 | Engineering | CI runs static checks | PASS | Ruff checks syntax-level and Pyflakes failures |
| DEP-001 | Engineering | Dependencies bounded | PASS | Requirements have intentional lower and upper bounds |
| DEP-002 | Engineering | Python support defined | PASS | README and CI reference Python 3.11 |
| REPO-001 | Repository | Generated artifacts untracked | PASS | Tracked `.pyc` files were removed and ignore rules hardened |
| SEC-001 | Security | No obvious tracked secrets | PASS | No credential-like tracked values detected |
| SEC-002 | Security | Actionable security policy | FAIL | No detailed private reporting path or handling process |
| DOC-002 | Documentation | README matches shipped UI | FAIL | Analysis Assistant and Export & Share are absent |
| REL-001 | Release | Changelog covers 0.3–0.6 | FAIL | Delivered milestones are missing from the changelog |
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

### P0 — Security and release process

1. Expand the security policy with a private reporting path.
2. Replace the six-line release note with a repeatable release procedure.
3. Keep v1.0 in `Planned` until all launch blockers are resolved.

### P1 — Public documentation

1. Update README to match the shipped pages and 0.3–0.6 capabilities.
2. Add accurate changelog entries for Understand, Explain, Share and Assist.
3. Align release notes and roadmap only after scope is frozen.

### P1 — Launch assets and manual validation

1. Replace the placeholder demo GIF with a verified final-product recording.
2. Capture final screenshots.
3. Test a clean installation on the supported environment.
4. Review keyboard navigation, focus, contrast and zoom.
5. Measure behavior at the intended maximum CSV size.
6. Review dependency vulnerabilities and export appearance.

## Recommended launch sequence

| Block | Outcome |
|---|---|
| L-02 | Complete — real CI, repository hygiene and version metadata |
| L-03 | Security, privacy and dependency review |
| L-04 | README, changelog and release-document alignment |
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
