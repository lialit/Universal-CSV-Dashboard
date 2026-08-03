# GitHub Project Automation Validation

Use this checklist after changing `.github/workflows/project-automation.yml`, the Project fields, or label mappings.

## Static validation

Run from the repository root:

```bash
python scripts/validate_project_automation.py
```

Expected result:

```text
Project automation configuration is valid.
```

## Safe manual smoke test

Open **Actions → Project automation → Run workflow** and use an existing roadmap item:

```text
item_url: https://github.com/lialit/Universal-CSV-Dashboard/issues/14
workflow_state: Ready
```

The run should:

1. validate `PROJECT_TOKEN`;
2. accept only URLs from `lialit/Universal-CSV-Dashboard`;
3. detect that Issue #14 already exists in Project #2;
4. set `Workflow` to `Ready`;
5. copy mapped `priority:*`, `release:*`, and `area:*` labels into Project fields;
6. finish successfully without creating a duplicate card.

## Event validation

For a disposable test Issue:

1. Open the Issue — it should be added to the Project with `Workflow = Backlog`.
2. Add labels such as `priority: P2`, `release: v1.2`, and `area: docs` — matching Project fields should update.
3. Remove and replace one mapped label — the replacement value should synchronize.
4. Close the Issue — `Workflow` should become `Done`.
5. Reopen the Issue — `Workflow` should return to `Backlog`.

## Expected safeguards

The workflow must fail clearly when:

- `PROJECT_TOKEN` is missing;
- the URL is not a GitHub Issue or pull request URL;
- the URL belongs to another repository;
- Project #2, a required field, or a mapped option cannot be resolved.

Removing a mapped label does not clear the corresponding Project field automatically. The workflow leaves the current field value unchanged until another mapped label is applied. This avoids accidental data loss when labels are edited temporarily.
