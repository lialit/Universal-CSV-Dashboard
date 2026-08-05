# Pull Request Labeler Regression Test

This temporary documentation change validates the path-based pull request labeler introduced in GH-04D.

Expected automatic labels:

- `area: docs`
- `area: github`

The pull request should remain open only long enough to confirm that the `Pull request labeler` workflow succeeds and applies the expected labels. After validation, merge the pull request so this record remains part of the repository history.

A follow-up synchronization run validates the corrected Project field option resolution from PR #31.
