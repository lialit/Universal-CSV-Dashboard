# Pull Request Workflow Validation

This document records the first end-to-end validation of the protected `main` branch workflow.

## Expected workflow

1. Create a short-lived branch from `main`.
2. Make a focused change.
3. Open a pull request targeting `main`.
4. Wait for the required `Release readiness` check.
5. Confirm unresolved conversations and an outdated branch block merging when applicable.
6. Merge only after all required checks pass.
7. Delete the source branch after merge.

## Validation scope

The validation change is documentation-only and does not affect application behavior.

## Success criteria

- [ ] Direct changes to `main` are not used.
- [ ] The pull request template is applied.
- [ ] CI runs for the pull request.
- [ ] `Release readiness` is reported as a required check.
- [ ] The pull request becomes mergeable only after required checks pass.
- [ ] The source branch can be deleted after merge.

## Result

Complete the checklist in the pull request before merging. After a successful merge, this file serves as the repository's branch-protection smoke-test record.
