# v0.6 — Assist

> **Status: Exploratory — not committed for release**

This stage will proceed only if guided analysis creates measurable value beyond
deterministic summaries and can preserve privacy, evidence and user control.

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

- [ ] Explain the selected metric and aggregation
- [ ] Answer questions from deterministic computed results
- [ ] Identify unsupported questions
- [ ] Link answers to source fields and filters
- [ ] Show the calculation behind numeric claims

### Guided investigation

- [ ] Suggest next analytical questions
- [ ] Explain data-quality limitations
- [ ] Compare available segments or periods
- [ ] Draft a summary for user review
- [ ] Refuse causal or predictive claims without supporting methods

### Provider and privacy model

- [ ] Evaluate a fully local path
- [ ] Evaluate optional external providers
- [ ] Show data-handling information before use
- [ ] Minimize transmitted data
- [ ] Add explicit opt-in
- [ ] Add usage and cost controls

### Evidence model

- [ ] Require source-linked numeric claims
- [ ] Separate calculation from generated wording
- [ ] Display uncertainty
- [ ] Preserve the non-AI result beside the answer
- [ ] Log enough metadata for reproducibility without exposing sensitive data

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

Proceed toward a release only if:

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
| Decision | Not yet made |

