# Test Strategy — AG Insurance QA Automation Lab

Scope and business rules are defined in [project-charter.md](project-charter.md). This document defines *how* testing is done.

## 1. Test objectives

- Verify the life-insurance application's business rules — above all premium calculation and its boundaries — behave as specified.
- Detect regressions quickly and cheaply after every change.
- Practise and evidence disciplined automation design (UFT hybrid framework, Playwright prototype).
- Produce traceable, reportable results (Azure DevOps runs → Power BI).

## 2. Test levels and types

| Type | Purpose | Primary level |
|---|---|---|
| Smoke | "Is the build testable at all?" — run first, always | UI + API |
| Functional | Verify each business rule and screen behaviour | API + UI |
| Regression | Re-verify previously working behaviour after change | API-heavy, thin UI |
| Negative | Invalid inputs, boundaries, error handling | API + UI |
| Data validation | Database state matches what the UI/API claims | SQL |
| Access control | Each role sees and does only what it may | API + UI |
| End-to-end | Full business journeys (quote → policy → status change) | Covered inside functional/regression |

## 3. Test pyramid for this lab

Most checks run at API/SQL level: fast, stable, cheap to maintain. A thin set of UI journeys runs in UFT (Windows) and Playwright (Linux prototype).

**Deliberate deviation:** this lab over-invests in UI tests relative to a real project, because UFT UI automation is the skill being practised. A production strategy would push more coverage down the pyramid; this document says so explicitly rather than pretending the ratio is ideal.

## 4. Automation selection criteria

Automate when a test is: deterministic, repeated every cycle, runs against a stable UI, and has high regression value.
Keep manual: exploratory testing, one-off checks, visually judged layouts, and tests against screens still changing.

**Rule of thumb: automate the boring; stabilize before automating.**

## 5. Smoke vs regression

The 5-test smoke suite answers one question in under two minutes: *can testing proceed?*

Recommended smoke set (rationale: each failure blocks everything behind it):
1. Application starts and login page loads.
2. Agent can log in.
3. Policy search returns a seeded policy.
4. A minimal valid policy can be created.
5. Premium calculation returns a value for a known input.

Regression is everything previously verified; smoke is the *gate* in front of it. A test belongs in smoke only if its failure makes running the rest pointless.

## 6. Entry and exit criteria

**Entry:** application deployed, seed data loaded and verified by SQL check, smoke suite green.
**Exit:** all planned tests executed; no open critical/high defects; every failure triaged (defect vs maintenance vs data vs environment) and documented; results published.

## 7. Defect severity and priority

Severity = business impact. Priority = fix order. They are independent.

| Severity | Meaning | Example |
|---|---|---|
| Critical | Wrong money or data loss | Premium calculated incorrectly |
| High | Core flow broken, no workaround | Policy creation fails for valid input |
| Medium | Function impaired, workaround exists | Search filter ignores one criterion |
| Low | Cosmetic | Typo on login page |

Priority (P1–P4) is assigned at triage. A low-severity typo can be P1 if it blocks a demo; a critical defect in an unreleased feature can wait behind a release blocker.

## 8. Triage: defect or test-maintenance issue?

First step when a previously passing test fails: **reproduce the failing step manually against the same build and data.**

- Manual reproduction fails too → likely an **application defect** (or data/environment issue — check seed state and environment next).
- Manual reproduction passes → likely **script maintenance**: the app changed (renamed element, new field, changed label) and the script did not.

Then confirm the category with evidence (screenshot, SQL state, app version/diff) before logging anything. Reasoning for each triaged case is recorded in `docs/defect-triage-examples.md` (Phase 7).

## 9. Test data

- All data synthetic and obviously fake (charter §9).
- Every automated test declares its data; shared mutable data between tests is forbidden.
- Seed and reset scripts restore a known database state before each run; SQL validation queries verify it.
- Data that a test mutates (created/updated policies) is isolated per test or cleaned up afterwards.

## 10. Risk-based coverage

Depth follows risk: premium calculation and policy status transitions get the densest coverage (money and contract state); search screens get the least. Boundary values (age 65, coverage min/max) each get explicit tests on both sides of the boundary.

## 11. Environments

- **Linux (this repo's CI):** application, API/SQL checks, Playwright prototype.
- **Windows (local, authorized):** UFT execution, Power BI Desktop.
- Environment differences are recorded in `docs/known-limitations.md`.

## 12. Reporting and metrics

Per run: total / passed / failed / blocked / not run, pass rate, duration, failure category (defect, maintenance, data, environment). Trend over time and defect breakdowns feed the Power BI dashboard (Phase 10). Metrics report *state*, never individual blame — and a rising maintenance-failure ratio is treated as a framework-design smell, not noise.

## 13. Evidence before closing a defect

A defect closes only with: the fixed build/version identified, the failing test re-run green on it, and the regression tests around it green. "Cannot reproduce" closes only after retesting on the original build, data, and environment.
