# BP-01 Integration Guide

This pack is structured to merge directly into the
`UniversalCSVDashboard` repository.

## Add the files

Copy these folders into the repository root:

```text
assets/
docs/branding/
marketing/
```

Then replace the root `README.md` with the README from this pack.

The pack does not modify application code. It also does not delete or replace
existing product documents such as `PRODUCT.md`, `ROADMAP.md`,
`CONTRIBUTING.md` or `LICENSE`.

## Recommended repository checks

```bash
git status
git diff -- README.md docs/branding/BRAND_BOOK.md
```

Preview `README.md` in PyCharm or on GitHub before committing.

## Suggested commit

```bash
git add README.md assets docs/branding marketing
git commit -m "Add BP-01 brand system and refresh README"
```

## Optional app integration

Use `assets/brand/favicon.svg` or `assets/brand/favicon-64.png` as the Streamlit
page icon. Keep the horizontal logo for README and documentation; use the
compact mark inside the application.
