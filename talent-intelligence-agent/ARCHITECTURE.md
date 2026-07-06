# Talent Intelligence Agent: Architecture

v1.0 · 2026-05-07

Priority build. The first of the Top 10. Demo case: GTM AI Engineer in NY at an AI startup.

## Outcome

Given a role + location + company archetype, return a sourcing brief any recruiter could pick up: market read, ranked target companies, ranked candidates, voice-matched outreach.

## Why chained skills (not one mega-skill)

- Reusable independently. Skill 1 alone is a market intel weapon. Skill 4 alone is a voice-matched outreach generator.
- Each is its own LinkedIn post.
- Easier to debug, version, and improve.
- Mirrors RJ's business-first-ai framework: building blocks first, orchestration second.

## Five chained skills + orchestrator

### Skill 1: Talent Map
- **Inputs:** role, location, optional comp band, optional seniority.
- **Outputs:** market size, supply/demand signal, comp benchmarks, common backgrounds, hot vs. saturated, top 5 insights to brief a hiring manager.
- **Sources:** Built In, Levels.fyi, Glassdoor, public job posts, news, Tech:NYC NY Snapshot, public funding data.

### Skill 2: Target Company Builder
- **Inputs:** company archetype (e.g., "Series A-C AI startup, NY-based, 50-500 employees, product-led").
- **Outputs:** ranked target company list with funding, headcount, hiring signals, why-they-fit rationale.
- **Sources:** Tech:NYC member list, NYC Startups Airtable, Crunchbase web results, Built In NYC, Decoded Futures member orgs.

### Skill 3: Candidate Sourcing & Ranking
Two modes so the skill works with or without paid tools.

- **Mode A (no paid tools):** Generates candidate hypothesis profile (ICP) + boolean strings to paste into LinkedIn.
- **Mode B (with Juicebox):** Ingests Juicebox csv export. Ranks candidates against the role with match score, strengths, gaps, "why now" trigger (recent layoffs, acquisitions, IPOs, tenure milestones).

### Skill 4: Voice-Matched Outreach
- **Inputs:** candidate profile + role context.
- **Outputs:** voice-matched first-touch + two-message follow-up cadence, channel-tuned for LinkedIn InMail vs. email.
- **Voice training:** pulled from RJ's Gmail sent folder (sourcing/recruiter messages only, no sensitive content).

### Skill 5: Talent Intelligence Agent (Orchestrator)
- One command runs the chain end-to-end.
- Returns a sourcing brief any recruiter could pick up.
- Open decision: build as a Claude Agent vs. sequenced Skill chain.

## v1 build sequence

1. **Session 1:** Skills 1 + 2, tested against GTM AI Engineer in NY at AI startup.
2. **Session 2:** Skill 3 with both modes. Run Juicebox once together to capture export format.
3. **Session 3:** Skill 4 (voice match from Gmail) + Skill 5 (orchestrator).

## Demo prompt (canonical test case)

- Role: GTM AI Engineer.
- Location: New York.
- Company archetype: Series A-C AI startup, NY-based or NY hub, 50-500 employees, product-led.

Every skill is validated against this prompt before shipping.

## Quality bar for v1

- Demo + interview weapon, not production-grade in-seat deployment.
- Output should be defensible in a live interview run-through.
- Each skill must produce a shareable artifact (csv, markdown, table).

## What good looks like (Skill 1 example output)

A market brief that tells a hiring manager:
1. There are roughly N GTM AI Engineers in NY at our target stage.
2. Comp range is $X to $Y base + equity.
3. The most common backgrounds are A, B, C.
4. Supply is tight/loose because of [reason].
5. The 3 things to do this week to win the market.

## Open decisions

- ~~Skill 5 architecture: Claude Agent (autonomous) vs. sequenced Skill chain (deterministic).~~ **Resolved 2026-06-10:** v1 = deterministic sequenced chain with checkpoints (built). Autonomous-agent variant deferred until all 5 skills are hardened.
- LinkedIn post cadence: one per skill ship vs. batch recap.
- Notion mirror structure for the build artifacts.
