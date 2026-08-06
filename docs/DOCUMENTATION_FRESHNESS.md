# Documentation Freshness

Documentation is reviewed against the current stable release, supported runtime, public product behavior and repository workflows.

## Audit scope

A freshness review should check:

- version and release-status statements;
- supported Python and CSV-size boundaries;
- page names and product navigation;
- install, test and validation commands;
- security, privacy and export boundaries;
- release and GitHub automation procedures;
- links to files, directories, screenshots and release assets.

## Current audit findings

The GH-05B review identified one stale public statement in `README.md`: the roadmap still describes version 1.0 as being in release-candidate validation and refers to `1.0.0-rc.1` as the current bundled milestone. The stable `v1.0.0` release is now the canonical public version. This wording must be corrected before GH-05B is closed.

## Automated protection

`scripts/check_markdown_links.py` validates repository-local Markdown and HTML links. The `Documentation links` workflow runs this check for documentation-related pull requests and pushes to `main`.

The checker intentionally does not request external websites. External-link availability can be transient and should be reviewed manually when a linked service or dependency changes.

## Maintenance rule

When a pull request changes public behavior, supported environments, release status, navigation, security boundaries or validation commands, update the canonical documentation in the same pull request.

Before a stable release:

1. run the local Markdown link checker;
2. review the root documentation entry points;
3. search for the previous release and release-candidate identifiers;
4. verify screenshots and demo assets;
5. record unresolved documentation limitations explicitly.
