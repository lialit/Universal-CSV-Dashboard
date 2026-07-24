# v1.0 — Launch

> **Status: Release candidate — validation in progress, not released**

The frozen candidate version is `1.0.0-rc.1`.

`v1.0` is a stability and trust milestone. It includes the validated local
workflow delivered through the `0.3–0.6` development milestones; it does not
promise that every exploratory or external-provider capability is included.

## Release outcome

A new user should be able to discover, install, understand and use Universal
CSV Dashboard without private guidance.

The product should provide a dependable path from CSV upload to a trustworthy
first-pass analysis, supported by clear documentation and release practices.

## What `1.0` means

Version `1.0` means:

- the core product promise is stable;
- supported inputs and limitations are documented;
- important calculations are tested;
- installation is repeatable;
- the local-first workflow is complete;
- breaking changes are managed intentionally;
- users and contributors know where to get help.

It does not mean that the product has every planned feature.

## Frozen candidate scope

Only launch-blocking fixes may enter `1.0.0-rc.1`. New product capabilities
move to a later version.

Required core capabilities:

- [x] Reliable CSV upload and parsing
- [x] Explainable, editable field detection
- [x] Consistent KPI calculations
- [x] Useful time, category, distribution and correlation views
- [x] Transparent Data Quality Score and issue details
- [x] Rule-based executive summary
- [x] Evidence-linked Business Insights
- [x] Local deterministic Analysis Assistant
- [x] Calculation Explainer and evidence-based summary drafts
- [x] Pre-share Claim Guard
- [x] Saved project workflow with schema validation
- [x] Structured Excel and executive PDF reporting
- [x] Light, Corporate and Dark report themes
- [x] Complete local-first workflow

### Explicitly excluded

- external AI or analytics providers;
- hidden upload or transfer of CSV values;
- cloud project synchronization;
- real-time collaboration;
- scheduled or emailed reports;
- predictive modeling or causal inference;
- autonomous business decisions.

## Launch criteria

### Product validation

- [ ] Core workflow tested with varied business datasets
- [ ] Field-detection corrections reviewed
- [ ] Time to first useful understanding measured
- [ ] Empty, warning and error states validated
- [x] Known analytical limitations documented

### Engineering

- [x] Supported Python versions defined
- [x] Automated test suite passes
- [x] CI checks are stable
- [ ] Clean installation succeeds
- [x] Dependencies are pinned or bounded intentionally
- [ ] Performance is reviewed for the supported file size
- [x] Upgrade and compatibility policy is documented

### Privacy and security

- [x] Local data flow documented
- [x] Temporary-file handling reviewed
- [x] Export behavior reviewed
- [x] Dependency vulnerabilities reviewed
- [x] Optional external processing requires explicit consent
- [x] Security-reporting path documented

### Accessibility and UX

- [ ] Keyboard and focus behavior reviewed where supported
- [ ] Color is not the only information carrier
- [ ] Contrast and zoom reviewed
- [ ] Long labels and narrow screens tested
- [ ] First-run guidance validated with a new user

### Documentation and open source

- [x] README matches shipped behavior
- [ ] `START_HERE.md` installation verified
- [x] Product documents remain aligned
- [ ] Architecture and contribution docs are current
- [ ] License and attribution confirmed
- [ ] Issue and pull-request templates reviewed
- [x] Release notes and changelog completed

### Release assets

- [ ] Final screenshots
- [ ] Verified demo GIF
- [x] Open Graph image
- [ ] GitHub Release description
- [ ] Version tag
- [ ] Announcement copy

## Non-goals

`v1.0` does not require:

- enterprise BI governance;
- real-time collaboration;
- a data warehouse;
- every specialized analytics module;
- a cloud-hosted service;
- AI functionality;
- removal of the local-first workflow.

## Known risks

| Risk | Mitigation |
|---|---|
| Version number creates unrealistic expectations | Publish explicit scope and limitations |
| Documentation drifts from behavior | Validate docs during the release checklist |
| Late features destabilize the core | Freeze scope before release-candidate testing |
| Installation differs across systems | Test supported environments from clean setups |
| Visual polish hides analytical limitations | Preserve quality and methodology context |

## Release-candidate process

The complete executable procedure, including clean-install validation, pytest,
tagging, publication and rollback, is maintained in
[`docs/10_RELEASE_PROCESS.md`](../../docs/10_RELEASE_PROCESS.md).

## Exit criteria

`v1.0` is ready when the core product is dependable, its limitations are
understandable and a new user can complete the primary workflow without private
support.

## Release record

| Field | Value |
|---|---|
| Release date | — |
| Git tag | — |
| GitHub Release | — |
| Supported Python | Python 3.11 |
| Migration required | No migration from a published version; saved project compatibility is validated when loaded |
