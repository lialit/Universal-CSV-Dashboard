# Branch protection for `main`

The repository uses a protected `main` branch so release-critical changes are reviewed through a pull request and pass CI before merging.

## Policy

- Changes to `main` must go through a pull request.
- The branch must be up to date before merging.
- The required check is `Release readiness`.
- The required check aggregates lint, configuration validation, the Linux/Windows test matrix, dependency auditing, privacy review, and release readiness checks.
- All review conversations must be resolved before merge.
- Force pushes are blocked.
- Branch deletion is blocked.
- The policy applies to repository administrators.
- No external approval is required because the repository currently has one maintainer.

## Apply the policy

From the repository root in Windows PowerShell:

```powershell
git pull
powershell -ExecutionPolicy Bypass -File .\scripts\sync_branch_protection.ps1
```

The authenticated GitHub account must have repository administration permission. If GitHub CLI reports insufficient permissions, refresh authentication with an appropriate token before retrying.

## Verify in GitHub

Open:

`Settings → Branches → Branch protection rules → main`

Confirm that:

- Require a pull request before merging is enabled.
- Require status checks to pass before merging is enabled.
- Require branches to be up to date before merging is enabled.
- `Release readiness` is required.
- Require conversation resolution before merging is enabled.
- Do not allow bypassing the settings is enabled for administrators.
- Force pushes and branch deletion are not allowed.

## Working after protection is enabled

Create changes on a branch instead of committing directly to `main`:

```powershell
git switch main
git pull
git switch -c feature/example-change
```

Push the branch and open a pull request:

```powershell
git push -u origin feature/example-change
gh pr create --base main --fill
```

Merge only after `Release readiness` succeeds and all conversations are resolved.

## Why only one required check?

`Release readiness` depends on all mandatory CI jobs. Requiring this stable aggregate check keeps branch protection reliable even if matrix job labels or supported Python versions change later.
