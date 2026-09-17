# AG Insurance QA Automation Lab

A personal learning laboratory built around the **Test Automation Engineer** opportunity at AG Insurance (reference **3492TESAE**, IS Life Division).

## Disclaimer

This is a **personal learning project and portfolio evidence only**.

- It contains **no real client, customer, production, or personal data** — all test data is synthetic.
- Completing this lab does **not** constitute professional experience with the tools involved.
- Commercial tools (OpenText UFT One, Power BI) are used only via authorized trials or licensed installations on a suitable Windows machine, with the exact versions documented.

## Repository map

| Folder | Purpose |
|---|---|
| `docs/` | Project charter, test strategy, test catalogue, defect-triage guides, interview notes |
| `application/` | Small life-insurance application under test (Python/Flask + SQL) |
| `automation/` | Linux-executable automation framework (Playwright) mirroring UFT concepts: object repository, keyword-driven and data-driven design |
| `uft/` | UFT One tests, object repositories, and VBScript function libraries produced on a Windows environment |
| `test-data/` | Designed test data (CSV), SQL seed, reset and validation scripts |
| `azure-devops/` | Pipeline YAML and test-plan structure/exports |
| `powerbi/` | Test-results CSV extracts and dashboard evidence |
| `evidence/` | Curated screenshots, execution results, and example defects |

## Current status

**Milestone 1 in progress** — repository skeleton, project charter, test strategy, application under test, and manual test catalogue.

## Technology stack

- Git, Python 3.11, Flask, SQLite (PostgreSQL optional later)
- Playwright + Chromium for Linux-side UI automation practice
- OpenText UFT One + VBScript (Windows environment, authorized installation)
- Azure DevOps (Boards, Test Plans, Pipelines)
- Power BI Desktop (Windows) for quality reporting

## Known limitation (up front)

UFT One requires a Windows execution environment. Development and design work in this repository happen on Linux; UFT scripts are authored and executed on a Windows machine and their artifacts and evidence are committed here. See `docs/known-limitations.md` (added in a later phase).
