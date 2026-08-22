# v1.1 Beta Feedback Guide

This guide supports GH-08H / Issue #20 — a small structured beta round before the v1.1 release gate.

## Purpose

The beta round validates whether a new user can understand and use Universal CSV Dashboard without private guidance.

The round should reveal:

- onboarding confusion;
- navigation dead ends;
- unclear or misleading insights;
- export problems;
- missing expectations that materially affect v1.1 readiness.

Do not collect private participant data in the repository. Record only the role/context needed to interpret the feedback.

## Minimum evidence

Issue #20 is complete only after at least **three beta sessions or equivalent structured responses**.

Use a mixed group when practical, for example:

- one analyst or technically confident user;
- one consultant/freelancer or business-facing user;
- one non-technical business user.

The same script should be used for every participant so findings remain comparable.

## Beta entry point

Public demo:

https://universal-csv-dashboard-ujqkgrohd7vy4zexcxkuqg.streamlit.app/

Participants should begin in a fresh browser session. The preferred first-run path is **Try demo data** so the session does not require sharing a real file.

## Session script

Target duration: 10–15 minutes.

### 1. First impression

Without explaining the product, ask the participant to open the demo and answer:

- What do you think this product does?
- What would you click first?
- Is the difference between **Try demo data** and **Use my CSV** clear?

Record hesitation or wrong assumptions, not just the final answer.

### 2. Onboarding

Ask the participant to choose **Try demo data** and continue without coaching.

Observe:

- whether the next step is obvious;
- whether Executive Overview feels like a useful first destination;
- whether labels and navigation are understandable;
- whether anything looks like an error or unfinished state.

### 3. Insights and quality

Ask the participant to:

1. identify the most important change or pattern they see;
2. open Business Insights;
3. open Data Quality;
4. explain in their own words what one insight means and what one quality result means.

Observe whether evidence, limitations and confidence language are understandable.

### 4. Analysis Assistant

Ask the participant to open Analysis Assistant and use one supported question.

Observe:

- whether the purpose of the page is clear;
- whether the response feels traceable rather than magical;
- whether limitations are visible enough;
- whether the user understands this is deterministic/local guidance, not a general AI chatbot.

### 5. Export

Ask the participant to open Export & Share and answer:

- Which option would you use to send results to someone else?
- Which option would you use to continue analysis later?
- Is the difference between project JSON, Excel and PDF clear?

If practical, download one Excel or PDF export and confirm that the filename and result look sensible.

### 6. Closing questions

Ask:

- What was easiest?
- What was confusing?
- What did you expect to find but could not?
- Would you trust the output enough to use it as a first-pass analysis? Why or why not?
- What single change would most improve the product?

## Response template

For each session, record only anonymized structured notes:

```text
Session: BETA-01 / BETA-02 / BETA-03
Participant context: analyst / consultant / business user / other
Environment: desktop browser + OS if relevant

First impression:
- ...

Onboarding:
- ...

Navigation:
- ...

Insights / Data Quality:
- ...

Analysis Assistant:
- ...

Exports:
- ...

Most important confusion or defect:
- ...

Most valuable positive signal:
- ...

Suggested improvement:
- ...
```

Do not include names, email addresses, employer names, customer datasets, screenshots containing private data, or other identifying information.

## Triage rules

Classify every actionable finding before the v1.1 release gate.

### Blocker

Use when the participant cannot complete a core flow or the product produces materially wrong/unsafe output.

Examples:

- demo cannot start;
- app crashes on a core page;
- export is corrupt or exposes a private local path;
- guidance presents unsupported claims as facts.

A blocker must be fixed before v1.1.

### High impact

Use when the flow works but a major part of the target experience is confusing or unreliable for multiple participants.

Examples:

- Start Here choice is repeatedly misunderstood;
- navigation hides a required next step;
- insight wording is consistently misread;
- users cannot distinguish export types.

High-impact findings should normally be fixed before v1.1 or explicitly waived with a documented reason.

### Polish

Use for non-blocking clarity, wording, layout or convenience improvements.

Polish may be included in v1.1 when low risk. Otherwise move it to the backlog.

### Later / out of scope

Use for requests that expand the product beyond v1.1, such as new analytical modules, external AI providers, collaboration, scheduled delivery or major new data sources.

Do not let feature requests silently become release blockers.

## Converting findings into Issues

Create a GitHub Issue when a finding is actionable and reproducible.

Each Issue should include:

- anonymized beta evidence (`BETA-01`, etc.);
- observed behavior;
- expected behavior;
- severity: blocker / high / polish;
- v1.1 decision: fix now / defer;
- reproduction steps when relevant.

If several participants report the same problem, keep one Issue and reference all affected beta session IDs.

## Final beta summary

After at least three sessions, add `docs/BETA_FEEDBACK_SUMMARY.md` containing:

- number and broad participant types;
- recurring positive signals;
- recurring confusion points;
- Issues created from blocker/high findings;
- deferred ideas and target backlog/release;
- final statement on whether any unresolved v1.1 blockers remain.

Issue #20 closes only after this evidence exists and every blocker/high-impact finding has been triaged.
