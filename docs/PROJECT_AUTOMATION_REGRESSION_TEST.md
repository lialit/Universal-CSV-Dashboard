# Project Automation Regression Test

This document records a regression test for the GitHub Project automation after fixing pull request handling.

## Scope

The test verifies that opening a pull request from a short-lived branch:

- adds the pull request to the GitHub Project;
- sets the `Workflow` field to `In progress`;
- completes the `Project automation / Sync roadmap item` check successfully;
- preserves the existing protected-branch CI workflow.

## Success criteria

- [ ] Project automation is green.
- [ ] All CI checks are green.
- [ ] The pull request is added to the roadmap Project.
- [ ] The pull request can be squash-merged after required checks pass.
- [ ] The source branch is deleted after merge.
