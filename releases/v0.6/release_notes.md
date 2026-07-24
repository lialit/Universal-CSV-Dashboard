# v0.6 — Assist

> **Status: Local deterministic scope delivered to `main` — not separately tagged**

This is the historical scope and decision record for the Assist milestone.
Checked local deterministic items are included in `1.0.0-rc.1`. External model
providers remain deferred. No standalone `v0.6` tag or GitHub Release was
published.

## Exploration outcome

Determine whether an optional analytical assistant can help users ask better
questions and understand calculations without becoming an opaque source of
unsupported conclusions.

## Why this stage is exploratory

Conversational analytics can be useful, but it introduces specific risks:

- generated text may sound more certain than the data allows;
- private business data may be sent to an external provider;
- costs may be unpredictable;
- answers may not be reproducible;
- a fluent response may hide an incorrect calculation.

The product must validate the need and the safeguards before treating this as a
committed release.

## Candidate experiments

### Dataset questions

- [x] Explain the selected metric and aggregation
- [x] Answer questions from deterministic computed results
- [x] Identify unsupported questions
- [x] Link answers to source fields and filters
- [x] Show the calculation behind numeric claims

### Guided investigation

- [x] Suggest next analytical questions
- [x] Explain data-quality limitations
- [x] Compare available segments or periods
- [x] Draft a summary for user review
- [x] Refuse or flag causal and predictive claims without supporting methods

### Provider and privacy model

- [x] Evaluate and implement a fully local deterministic path
- [ ] Evaluate optional external providers
- [x] Show data-handling information before use
- [x] Keep the delivered path free of transmitted CSV data
- [ ] Add explicit opt-in
- [ ] Add usage and cost controls

### Evidence model

- [x] Require source-linked numeric claims
- [x] Separate calculation from interpretation
- [x] Display uncertainty
- [x] Preserve deterministic evidence beside the answer
- [x] Keep method and field metadata visible without persisting sensitive rows

## Non-goals

This stage will not create:

- an autonomous decision-maker;
- automatic execution of business actions;
- unreviewed recommendations;
- hidden external data transfer;
- a requirement to use AI for core product value;
- general-purpose chat unrelated to the loaded dataset.

## Required guardrails

- The existing non-AI workflow remains fully useful.
- AI functionality is optional and disabled by default.
- Users know which data may leave their machine.
- Every numeric answer links to a deterministic result.
- The assistant can clearly say that the data cannot answer a question.
- Cost and usage are visible.
- Generated summaries require user review before export.

## Evaluation plan

### Value

- [ ] Compare task completion with and without the assistant
- [ ] Measure whether suggested questions improve investigation
- [ ] Confirm users understand the underlying evidence
- [ ] Identify use cases already served better by rule-based explanations

### Safety and trust

- [ ] Test unsupported causal questions
- [ ] Test ambiguous metric definitions
- [ ] Test prompt injection inside uploaded text fields
- [ ] Test sensitive-data handling
- [ ] Review incorrect-answer recovery

### Decision gate

The local deterministic scope passed the evidence, privacy and control gate.
External-provider work did not enter this release. Any future provider path
must still prove that:

- the assistant improves a defined user task;
- evidence remains inspectable;
- privacy controls are practical;
- cost is predictable;
- failure modes are understandable;
- the feature does not weaken the core product.

## Known risks

| Risk | Mitigation |
|---|---|
| Fluent but incorrect answer | Ground numeric claims in deterministic calculations |
| Sensitive data leaves the machine | Explicit opt-in and data minimization |
| Feature distracts from the core product | Require measurable task value |
| Provider cost is unclear | Usage limits and visible estimates |
| Uploaded text manipulates the assistant | Treat file content as data, not instructions |

## Release record

This section remains empty unless the exploration passes the decision gate.

| Field | Value |
|---|---|
| Release date | — |
| Git tag | — |
| GitHub Release | — |
| Decision | Local deterministic scope accepted for `1.0.0-rc.1`; external providers deferred |
