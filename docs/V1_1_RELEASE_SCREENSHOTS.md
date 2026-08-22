# v1.1 Release Screenshot Set

This document defines the canonical screenshot set for GH-08G / Issue #19.

The screenshots must represent the current hosted v1.1 workflow and use only the bundled synthetic demo dataset. Do not capture customer data, local filesystem paths, browser-profile information, credentials, or private session content.

## Capture source

Use the public Streamlit Community Cloud deployment:

https://universal-csv-dashboard-ujqkgrohd7vy4zexcxkuqg.streamlit.app/

Start from a clean browser session and choose **Try demo data** so every screenshot is reproducible from the same synthetic state.

## Recommended capture settings

- desktop browser viewport around 1440×900;
- browser zoom 100%;
- Streamlit sidebar visible where it helps explain navigation;
- no browser bookmarks bar or unrelated tabs in the crop;
- capture the application area cleanly;
- do not include Streamlit deployment/admin controls;
- keep the same light theme and demo dataset across the set.

The images may be cropped for presentation, but the analytical content and labels must not be altered.

## Canonical files

Store the final screenshots under `releases/v1.1/screenshots/` using these names:

1. `01-start-here.png` — Start Here with the **Try demo data** and **Use my CSV** paths visible.
2. `02-executive-overview.png` — KPI cards plus the primary overview/trend content after demo data is loaded.
3. `03-business-insights.png` — representative evidence-linked insight cards and supporting visualization/content.
4. `04-analysis-assistant.png` — supported deterministic question/guidance flow with evidence or calculation context visible.
5. `05-data-quality.png` — Data Quality score plus representative issue/component detail.
6. `06-export-share.png` — project, Excel, and PDF export options with the privacy/sharing context visible.

Optional if it adds useful public context:

7. `07-upload-configure.png` — own-CSV upload/configuration path. This is secondary in v1.1 because Start Here is now the default entry page.

## README presentation

The v1.1 README gallery should lead with **Start Here**, not Upload & Configure.

Recommended gallery order:

- Start Here + Executive Overview;
- Business Insights + Analysis Assistant;
- Data Quality + Export & Share.

The live-demo CTA remains the primary way for visitors to explore the product interactively; screenshots are supporting evidence and should match that hosted interface.

## Acceptance checklist

Before merging the final documentation PR:

- every required image above exists;
- every image was captured with bundled synthetic demo data;
- screenshots match current navigation and page labels;
- no private/local data appears;
- README references only files that exist;
- documentation link checks pass;
- setup, privacy, export, architecture, contribution, and live-demo links remain easy to find;
- README and ROADMAP describe v1.1 as current work rather than a hypothetical future state;
- the release hub records v1.1 as the active Polish & Adoption stage without claiming it is released before the tag exists.

## Decision

Issue #19 should close only after the user-facing documentation and this verified screenshot set land together. The screenshot refresh is not cosmetic: it is evidence that the public repository describes the interface a visitor actually sees in v1.1.
