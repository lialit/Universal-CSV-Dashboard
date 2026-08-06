# Public Repository Profile

This document records the intended public GitHub profile for Universal CSV Dashboard. Repository-level settings are not stored in the Git tree, so maintainers should review this checklist after major releases or repository transfers.

## About section

Use the following public metadata:

- **Description:** `Local-first Streamlit app that turns CSV files into clear business metrics, insights, data-quality checks, and traceable reports.`
- **Homepage:** leave empty until a stable public demo or product landing page exists. Do not link a temporary deployment.
- **Topics:** `csv`, `dashboard`, `data-analysis`, `business-intelligence`, `streamlit`, `python`, `data-visualization`, `data-quality`, `analytics`, `local-first`.

The description should explain the product outcome rather than repeat the repository name. Topics should remain specific enough to support GitHub discovery and should not claim capabilities the stable release does not provide.

## Repository features

Recommended public settings:

| Setting | Expected value | Reason |
|---|---|---|
| Issues | Enabled | Structured issue forms are maintained |
| Projects | Enabled | Public roadmap and triage use GitHub Projects |
| Discussions | Disabled for now | No maintained discussion workflow yet |
| Wiki | Disabled | Canonical documentation lives in the repository |
| Releases | Enabled | Stable and prerelease artifacts are published here |
| Squash merging | Enabled | Matches the documented contribution workflow |
| Merge commits | Disabled | Avoids multiple competing merge histories |
| Rebase merging | Disabled | Keeps the public history consistent with squash merges |
| Automatically delete head branches | Enabled | Matches the short-lived branch workflow |
| Auto-merge | Optional | Enable only when branch protection and review policy are stable |

## Public trust signals

The repository should visibly expose:

- a detected MIT license;
- a stable release marked as latest;
- passing CI and documentation-link checks;
- supported Python version;
- security reporting instructions;
- contributor guidance and structured issue forms;
- current screenshots and a non-confidential demo;
- the validated 25 MB v1.0 CSV boundary and local-first privacy model.

Badges must link to their underlying evidence rather than serve as decoration. Avoid badges for vanity metrics or services that are not part of the supported workflow.

## Stable release visibility

The stable `v1.0.0` release should remain the GitHub **Latest** release. Prereleases such as `v1.0.0-rc.1` must remain marked as prerelease and should not replace the stable release in public onboarding text.

Smoke-test drafts must be deleted after validation and must never be published.

## Review cadence

Review this profile:

1. before each stable release;
2. after changing the product homepage or public demo;
3. after enabling a new community feature;
4. after changing merge strategy or branch protection;
5. when the supported product boundary or privacy model changes.

Record any intentional deviation in this document so repository settings and contributor documentation do not silently diverge.