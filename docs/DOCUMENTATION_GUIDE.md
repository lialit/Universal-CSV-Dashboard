# Documentation Guide

Universal CSV Dashboard uses a small set of canonical entry points so readers do not need to compare several overlapping guides.

## Canonical entry points

| Reader goal | Canonical document |
|---|---|
| Understand the product | `README.md` |
| Install and take the first tour | `START_HERE.md` |
| Contribute code or documentation | `CONTRIBUTING.md` |
| Understand product scope | `PRODUCT.md` |
| Review delivery direction | `ROADMAP.md` |
| Browse detailed documentation | `docs/README.md` |
| Operate releases | `docs/10_RELEASE_PROCESS.md` and `docs/RELEASE_WORKFLOW_OPERATIONS.md` |

## Avoiding duplication

When information belongs to another canonical document:

1. keep only a short contextual summary;
2. link to the canonical source;
3. do not copy long command sequences, validation checklists or policy text;
4. update all affected links when a document is renamed.

Installation commands belong in `START_HERE.md`. Contributor-only dependencies and validation commands belong in `CONTRIBUTING.md`. README should retain only the shortest usable quick start.

## Adding a document

Before adding a new Markdown file:

1. confirm that the topic does not already have a canonical page;
2. choose a descriptive, stable filename;
3. add the document to `docs/README.md`;
4. link it from another root document only when it is a common entry point;
5. use relative links so documentation works on branches and release tags.

## Maintenance expectations

Documentation changes should accompany changes to public behavior, supported environments, validation commands, security boundaries or release operations.

Use synthetic examples. Do not include private CSV data, credentials, secrets, internal client information or screenshots containing confidential values.