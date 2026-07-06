---
name: target-company-builder
description: Build a ranked target-company list — companies matching an archetype, or the enriched employer landscape where a role's talent sits — with funding, headcount, hiring signals, and why-they-fit rationale. Use when RJ wants a target company list, a competitor/poaching map with funding+headcount depth, or to enrich a bare employer list. Triggers on phrases like "build a target company list", "which companies should I target for", "map the companies hiring [role]", "enrich the employer list", "target company builder", "who are the competitors for talent". Skill 2 of the Talent Intelligence Agent chain.
---

# Target Company Builder

v1.0 · 2026-06-10

## Purpose

Produce a ranked, enriched list of target companies — each with funding, headcount, hiring signals, and a why-they-fit rationale — so a recruiter knows not just *which* companies matter but *how to prioritize* them. Skill 2 of the Talent Intelligence Agent chain. Sits between Talent Map (Skill 1) and Candidate Sourcing (Skill 3).

## Two modes

- **Archetype mode (canonical).** Input a company archetype (e.g., "Series A–C AI startup, NY, 50–500, product-led"). Output a ranked list of matching companies.
- **Talent-landscape mode.** Input a role + its ecosystem map (from Skill 1). Output the **enriched employer landscape** — the same companies where the role's candidates sit, but upgraded from "name + density" to full funding/headcount/hiring-signal/why-fit depth. This is the mode that enriches Skill 3's lightweight target-employer list.

## Inputs

Required:
- Either a company archetype, or a role + ecosystem map (Skill 1 output)
- Location / geo focus

Optional:
- Stage, headcount, or sector filters
- Companies to exclude
- Whether the purpose is poaching (where talent works) vs. demand-mapping (who else hires this role)

## Process

1. **Assemble the candidate company set.** Archetype mode: pull from Tech:NYC member list, NYC Startups Airtable, Built In, Crunchbase web results. Talent-landscape mode: start from Skill 1's ecosystem map employers and expand with obvious adjacent players.
2. **Enrich each company** via web research — funding (latest round, amount, investor, valuation), headcount (and growth trajectory), and **hiring signals** (open roles in the target function, recent funding, expansion announcements, reorgs). Cite each figure.
3. **Score why-they-fit** for the purpose at hand (poaching density vs. demand match): stage fit, talent density, approachability, and any "why now" signal.
4. **Rank** by a transparent rule (e.g., poaching mode → talent density × approachability; demand mode → archetype match × hiring intensity).
5. **Flag data gaps** — private labs and corporates won't have "funding"; note when a figure is unavailable rather than guessing.
6. Output as a table; save to `/Claude for Builders/10x-TA-Leader/outputs/Target-Companies-[Role-or-Archetype]-[Location].md`, **or** append an identified enrichment layer to an existing Sourcing Plan when run in talent-landscape mode.

## Output structure

Ranked table: **Company | Stage / Funding | Valuation | Headcount (trajectory) | Hiring signal | Why-they-fit | Rank rationale.**

Plus:
- **Top picks** — 1–2 line prioritization note for the top 3–5.
- **Data gaps** — companies where funding/headcount couldn't be verified.
- **Sources** — cited URLs with dates.

## Quality bar

- Every funding/headcount/valuation figure is cited and dated.
- Private/corporate labs are kept in the list but clearly marked "N/A — corporate" for funding, with headcount/hiring-signal still filled where possible.
- Ranking rule is stated, not implicit.
- When enriching an existing list, the new layer is clearly **identified and separated** from the original lite list — never silently merged.

## Sources

- Crunchbase (public web), Tech:NYC member list, NYC Startups Airtable, Built In, company careers pages, funding-news outlets (TechCrunch, Music Business Worldwide, etc.). See `Data-Sources.md`.

## Demo case (canonical test)

- Role: Machine Learning Scientist (generative audio/music), Boston (a Series-D AI startup)
- Mode: Talent-landscape (enriches the audio-ML employer landscape)
- Output: appended as an identified enrichment layer in `Sourcing-Plan-ML-Scientist-Audio-Boston.md` (Section 3).

## Future iterations

- Auto-pull Crunchbase via allowlisted access for live funding data.
- Cross-reference Tech:NYC + NYC Startups Airtable for NY archetype runs.
- Add a "hiring intensity" score from live careers-page job counts.
