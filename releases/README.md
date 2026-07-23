# Release Hub

This directory contains planning notes, release criteria and published notes for
Universal CSV Dashboard versions.

> **Important:** A version directory does not mean that the version has been
> released. Always check the status at the top of its `release_notes.md`.

## Release sequence

| Version | Name | Outcome | Status |
|---|---|---|---|
| [`v0.3`](v0.3/release_notes.md) | **Understand** | Stronger automatic interpretation of structure and quality | Next |
| [`v0.4`](v0.4/release_notes.md) | **Explain** | Evidence-based observations with visible limitations | Planned |
| [`v0.5`](v0.5/release_notes.md) | **Share** | Saved work and responsible report exports | Planned |
| [`v0.6`](v0.6/release_notes.md) | **Assist** | Optional guided analysis with privacy controls | Exploratory |
| [`v1.0`](v1.0/release_notes.md) | **Launch** | Stable, documented and dependable public product | Planned |

The currently available product foundation is represented by the `0.1` and
`0.2` sections of [`CHANGELOG.md`](../CHANGELOG.md).

## Source-of-truth rules

These files have different roles:

| File | Role |
|---|---|
| [`ROADMAP.md`](../ROADMAP.md) | Product direction and priority |
| [`CHANGELOG.md`](../CHANGELOG.md) | Shipped, notable changes |
| `releases/<version>/release_notes.md` | Scope, criteria and final notes for one version |
| [`RELEASE_TEMPLATE.md`](RELEASE_TEMPLATE.md) | Structure for future versions |

When a capability ships:

1. update the version release notes;
2. move the relevant item into a versioned `CHANGELOG.md` section;
3. add the release date;
4. verify that `ROADMAP.md` reflects the new current stage;
5. create the Git tag and GitHub Release only after validation is complete.

## Status definitions

| Status | Meaning |
|---|---|
| **Next** | The next intended product stage; scope may still change |
| **Planned** | Direction is accepted, but implementation is not current |
| **Exploratory** | The value, safety or implementation approach must be validated |
| **Release candidate** | Scope is frozen and final validation is underway |
| **Released** | The version has a date, tag and published release notes |

## Release standards

Every release should:

- describe user-visible outcomes rather than only implementation details;
- distinguish delivered work from planned work;
- include known limitations;
- preserve relevant privacy and quality context;
- pass automated tests;
- verify installation from a clean environment;
- update public documentation;
- avoid unsupported performance or compatibility claims.

## Assets

Version directories may contain:

- `release_notes.md`;
- verified screenshots;
- a short demo GIF;
- migration instructions;
- downloadable example output.

Do not add placeholder media to published release notes. Assets should represent
the version being released.

