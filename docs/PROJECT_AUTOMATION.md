# GitHub Project automation

The repository workflow at `.github/workflows/project-automation.yml` keeps Issues and pull requests synchronized with the **Universal CSV Dashboard Roadmap** project.

## What it does

- Adds newly opened, reopened, or transferred Issues to the project.
- Adds opened, reopened, synchronized, ready-for-review, or closed pull requests.
- Sets the custom `Workflow` project field automatically:
  - new or reopened Issue → `Backlog`
  - closed Issue → `Done`
  - opened, reopened, or updated pull request → `In progress`
  - pull request marked ready for review → `Review`
  - closed pull request → `Done`
- Supports a manual run for repairing or resynchronizing a specific Issue or pull request by URL.

## Required repository secret

GitHub's repository-scoped `GITHUB_TOKEN` cannot write to a user-level Project. Create a personal access token and store it as a repository Actions secret named:

```text
PROJECT_TOKEN
```

For a classic personal access token, grant:

```text
repo
project
```

Treat the token as a credential. Never commit it, paste it into an Issue, or expose it in workflow logs.

## Add the secret

1. Open the repository on GitHub.
2. Go to **Settings → Secrets and variables → Actions**.
3. Select **New repository secret**.
4. Set the name to `PROJECT_TOKEN`.
5. Paste the token value and save it.

## Test the workflow

Open **Actions → Project automation → Run workflow** and use:

```text
item_url: https://github.com/lialit/Universal-CSV-Dashboard/issues/14
workflow_state: Ready
```

A successful run should leave Issue #14 in the `Ready` column of the `v1.1 Delivery` view.

## Troubleshooting

- **Resource not accessible / permission denied:** confirm `PROJECT_TOKEN` exists and has project write access.
- **Project field not found:** confirm the project contains a single-select field named exactly `Workflow`.
- **Workflow option not found:** confirm these options exist exactly: `Backlog`, `Ready`, `In progress`, `Review`, `Done`.
- **Item not found after adding:** rerun the workflow manually; the workflow already retries project indexing five times.
