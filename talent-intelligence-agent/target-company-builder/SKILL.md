---
name: target-company-builder
description: Build a ranked target-company list for any role or company archetype, in any location. Either companies matching an archetype, or the enriched employer landscape where a role's talent sits, with funding, headcount, hiring signals, and why-they-fit rationale. Use when RJ wants a target company list, a poaching map with funding and headcount depth, or to enrich a bare employer list. Triggers on phrases like "build a target company list", "which companies should I target for", "map the companies hiring [role]", "enrich the employer list", "target company builder", "who are the competitors for talent". Skill 2 of the Talent Intelligence Agent chain.
---

# Target Company Builder

v1.1 · 2026-09-29

> v1.1 removes built-in New York sources (now a location pack), adds the live job board check for hiring signals, and saves to the per-search folder.

## Purpose

Produce a ranked, enriched list of target companies, each with funding, headcount, hiring signals, and a why-they-fit rationale, so a recruiter knows which companies matter and how to prioritize them. Skill 2 of the Talent Intelligence Agent chain. Sits between Talent Map (Skill 1) and Candidate Sourcing (Skill 3).

## Two modes

- **Archetype mode.** Input a company archetype (for example "Series A to C AI startup, 50 to 500 employees, product-led, in [metro]"). Output a ranked list of matching companies.
- **Talent-landscape mode.** Input a role and its ecosystem map (Skill 1). Output the enriched employer landscape where the role's candidates sit, upgraded from name and density to funding, headcount, hiring signal, and why-fit. This is the default inside the orchestrator.

## Inputs

Required:
- A company archetype, or a role plus its ecosystem map
- Location or geo focus

Optional:
- Stage, headcount, or sector filters
- Companies to exclude
- Purpose: poaching (where talent works) vs demand-mapping (who else hires this role)
- The hiring company's pay range, to judge approachability

## Process

1. **Assemble the company set.** Archetype mode: Built In (city edition), Crunchbase web results, funding news, and the matching location pack in `../talent-map/references/location-packs.md`. Talent-landscape mode: start from Skill 1's ecosystem map and add obvious adjacent players.
2. **Enrich each company** via web research: funding (latest round, amount, valuation), headcount and direction, and **hiring signals**. Cite each figure with a date. For public companies, prefer SEC filings for headcount and state WARN notices for layoffs.
3. **Live hiring signals.** Where a company is on Ashby, Greenhouse, or Lever, pull its board (see `../talent-map/scripts/job_board_scan.py`) for open roles in the target function and their posted pay ranges. A competing opening is a demand signal. A layoff or reorg that touched the target function is a supply signal.
4. **Score** for the purpose at hand. Poaching: talent density (1 to 3) x approachability (1 to 3), plus 1 for a verified "why now" supply signal. Demand: archetype match x hiring intensity. State the rule and the tie-breaks.
5. **Rank** by the stated rule.
6. **Flag data gaps.** Mark anything unverified as "not verified" and list it. Never estimate a figure to fill a cell.
7. **Save** to the search folder as `Target-Companies-<Role-or-Archetype>-<Location>.md`, or append an identified enrichment layer to an existing Sourcing Plan.

## Output structure

- **Ranking rule.** The formula and tie-breaks.
- **Ranked table:** Company | Stage / Funding | Headcount (direction) | Hiring signal | Why they fit | Rank rationale.
- **Top picks.** One or two lines each for the top 5.
- **Data gaps.** Every "not verified" figure and single-source claim.
- **Sources.** Cited URLs with dates.

## Quality bar

- Every funding, headcount, and valuation figure is cited and dated.
- Private labs, corporates, and search firms stay in the list with "N/A" for funding where it does not apply.
- The ranking rule is stated, not implicit.
- When enriching an existing list, the new layer is identified and separated, never silently merged.
- RJ-facing text follows her writing rules: no em or en dashes, plain declarative sentences.

## Examples (not defaults)

- Machine Learning Scientist (generative audio/music), Boston, for a Series-D AI startup. Talent-landscape mode. Appended as an enrichment layer in `Sourcing-Plan-ML-Scientist-Audio-Boston.md` (Section 3).

## Future iterations

- Crunchbase access for live funding data.
- A hiring-intensity score from live careers-page job counts.
