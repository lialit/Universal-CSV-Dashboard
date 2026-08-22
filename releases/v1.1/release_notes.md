# Universal CSV Dashboard v1.1 — Polish & Adoption

**Status:** In progress / release candidate preparation

v1.1 focuses on making the stable v1.0 product easier to discover, easier to try, faster to understand and safer to share.

## User-visible outcomes

- Guided **Start Here** onboarding with two clear paths: bundled synthetic demo data or the user's own CSV.
- Bundled demo data that opens directly into Executive Overview without requiring a file upload.
- Repeatable performance confidence coverage for small, medium and supported-boundary CSV profiles.
- Improved responsive behavior and actionable empty states across the main dashboard flow.
- Hardened Excel and PDF exports with safer deterministic filenames, path stripping and edge-case regression coverage.
- Public Streamlit Community Cloud demo:
  https://universal-csv-dashboard-ujqkgrohd7vy4zexcxkuqg.streamlit.app/
- Refreshed public documentation and screenshots representing the actual v1.1 workflow.

## Supported boundary

The validated CSV upload boundary remains **25 MB per CSV**. CSV processing and analysis are in-memory, so wide or complex datasets may require substantially more RAM than their file size.

The public Streamlit deployment uses the same 25 MB server upload limit.

## Privacy and data handling

The product remains local-first. The public demo is a convenience layer for trying the product; users who need maximum control over sensitive data should run the application locally.

The bundled demo data is synthetic. No customer-derived or confidential dataset is included in the repository.

The application does not require API keys or an external AI service for its analytical assistant. The assistant is deterministic and local to the running application session.

## v1.1 screenshot set

Canonical screenshots are stored in `releases/v1.1/screenshots/`:

1. Start Here
2. Executive Overview
3. Business Insights
4. Analysis Assistant
5. Data Quality
6. Export & Share

All public screenshots must use the bundled synthetic demo dataset and must not contain private paths, credentials or customer data.

## Validation before release

v1.1 is ready for release only after:

- full CI is green on the final release candidate;
- Documentation links is green;
- clean-environment setup guidance is verified;
- the public live demo opens in a clean browser session and the bundled demo flow works;
- representative Excel and PDF exports are opened and visually checked;
- the six v1.1 screenshots match the final interface;
- beta feedback is triaged with no unresolved release blocker;
- README, START_HERE, ROADMAP, release notes, privacy and export documentation agree on supported behavior and limits.

## Known limitations

- CSV analysis is intentionally bounded to the documented 25 MB workflow.
- The application is a first-pass business-understanding tool, not a spreadsheet editor, data warehouse, statistical modeling suite or autonomous decision system.
- Insight interpretation is rule-based and evidence-linked; it does not establish causation.
- Public hosting changes the deployment context but does not replace the local-first usage option.

## Release gate

The final v1.1 tag and GitHub Release are created only after beta validation and the v1.1 release-readiness gate are complete.
