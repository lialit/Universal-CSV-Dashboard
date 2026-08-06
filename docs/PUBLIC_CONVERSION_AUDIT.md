# Public README and Release Conversion Audit

This document records the GH-06D review of the path from first repository visit to a useful next action.

## Conversion goal

The public repository should help an external visitor move quickly from interest to one of four supported actions:

1. run the product locally;
2. inspect the latest stable release;
3. get help through the correct route;
4. contribute or report a reproducible problem.

The repository does not use a temporary hosted demo as a primary call to action. Local installation remains the supported product path until a maintained public deployment exists.

## Audit result

| Visitor question | Evidence or route | Status |
|---|---|---|
| What does the product do? | Product promise, hero, capability table, and demo | Passed |
| Can I trust the project? | CI, documentation, release, Python, licence, and privacy badges | Passed |
| How do I start? | Primary `Run locally` route and `Quick start` section | Passed after GH-06D update |
| Where is the stable version? | Primary `Stable release` route and release badge | Passed after GH-06D update |
| Where do I ask for help? | Primary `Get support` route and `SUPPORT.md` | Passed after GH-06D update |
| Where do I report a problem? | Support guide and structured issue chooser | Passed |
| How do I contribute? | `CONTRIBUTING.md`, PR template, and contributor validation guide | Passed |
| Is there an online demo? | No unsupported deployment claim is made | Passed |

## First-screen rules

The area before the hero image should contain:

- the product identity and outcome;
- a short evidence-linked badge row;
- one primary local-run route;
- one stable-release route;
- one support route;
- compact navigation for deeper reading.

Do not add multiple competing commercial, social, or vanity calls to action. The first screen should remain understandable without scrolling through the complete feature list.

## Release conversion rules

- `releases/latest` must resolve to a published stable release.
- The README must not point first-time users to a prerelease.
- Installation documentation should default to the current repository state, while the stable release page remains available for reproducible versioned installation.
- Release notes must include scope, installation, validation, limitations, and security reporting.
- Temporary smoke drafts and deployments must not become public CTAs.

## Support conversion rules

- General help routes must lead to `SUPPORT.md` before inviting an unstructured issue.
- Vulnerability reports must remain private.
- Public examples must be synthetic or redacted.
- Professional customisation must remain separate from open-source bug support.
- No response-time or delivery guarantee should be implied.

## Regression checklist

Review the public path:

1. before every stable release;
2. after changing README navigation or hero content;
3. after publishing or removing a public demo;
4. after changing support or security routes;
5. after changing the latest stable release;
6. when any first-screen link or badge becomes stale.

A visitor should reach local setup, the stable release, or support in one click from the first screen.