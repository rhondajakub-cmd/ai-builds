---
name: talent-intelligence-agent
description: Run the full Talent Intelligence Agent end-to-end from a single command — market intel, target companies, candidate sourcing, and outreach — and assemble one talent intelligence brief a recruiter could pick up. Use when RJ wants the whole run, not one skill at a time. Triggers on phrases like "run the talent intelligence agent for", "run my talent intelligence agent", "full talent intelligence run for", "source [role] in [location] end to end", "give me a complete talent intelligence brief for". Inputs: role + location (+ optional company archetype/target company). This is the orchestrator (Skill 5) of the Talent Intelligence Agent chain.
---

# Talent Intelligence Agent (Orchestrator)

v1.0 · 2026-06-10

## Purpose

One command runs the Talent Intelligence Agent chain end-to-end and assembles a single **Sourcing Brief** any recruiter could pick up. Sequences the building-block skills, passes each one's output into the next, and stitches the results into one document. Skill 5 of the Talent Intelligence Agent chain.

## Architecture decision (resolved)

v1 is a **deterministic sequenced skill chain**, not an autonomous agent. Each step is an explicit skill call with a checkpoint between, so RJ can inspect/adjust between stages and the run is reproducible. (The autonomous-agent option from the architecture's open decisions is deferred — revisit once all 5 skills are hardened.)

## Inputs

Required:
- Role title
- Location

Optional:
- Company archetype (for Skill 2) or a specific target company (e.g. a specific startup)
- Seniority, comp band, companies to exclude
- Relocation allowed? (changes pool sizing and candidate geo)

## The chain

| Step | Skill | Status | Produces |
|---|---|---|---|
| 1 | `talent-map` | ✅ built | Market brief: sizing, comp, ecosystem map, tiered pool estimate |
| 2 | `target-company-builder` | ✅ built | Ranked target/poaching company list w/ funding, headcount, hiring signals |
| 3 | `candidate-sourcing-ranking` | ✅ built | ICP + booleans + **live named shortlist** (auto-run via Chrome) |
| 4 | `voice-matched-outreach` | ⬜ not built | First-touch + follow-up messages for top candidates |

## Process

1. **Run Skill 1 (Talent Map)** with role + location. Capture the market brief — especially the **ecosystem map** and **tiered pool sizing**, which feed Steps 2 and 3.
2. **Run Skill 2 (Target Company Builder)** with the company archetype + the ecosystem map from Step 1. *If unbuilt:* substitute the ecosystem map's employer list as the interim target list and flag the gap.
3. **Run Skill 3 (Candidate Sourcing & Ranking)**, feeding it the Step 1 brief and Step 2 company list. Use its automated Chrome run to produce the deduped, tiered named shortlist + textured floor.
4. **Run Skill 4 (Voice-Matched Outreach)** for the top-tier names from Step 3. *If unbuilt:* stop at the shortlist and flag outreach as the next manual step.
5. **Assemble the Sourcing Brief** (structure below), pulling the headline from each step. Cross-link the per-skill output files rather than duplicating them.
6. Save to `/Claude for Builders/10x-TA-Leader/outputs/Sourcing-Brief-[Role]-[Location].md`.

### Checkpoints
Pause after Step 1 (confirm the role framing + relocation assumption) and after Step 3 (confirm the shortlist before any outreach drafting). Never trigger outreach (Step 4) without RJ's explicit go — outreach is a send-on-RJ's-behalf action.

## Output structure — Sourcing Brief

1. **Executive summary** — the market in 2 sentences, the pool size (calibrated), and the single most important sourcing move.
2. **Market read** — headline + comp + supply/demand, linked to the Skill 1 brief.
3. **Target companies** — ranked list (or ecosystem-map interim), linked to Skill 2 output.
4. **Candidate shortlist** — tiered named list with the live count + saturation note, linked to Skill 3 output.
5. **Outreach plan** — top candidates + message status, linked to Skill 4 output (or "pending — chain incomplete").
6. **Coverage & confidence** — what's a floor vs. verified, what source/tool gaps remain, what would tighten it.

## Quality bar

- The brief stands alone: a recruiter reads the summary and knows the market, the pool, and who to contact first.
- Every number carries a confidence label (floor / estimate / verified) and its source.
- Unbuilt steps are clearly flagged as gaps, never silently skipped.
- Each section links its underlying skill output instead of duplicating it.

## Current limitation

Steps 1, 2, and 3 are built; only Step 4 (outreach) remains. A v1 run produces: market brief → enriched target-company list → live candidate shortlist → outreach flagged as pending. Skill 4 completes the chain.

## Demo case (canonical test)

- Role: Machine Learning Scientist (generative audio/music), Boston (a Series-D AI startup)
- Existing partial outputs: `Market-Brief-ML-Scientist-Audio-Boston.md` (Step 1), `Sourcing-Plan-ML-Scientist-Audio-Boston.md` (Step 3)
- A full orchestrator run would stitch these into `Sourcing-Brief-ML-Scientist-Audio-Boston.md`.

## Future iterations

- Build Skills 2 and 4 to complete the chain.
- Add the autonomous-agent variant once all skills are hardened.
- Auto-dedupe candidates against RJ's prior-contact log.
- One-run regeneration: re-run the whole chain on a cadence to catch market/candidate movement.
