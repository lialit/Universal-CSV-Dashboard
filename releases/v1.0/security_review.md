# L-03 — Security, Privacy and Dependency Review

**Review date:** 2026-07-24

**Release candidate:** `1.0.0-rc.1`

**Overall result:** PASS for the controls in L-03

## Automated validation

```text
Security and Privacy Review: PASS
Dependency vulnerability audit: no known vulnerabilities reported
Automated tests: 145 passed
Release readiness: 16 PASS · 0 WARN · 5 FAIL
```

The vulnerability result is a point-in-time scan of the dependency versions
resolved from the bounded requirements. It does not prove that the application
or its dependencies are free of unknown vulnerabilities.

## Privacy-control evidence

| Control | Result | Repository evidence |
|---|---|---|
| Upload parsing | PASS | CSV bytes are passed to pandas through `BytesIO` |
| Product-managed row-level temporary file | PASS | No runtime `NamedTemporaryFile` or `TemporaryDirectory` path |
| External runtime client | PASS | No direct HTTP or external AI client in runtime imports or direct requirements |
| Client error disclosure | PASS | `.streamlit/config.toml` sets `showErrorDetails = "none"` |
| Saved project data | PASS | Project JSON stores configuration and schema metadata, not raw rows |
| Export boundary | PASS | PDF and Excel behavior and row-level Excel sensitivity are documented |
| External-processing consent | PASS | Current release has no external processing; future use must be explicit and opt-in |
| Private vulnerability reporting | PASS | GitHub private security advisory path and response process documented |

## Dependency controls

| Control | Result |
|---|---|
| Direct requirements use compatible lower and upper bounds | PASS |
| Installed package compatibility checked with `pip check` | PASS |
| Known vulnerabilities checked with strict `pip-audit` | PASS |
| Python dependency updates proposed weekly by Dependabot | CONFIGURED |
| GitHub Actions updates proposed monthly by Dependabot | CONFIGURED |

The automated scan command is:

```powershell
python -m pip_audit -r requirements.txt --strict
```

## Security-reporting path

Reports should use GitHub's private advisory form:

<https://github.com/lialit/Universal-CSV-Dashboard/security/advisories/new>

Reports must use synthetic reproduction data and must not contain real client
CSV files, credentials or personal information.

## Residual risks

The following boundaries remain outside the L-03 automated guarantees:

- behavior of the browser, operating system and Python runtime caches;
- swap, proxy, memory and logging behavior on a hosted deployment;
- confidentiality after a PDF, Excel or JSON artifact is downloaded;
- unknown or newly disclosed dependency vulnerabilities;
- legal or regulatory compliance for a specific organization;
- malicious files outside the documented supported CSV scope.

These risks are documented rather than hidden. Users remain responsible for
running the product in a trusted environment and reviewing exports before
sharing.
