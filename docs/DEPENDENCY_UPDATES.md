# Automated Dependency Updates

Universal CSV Dashboard uses Dependabot to keep Python packages and GitHub Actions current without bypassing repository protections.

## Schedule

- Python dependencies: every Monday at 08:00 Europe/Kyiv.
- GitHub Actions: monthly on Monday at 08:30 Europe/Kyiv.

## Update policy

Minor and patch updates are grouped by ecosystem to reduce pull request noise. Major updates remain separate so compatibility, migration notes, and user-facing impact can be reviewed individually.

Dependabot pull requests:

- target `main`;
- are assigned to `lialit`;
- receive `dependencies`, area, and priority labels;
- must pass the protected `Release readiness` check;
- are rebased automatically when needed;
- are not merged automatically.

## Review checklist

Before merging a dependency update:

1. Read the upstream release notes, especially for major versions.
2. Confirm the dependency remains inside the supported version range.
3. Wait for the complete cross-platform CI matrix.
4. Review security-audit output.
5. Smoke-test affected application features when the update touches Streamlit, pandas, Plotly, exports, or file parsing.
6. Use squash merge and delete the Dependabot branch after merge.

## Security updates

Security-related Dependabot pull requests still follow branch protection and required CI. Urgent patches may be reviewed and merged ahead of the regular weekly batch, but required checks must not be bypassed.
