# Pull Request Labeling

Universal CSV Dashboard uses two complementary label types for pull requests.

## Automatic area labels

The `Pull request labeler` workflow applies labels from changed file paths using `.github/labeler.yml`.

Examples:

- `.github/**` → `area: github`
- Markdown and `docs/**` → `area: docs`
- `app.py` and `pages/**` → `area: dashboard`
- `tests/**` → `testing`
- dependency manifests → `dependencies`

Automatic labels are synchronized when the pull request changes, so stale path-based labels are removed.

## Manual change-type labels

Every product or maintenance pull request should receive the most accurate semantic label before merge:

- `feature` — a new user-facing capability;
- `enhancement` — an improvement to existing behavior;
- `bug` — a defect fix;
- `performance` — speed, memory, caching, or scalability work;
- `refactor` — internal restructuring without intended behavior change;
- `documentation` — documentation-only work;
- `testing` — tests or validation work;
- `dependencies` — dependency or compatibility updates.

Path-based automation intentionally does not guess these semantic labels.

## Generated release notes

`.github/release.yml` maps the labels above into stable release-note sections. Pull requests without a matching semantic or infrastructure label fall back to `Other changes`.

Before merging a pull request, confirm that it has:

1. at least one appropriate area label;
2. one accurate change-type label when applicable;
3. `skip-changelog` only when the change should not appear in generated release notes.
