## Summary

Describe the user or developer outcome.

## What changed

## Why

## Validation

List the exact commands and manual checks performed, including outcomes. Explain
any skipped check and why it was not applicable or could not run.

```text
python -m ruff check . —
python -m pytest -q —
python scripts/check_markdown_links.py —
```

## Privacy, security and exports

Describe any effect on uploaded data, session state, external processing,
saved projects, Excel or PDF contents. Write `No change` when applicable.

## Screenshots

Required for visible UI changes. Use synthetic or non-confidential data.

## Limitations and follow-up

## Checklist

- [ ] The change is focused and contains no unrelated files.
- [ ] Exact validation commands and outcomes are recorded above.
- [ ] Tests pass and behavior changes have coverage.
- [ ] Public documentation is updated.
- [ ] Privacy and export implications were reviewed.
- [ ] Screenshots are included for UI changes.
- [ ] No secrets, private datasets or generated local artifacts are committed.
