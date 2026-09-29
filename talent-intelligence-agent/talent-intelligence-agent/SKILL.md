---
name: talent-intelligence-agent
description: Run the full Talent Intelligence Agent end-to-end for any open rec, starting from a job link, a pasted job description, or just a role and location. Produces a market brief, ranked target companies, and a live named candidate shortlist, assembled into one sourcing brief a recruiter could pick up. Use when RJ wants the whole run, not one skill at a time. Triggers on phrases like "run the talent intelligence agent for", "run my talent intelligence agent", "source this rec", "find people for this role", "run the sourcing agent on [link]", "full talent intelligence run for", "source [role] in [location] end to end". This is the orchestrator (Skill 5) of the Talent Intelligence Agent chain.
---

# Talent Intelligence Agent (Orchestrator)

v1.2 · 2026-09-29

> v1.2 makes the chain work for any rec. New Step 0 intake from a job link. Per-search output folder. Optional Google Drive handoff. Nothing role- or city-specific is built in; examples are examples only.

## Purpose

One command runs the chain end-to-end and assembles a single **Sourcing Brief** any recruiter could pick up. Sequences the building-block skills, passes each one's output into the next, and stitches the results into one document. Skill 5 of the Talent Intelligence Agent chain.

## Architecture decision (resolved)

v1 is a **deterministic sequenced skill chain**, not an autonomous agent. Each step is an explicit skill call with a checkpoint between, so RJ can inspect and adjust between stages and the run is reproducible.

## The chain

| Step | Skill | Status | Produces |
|---|---|---|---|
| 0 | Rec intake (this skill) | ✅ built | The search definition and the search folder |
| 1 | `talent-map` | ✅ built | Market brief: sizing, comp, live job board check, ecosystem map |
| 2 | `target-company-builder` | ✅ built | Ranked target company list with funding, headcount, hiring signals |
| 3 | `candidate-sourcing-ranking` | ✅ built | ICP, booleans, filter used, **live named shortlist** (Chrome) |
| 4 | `voice-matched-outreach` | ⬜ not built | First-touch and follow-up messages for top candidates |
| 5 | Assemble (this skill) | ✅ built | Sourcing Brief, plus optional Google Drive handoff |

## Step 0: Rec intake

Accept whichever RJ gives:

- **A job link.** Run `python3 scripts/rec_intake.py "<url>"`. Works for Ashby, Greenhouse, and Lever links. It returns company, title, location, comp, published date, and the full description. A company careers page with `gh_jid` needs the Greenhouse board slug; if the script exits with code 2, ask RJ to paste the description.
- **A pasted job description.** Extract the same fields by reading it.
- **Just a role and location.** Use them as given.

From the description, pull: seniority, must-haves, nice-to-haves, the functions or sub-specialties named, and anything that shapes the pool (on-site vs remote, years of experience, industry).

Then ask RJ **only** for what is still missing, in one message:
- Search geography (the posting location, a wider metro, or remote) and whether relocation is allowed.
- Companies to exclude (current employer, off-limits clients, already contacted).
- Anything about who the search is for, if it changes the brief (for example, a friend's company vs RJ's own search).

Do not ask for anything the posting already answers.

**Search folder.** Create `~/Claude for Builders/10x-TA-Leader/outputs/<Company>-<Role>-<Location>/` using short, filename-safe words (for example `Acme-ML-Scientist-Boston`). Use `Role-Location` when there is no company. Every step saves into this folder. If RJ names another location for outputs, use hers.

## Process

1. **Step 0: Rec intake** (above).
2. **Run Skill 1 (Talent Map)** with the intake fields. Capture the ecosystem map, tiered pool sizing, and the live job board check.
3. **Checkpoint 1.** Show RJ the headline read and the pool sizing, and confirm the role framing, geography, and which adjacent pools count. Wait for go.
4. **Run Skill 2 (Target Company Builder)** in talent-landscape mode with the Step 1 ecosystem map. This is research-heavy and independent of the LinkedIn run, so it can run as a background subagent while Step 3 starts.
5. **Run Skill 3 (Candidate Sourcing & Ranking)** with the Step 1 brief and the Step 2 list (or the Step 1 ecosystem map if Step 2 is still running). Use the automated Chrome run.
6. **Propagate.** If Steps 2 or 3 correct anything in the market brief (a pool estimate, an unverified fact, a new supply signal), update the market brief in the same turn and bump its version. Carry every caveat downstream.
7. **Checkpoint 2.** Show RJ the shortlist by tier before any outreach. Outreach is a send-on-RJ's-behalf action and needs her explicit go.
8. **Run Skill 4 (Voice-Matched Outreach)** for Tier 1 names once built. *Until then:* stop at the shortlist and flag outreach as the next manual step.
9. **Assemble the Sourcing Brief** (structure below) in the search folder as `Sourcing-Brief-<Role>-<Location>.md`. Link each section to its underlying file rather than duplicating it.
10. **Optional: Google Drive handoff.** Only when RJ asks for links or says go (she reviews before anything lands in Drive). Create a folder named for the search, upload each file as a Google Doc with `contentMimeType: text/markdown` in this order and with these title prefixes: `1. Sourcing Brief (start here)`, `2. Market Brief`, `3. Target Companies`, `4. Sourcing Plan and Shortlist`. Upload the market brief and target companies first, then rewrite the links inside the sourcing plan and brief to point to the Drive docs before uploading them. Share with anyone only after RJ confirms the email address.

## Output structure: Sourcing Brief

1. **Executive summary.** The market in 2 sentences, the pool size (calibrated), and the single most important sourcing move.
2. **Market read.** Headline, comp, supply and demand, linked to the Step 1 brief.
3. **Target companies.** Top 5 with one reason each, linked to Step 2.
4. **Candidate shortlist.** Count per tier and who to contact first, linked to Step 3.
5. **Outreach plan.** Status (pending until Skill 4 is built).
6. **Coverage and confidence.** A table of key figures labeled verified, floor, estimate, or not verified, with source. What would tighten it.

## Quality bar

- The brief stands alone: a recruiter reads the summary and knows the market, the pool, and who to contact first.
- Every number carries a confidence label (floor, estimate, verified) and its source.
- Unbuilt steps are flagged as gaps, never silently skipped.
- Nothing from one search (names, companies, filters) is written back into the skills.
- RJ-facing text follows her writing rules: no em or en dashes, plain declarative sentences.

## Examples (not defaults)

- GTM AI Engineer, New York, Series A to C AI startups.
- Machine Learning Scientist (generative audio/music), Boston, for a Series-D AI startup. Research role, thin pool, academic alternate pool.

## Future iterations

- Build Skill 4 (voice-matched outreach) to complete the chain.
- Autonomous-agent variant once all skills are hardened.
- Auto-dedupe candidates against RJ's prior-contact log.
- One-run regeneration on a cadence to catch market and candidate movement.
