# v1.1 Product Execution Readiness

This document records GH-08A, the execution plan for the v1.1 — Polish & Adoption backlog.

## Goal

Turn the existing v1.1 backlog into a dependency-aware delivery sequence that prioritizes first-use value, product confidence, public adoption and release safety.

## Backlog reviewed

The v1.1 milestone currently contains these product issues:

- #14 — Deploy a public live demo;
- #15 — Add guided onboarding and bundled demo dataset;
- #16 — Optimize dashboard performance for medium and large CSV files;
- #17 — Polish navigation, empty states, and responsive UX;
- #18 — Harden Excel and PDF exports for real user workflows;
- #19 — Finalize user documentation and release screenshots;
- #20 — Run structured beta feedback round and triage findings;
- #21 — Complete v1.1 release readiness review.

## Recommended execution order

### 1. #15 — Guided onboarding and bundled demo dataset

This is the first delivery package because every later adoption task depends on a clean first-run experience. The public demo should not expose an empty or confusing initial state.

Primary outcome: a first-time user can reach a meaningful dashboard without external instructions and without supplying private data.

### 2. #16 — Performance optimization

Performance should be stabilized before UX polish and public exposure. Navigation, cache boundaries and repeat visits need to remain responsive on representative datasets so later usability work is not evaluated on a slow foundation.

Primary outcome: documented and repeatable performance behavior for small, medium and large synthetic CSV workloads.

### 3. #17 — Navigation, empty states and responsive UX

Once onboarding and performance are stable, polish the complete user journey: page labels, hierarchy, warning states, narrow-window behavior and clear next actions.

Primary outcome: a consistent end-to-end flow with no confusing dead ends.

### 4. #18 — Excel and PDF export hardening

Exports should be hardened against the final product state rather than before navigation and dashboard behavior settle.

Primary outcome: shareable Excel/PDF outputs that handle realistic edge cases and contain only intended data.

### 5. #14 — Public live demo

Deployment comes after the first-run path, performance, UX and exports are dependable. The hosted experience must be a representative product demonstration rather than merely a running Streamlit process.

Primary outcome: a public URL that opens directly into a safe, useful product experience using synthetic demo data.

### 6. #19 — User documentation and release screenshots

Documentation and screenshots should describe the actual final v1.1 interface and hosted journey, so they follow live-demo stabilization.

Primary outcome: README, START_HERE and screenshots match the released product and public demo.

### 7. #20 — Structured beta round

Beta feedback is most valuable after the intended v1.1 experience exists. Findings can then distinguish real usability gaps from unfinished implementation.

Primary outcome: at least three structured feedback sessions/responses, with actionable P0/P1 findings converted into Issues.

### 8. #21 — v1.1 release readiness

This is the final release gate after implementation, documentation and beta triage.

Primary outcome: clean install, hosted-demo verification, automated checks, issue review and release notes all pass before v1.1 is published.

## Dependency graph

The main delivery path is:

`#15 onboarding -> #16 performance -> #17 UX -> #18 exports -> #14 live demo -> #19 docs -> #20 beta -> #21 release readiness`

Parallel work is allowed only when it does not make later evidence stale. In particular:

- documentation screenshots should not be finalized before the UI is stable;
- beta testing should not be used as a substitute for known unfinished P0 work;
- public deployment should not be treated as complete until onboarding and synthetic demo data work in a clean browser session;
- release readiness remains the final gate and should not be collapsed into implementation PRs.

## GH-08 package map

Recommended package structure:

- GH-08A — v1.1 execution readiness and sequencing;
- GH-08B — onboarding and bundled demo data (#15);
- GH-08C — performance confidence (#16);
- GH-08D — navigation and responsive UX polish (#17);
- GH-08E — export hardening (#18);
- GH-08F — public live demo (#14);
- GH-08G — documentation and screenshots (#19);
- GH-08H — beta feedback round (#20);
- GH-08I — v1.1 release readiness (#21).

A package may use multiple PRs if implementation risk requires separation, but the issue-level acceptance criteria remain the source of truth.

## Delivery rules

For every package:

1. preserve local-first privacy unless the scope explicitly concerns public hosting;
2. use only synthetic demo/test data in the repository and public demo;
3. keep analytics behavior stable unless a product issue explicitly changes it;
4. require green CI before merge;
5. add focused tests or repeatable manual evidence for new behavior;
6. update canonical documentation in the same package when public behavior changes;
7. avoid closing an Issue until all of its acceptance criteria are demonstrably satisfied.

## Definition of v1.1 ready

v1.1 is ready only when:

- onboarding works from a clean session;
- realistic CSV workloads remain responsive within documented limits;
- navigation and empty/error states are polished;
- Excel/PDF exports pass realistic edge cases;
- the public demo is accessible and safe;
- repository documentation matches the final interface;
- structured beta feedback has been triaged;
- no unresolved P0 Issues remain;
- remaining P1 work is either completed or explicitly deferred;
- the full release-readiness gate passes.

## Decision

GH-08 will execute the v1.1 backlog in the order above. The first implementation package after this planning PR is GH-08B for Issue #15 — guided onboarding and bundled demo dataset.
