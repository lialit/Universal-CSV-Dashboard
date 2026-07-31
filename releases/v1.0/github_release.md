# Universal CSV Dashboard 1.0.0-rc.1

Universal CSV Dashboard turns a CSV file into a transparent first-pass
business analysis: editable field detection, executive metrics, evidence-linked
insights, data-quality context, local guided explanations and responsible
exports.

This is a **release candidate** for validation. It is not the final `1.0.0`
release.

## Highlights

- local-first CSV analysis without an external AI or analytics service;
- automatic, editable date, metric and category suggestions;
- Executive Overview with verified facts and rule-based interpretations;
- Business Insights with evidence, confidence and visible limitations;
- deterministic Analysis Assistant with inspectable calculations;
- transparent Data Quality Score;
- saved project state plus branded Excel and executive PDF reports;
- Light, Corporate and Dark report themes.

## Validated boundary

The v1.0 candidate supports CSV uploads up to **25 MB**. The Windows Python
3.11 reference check processed a synthetic 24 MB file containing 738,965 rows
and 6 columns. Core parsing, field detection and quality analysis completed in
4.07 seconds. After the first calculation, the reviewed analytical pages
reopened immediately in the observed Streamlit session.

## Install

```bash
git clone https://github.com/lialit/Universal-CSV-Dashboard.git
cd Universal-CSV-Dashboard
python -m venv .venv
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

See the
[`START_HERE.md`](https://github.com/lialit/Universal-CSV-Dashboard/blob/v1.0.0-rc.1/START_HERE.md)
guide for the complete Windows, macOS and Linux setup flow.

## Validation

- 165 automated tests passed;
- GitHub Actions CI passed;
- Security and Privacy Review passed;
- Release Readiness: 21 PASS, 0 WARN, 0 FAIL;
- clean installation, keyboard/focus behavior, zoom, narrow layout, exports and
  the 25 MB performance boundary were reviewed manually;
- the verified demo and six final screenshots use synthetic project data.

## Important limitations

- calculations and explanations are deterministic; they are not causal or
  predictive claims;
- technical data quality does not prove business accuracy or suitability;
- files above 25 MB should be reduced, split or aggregated before upload;
- the application does not provide cloud synchronization, collaboration,
  scheduled delivery or autonomous decisions;
- review exported content before sharing it outside your organization.

Please report defects through GitHub Issues and security concerns through the
private process in
[`SECURITY.md`](https://github.com/lialit/Universal-CSV-Dashboard/blob/v1.0.0-rc.1/SECURITY.md).
