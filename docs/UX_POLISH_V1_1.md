# v1.1 Navigation and Responsive UX Polish

This document records GH-08D for Issue #17 — navigation, empty states, and responsive UX polish.

## Scope

GH-08D improves the complete user journey without changing analytical calculations, data preparation, insight rules, or export semantics.

The review covers:

- navigation order and first-use entry point;
- empty dataset states;
- narrow browser widths;
- card and column wrapping;
- page hierarchy and next actions;
- consistency with the v1.1 guided onboarding flow.

## Navigation decision

The v1.1 navigation order remains:

1. Start Here;
2. Upload & Configure;
3. Executive Overview;
4. Business Insights;
5. Analysis Assistant;
6. Data Quality;
7. Export & Share;
8. About This Template.

This order follows the product journey from first contact to analysis, validation, sharing, and product context. No additional page or duplicate instruction layer is needed.

## Empty-state improvement

All analytical pages that require a loaded dataset use the shared `require_dataset()` guard.

GH-08D turns that guard into an actionable state:

- the message explains why the page cannot render;
- `Go to Start Here` returns the user to the guided demo/upload choice;
- `Upload a CSV` jumps directly to the configuration flow;
- the state stops page execution before dependent calculations run.

This removes a common dead end where a user could land on an analytical page and only be told that data was missing.

## Responsive layout

The shared theme now includes narrow-width rules rather than relying on a wide desktop canvas only.

At widths below 900 px:

- the main content padding is reduced;
- page titles scale down;
- Streamlit horizontal blocks may wrap;
- columns become flexible cards with a practical minimum width.

At widths below 560 px:

- page headings scale down again;
- multi-column content stacks to a single column;
- KPI cards, onboarding choices, summary panels, and other column-based layouts remain readable instead of being compressed into unusable narrow cards.

The responsive layer is intentionally CSS-only. It does not change calculations or build separate mobile-specific data paths.

## Existing states retained

The following existing UX patterns remain valid:

- Start Here gives first-time users `Try demo data` and `Use my CSV` routes;
- returning users can continue directly to Executive Overview or replace the current dataset;
- Upload & Configure provides parsing errors, validation warnings, detection evidence, and an explicit configuration acceptance step;
- Executive Overview explains when selected filters return no rows;
- analytical pages use consistent shared headers and sidebar navigation.

## Manual acceptance check

Before v1.1 release, verify the current interface in a clean browser session at:

- normal desktop width;
- approximately 900 px viewport width;
- approximately 560 px or narrower viewport width.

For each width:

1. open Start Here with no dataset;
2. try the demo path;
3. visit Executive Overview and the remaining analytical pages;
4. open a fresh session and navigate directly to an analytical page with no dataset;
5. confirm the recovery links are visible and usable;
6. confirm cards and columns do not overlap or become unreadably narrow;
7. confirm primary actions remain visible without horizontal page scrolling.

## Acceptance mapping for Issue #17

| Acceptance criterion | GH-08D result |
| --- | --- |
| Every page has a clear purpose and next action | Pass — navigation follows the product journey and missing-data states now expose recovery actions |
| Empty and error states explain how to continue | Pass — shared missing-dataset state links to Start Here and Upload & Configure |
| Visual hierarchy is consistent | Pass — shared header/theme remains canonical and responsive rules apply globally |
| Core workflows remain usable in narrow browser windows | Pass pending final manual viewport check — columns wrap/stack below documented breakpoints |
| Updated screenshots match final interface | Deferred to GH-08G / Issue #19 after UX and live-demo stabilization |

## Regression triggers

Repeat this review when any of the following changes materially:

- page order or navigation groups;
- Start Here onboarding;
- shared theme or column layout;
- Streamlit navigation/page-link APIs;
- new analytical pages are introduced;
- major KPI/card layout changes;
- release screenshots are refreshed.

## Decision

GH-08D establishes the v1.1 navigation and responsive UX baseline. Issue #17 can close when the PR passes CI and the documented narrow-width smoke check is accepted. Final release screenshots intentionally remain part of GH-08G so they are not made stale by later export or live-demo work.
