# Project Charter — AG Insurance QA Automation Lab

## 1. Purpose

Build a small, disciplined QA automation laboratory to learn, practise, and evidence the skills required by the **Test Automation Engineer** role at AG Insurance (reference **3492TESAE**, IS Life Division), and to prepare for its technical interviews.

## 2. Learning objectives

By the end of the project I can demonstrate, with committed evidence:

- ISTQB-style test design (equivalence partitioning, boundary analysis, decision tables) applied to a life-insurance domain.
- A manually designed, traceable test catalogue before any automation.
- Test-data management: designed synthetic data, SQL seed/reset scripts, isolation, and SQL validation queries.
- UFT One concepts on Windows: GUI tests, object repositories, VBScript function libraries, data-driven and keyword-driven execution, a hybrid framework.
- Defect triage: distinguishing application defects from script maintenance, test-data, and environment issues, with documented reasoning.
- Azure DevOps: work items, test plans, suites, cases, runs, and a YAML pipeline.
- Power BI quality reporting from execution-result data.
- Clear test governance writing: strategy, entry/exit criteria, severity/priority, reporting.

## 3. Scope

- **Application under test**: one small Flask life-insurance web application, capped at:
  - **2 user roles** (agent, manager),
  - **2 core entities** (Customer, Policy),
  - **~8 screens/endpoints**: login, dashboard, customer search, policy search, policy create, policy update, policy status change, premium calculation view.
- **Test catalogue**: ~36 tests (5 smoke, 10 functional, 10 regression, 5 negative, 3 data-validation, 3 access-control).
- **Automation**: one Playwright framework (Linux, design prototype) and one UFT hybrid framework (Windows), both mirroring the same design.
- **One** Azure DevOps project, **one** CI/CD pipeline, **one** Power BI dashboard.

### Core business rule — premium calculation (v1)

`premium = base_premium × age_factor × coverage_factor`

- `base_premium`: fixed per product type.
- `age_factor`: increases with age bands; **no new policy for age > 65** (boundary rule).
- `coverage_factor`: proportional to coverage amount within a min/max range.
- Invalid inputs (negative coverage, age out of range, missing data) must produce validation errors.

*This rule is deliberately simple and may be fine-tuned as test design reveals gaps; changes are recorded here with a date.*

## 4. Out of scope

- Performance, load, and security testing.
- Mobile testing.
- A real HP ALM / OpenText ALM server (concepts mapped to Azure DevOps instead).
- Multi-environment deployment, high availability, enterprise architecture.
- Any real client, customer, production, or personal data.

## 5. Test levels and types

Smoke, functional, regression, negative, data validation, access control. End-to-end flows are covered inside functional/regression. The application itself carries no unit-test coverage targets — it is a test target, not a product.

## 6. Definition of done

**The lab is done when all 12 phases have committed evidence in this repository, and I can explain every artifact unaided** — what it is, why it is designed that way, and what I would change at real-project scale.

Per-phase: a phase is done only when its artifacts are committed **and** I have explained what I built and why (recorded in `docs/interview-notes.md` from Phase 12 onward).

## 7. Time-box

- **Intensive sprint: 17–21 September 2026** — Milestone 1: repository, charter, test strategy, application under test, manual test catalogue.
- **Completion: by 30 September 2026** — remaining phases (SQL/test data, UFT exercises, Azure DevOps, CI/CD, Power BI, documentation, interview prep).
- If the deadline pressures scope, scope is cut from the end (Power BI depth first), never from test-design quality.

## 8. Known limitations

- UFT One is Windows-only; it cannot run in this repository's Linux environment. UFT work happens on an authorized Windows installation and its artifacts are committed here.
- If Azure DevOps access is unavailable, its structure is simulated in Markdown/CSV and clearly labelled as a simulation.
- **This is a personal learning project.** It is portfolio evidence of practised skills, not professional experience.

## 9. Data policy

All data is synthetic and obviously fake (e.g., customers named "Test Alpha", "Test Beta"). No passwords, tokens, licence keys, or private URLs are ever committed.
