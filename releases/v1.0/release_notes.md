# v1.0 — Launch

> **Status: Planned — not released**

`v1.0` is a stability and trust milestone. It is not a promise that every
exploratory feature will be included.

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

## Candidate product scope

The final scope will be selected from validated pre-`1.0` work.

Required core capabilities:

- [ ] Reliable CSV upload and parsing
- [ ] Explainable, editable field detection
- [ ] Consistent KPI calculations
- [ ] Useful time, category and distribution views
- [ ] Visible data-quality checks
- [ ] Clear unsupported-input guidance
- [ ] Responsible exports included in the final scope
- [ ] Complete local-first workflow

Optional capabilities are included only if validated:

- [ ] Rule-based executive summary
- [ ] Evidence-linked explanations
- [ ] Saved configuration workflow
- [ ] PDF or Excel reporting
- [ ] Guided analysis

## Launch criteria

### Product validation

- [ ] Core workflow tested with varied business datasets
- [ ] Field-detection corrections reviewed
- [ ] Time to first useful understanding measured
- [ ] Empty, warning and error states validated
- [ ] Known analytical limitations documented

### Engineering

- [ ] Supported Python versions defined
- [ ] Automated test suite passes
- [ ] CI checks are stable
- [ ] Clean installation succeeds
- [ ] Dependencies are pinned or bounded intentionally
- [ ] Performance is reviewed for the supported file size
- [ ] Upgrade and compatibility policy is documented

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

- [ ] README matches shipped behavior
- [ ] `START_HERE.md` installation verified
- [ ] Product documents remain aligned
- [ ] Architecture and contribution docs are current
- [ ] License and attribution confirmed
- [ ] Issue and pull-request templates reviewed
- [ ] Release notes and changelog completed

### Release assets

- [ ] Final screenshots
- [ ] Verified demo GIF
- [ ] Open Graph image
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

1. Freeze the `v1.0` scope.
2. Move remaining work out of the launch milestone.
3. Complete product, engineering and documentation validation.
4. Publish a release candidate.
5. Resolve launch-blocking defects.
6. Verify final assets and version metadata.
7. Publish the tag, GitHub Release and changelog entry.

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
| Supported Python | To be defined |
| Migration required | To be determined |
