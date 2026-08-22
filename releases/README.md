# Release Hub

This directory contains planning notes, release criteria and published notes for
Universal CSV Dashboard versions.

> **Important:** A version directory does not mean that the version has been
> released. Always check the status at the top of its `release_notes.md`.

## Release sequence

| Version | Name | Outcome | Status |
|---|---|---|---|
| [`v0.3`](v0.3/release_notes.md) | **Understand** | Transparent quality scoring and executive interpretation | Delivered to `main`; untagged |
| [`v0.4`](v0.4/release_notes.md) | **Explain** | Evidence-based observations with visible limitations | Delivered to `main`; untagged |
| [`v0.5`](v0.5/release_notes.md) | **Share** | Saved work and responsible report exports | Delivered to `main`; untagged |
| [`v0.6`](v0.6/release_notes.md) | **Assist** | Local deterministic guidance with privacy controls | Delivered to `main`; untagged |
| [`v1.0`](v1.0/release_notes.md) | **Launch** | Stable, documented and dependable public product | Released |
| [`v1.1`](v1.1/release_notes.md) | **Polish & Adoption** | Guided onboarding, live demo, performance/UX/export confidence and public documentation | In progress |

The stable `1.0.0` release includes the delivered `0.1–0.6`
capabilities recorded in [`CHANGELOG.md`](../CHANGELOG.md). Versions
`0.3–0.6` were development milestones and were not published as standalone
Git tags.

v1.1 is the current product stage. Its working release notes and canonical
screenshot set live under [`v1.1/`](v1.1/). The release remains unpublished
until beta validation and the final release-readiness gate are complete.

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

The executable validation, publication and rollback checklist is maintained in
[`docs/10_RELEASE_PROCESS.md`](../docs/10_RELEASE_PROCESS.md).

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
