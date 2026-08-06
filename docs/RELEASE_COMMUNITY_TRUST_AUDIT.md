# Release and Community Trust Audit

This document records the GH-06C review of the public release and community experience for Universal CSV Dashboard.

## Audit result

| Area | Evidence | Status |
|---|---|---|
| Latest stable release | GitHub `releases/latest` resolves to published, non-prerelease `v1.0.0` | Passed |
| Stable release description | Release notes include product scope, installation, validation, limitations, and security route | Passed |
| License | MIT license is detected by GitHub | Passed |
| README trust signals | CI, documentation links, release, Python, license, and privacy claims link to evidence | Passed |
| Contribution route | `CONTRIBUTING.md` and PR template define workflow and validation evidence | Passed |
| Issue route | Structured issue forms and issue chooser separate bugs, features, documentation, and security | Passed |
| Security route | `.github/SECURITY.md` directs vulnerabilities to private advisories | Passed after GH-06C update |
| Supported versions | Security policy follows the latest stable `1.x` release and `main` | Passed after GH-06C update |
| Support expectations | `SUPPORT.md` separates bugs, usage help, features, security, and professional customisation | Passed after GH-06C update |
| Community conduct | Code of Conduct defines expected behaviour, reporting scope, and enforcement | Passed after GH-06C update |
| Privacy boundary | Public reports require synthetic or redacted examples | Passed |
| Community profile | GitHub reports a complete community profile | Passed |

## External visitor path

A visitor should be able to:

1. understand the product and trust signals from `README.md`;
2. install it through `START_HERE.md`;
3. identify the latest stable release through GitHub Releases;
4. choose support through `SUPPORT.md`;
5. report ordinary defects through structured issue forms;
6. report vulnerabilities privately through `.github/SECURITY.md`;
7. understand participation expectations through `.github/CODE_OF_CONDUCT.md`;
8. contribute through `CONTRIBUTING.md` and the PR template.

No step should require access to maintainer-only project notes or private communication.

## Release trust rules

- The GitHub **Latest** release must be a published stable release, not a prerelease or smoke draft.
- Release notes must state installation steps, supported boundary, validation evidence, and important limitations.
- README version claims must not move ahead of the latest stable release.
- Smoke drafts must be deleted after validation.
- Security support must be updated when the latest stable major or maintained release line changes.

## Community trust rules

- Public help routes must not invite confidential datasets or credentials.
- Security details must never be redirected to public issues.
- Support language must avoid guaranteed response times or delivery commitments.
- Professional customisation must remain separate from open-source defect triage.
- Conduct enforcement must protect participants without promising a process the maintainer cannot operate.

## Regression checklist

Review this audit:

1. before every stable release;
2. after changing supported versions;
3. after changing issue, support, or security routes;
4. after enabling Discussions or another community feature;
5. after changing the licence, privacy model, or public deployment model;
6. whenever GitHub's community profile reports a missing file or lower health score.
