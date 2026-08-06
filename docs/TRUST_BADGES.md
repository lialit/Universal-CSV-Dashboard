# README Trust Badges

The README badge row is a compact evidence index, not a collection of promotional decorations. Every badge must point to a maintained source that lets a reader verify the claim.

## Approved badges

| Badge | Evidence source | Update rule |
|---|---|---|
| CI | `.github/workflows/ci.yml` workflow runs | Keep only while CI runs on `main` and pull requests |
| Documentation links | `.github/workflows/documentation-links.yml` workflow runs | Keep only while repository-local Markdown links are checked automatically |
| Latest release | GitHub Releases latest stable endpoint | Must resolve to a published non-prerelease version |
| Python | `START_HERE.md`, CI configuration, and the stable release instructions | Update when the minimum supported Python version changes |
| MIT license | Repository `LICENSE` file and GitHub license detection | Remove or change immediately if the project license changes |
| Local-first | `docs/12_SECURITY_PRIVACY.md` | Keep only while CSV analysis remains local by default and external transfer is not required |

## Presentation rules

- Place the badges below the product promise and before navigation links.
- Keep the row short enough to scan as one trust summary.
- Link workflow badges to their Actions pages, not only to badge images.
- Link the release badge to the latest stable release.
- Link static claims to the canonical repository document that explains the boundary.
- Do not add download counts, stars, social metrics, coverage estimates, or third-party quality scores unless they become maintained decision evidence.
- Avoid badges for temporary deployments or services outside the supported workflow.

## Review checklist

Review the badge row:

1. before each stable release;
2. after renaming or replacing a workflow;
3. after changing the supported Python version;
4. after changing the license or privacy model;
5. whenever a badge displays `unknown`, `no status`, or a stale release.

A broken or unsupported badge should be removed in the same pull request that invalidates its evidence source.