---
name: talent-map
description: Generate a structured talent market intelligence brief for any role and location. Use when RJ wants to understand the talent market before opening a search, briefing a hiring manager, or evaluating a target company. Triggers on phrases like "talent map for [role]", "map the talent for", "market read for [role]", "talent intel on", "what's the market for [role]", "supply demand for [role]", "build a market brief". Outputs a market brief with tiered pool sizing, a local ecosystem map, comp benchmarks including live posted pay ranges, competing openings, common backgrounds, supply and demand signal, and 5 actionable insights for the hiring manager. Skill 1 of the Talent Intelligence Agent chain.
---

# Talent Map

v1.2 · 2026-09-29

> v1.2 adds the live job board check (verified pay ranges and competing openings), location packs instead of built-in New York sources, and the per-search output folder.

## Purpose

Produce a structured talent market intelligence brief for a role and location. Defensible in front of a hiring manager. Foundation for the rest of the sourcing strategy.

Whenever the pool is specialized or thin, the brief must answer the hiring manager's real question: **"How many qualified people are actually here, and where do they sit?"** That needs a Local Talent Ecosystem Map and a tiered, calibrated pool estimate, not a single global number.

## Inputs

Required:
- Role title
- Location (a metro, or "remote US")

Optional (the orchestrator's Step 0 intake fills these from a job link):
- Hiring company and the posting's pay range
- Seniority, must-haves, named sub-specialties
- Company stage focus

## Process

1. **Web research.** Run parallel searches:
   - "[Role] [Location] salary [year]"
   - "[Role] [Location] hiring demand [year]"
   - "[Role] role definition responsibilities" (only if the role is non-standard)
   - Recent layoffs, reorgs, or funding in the employers that hold this talent (supply and demand triggers)

2. **Live job board check.** Run `python3 scripts/job_board_scan.py --title "<regex of title variants>" [--location "<regex>"]`. It reads every job on the boards in `scripts/boards.txt` (Ashby, Greenhouse, Lever) and returns matching openings with posted pay ranges and dates.
   - Use the results as **verified** comp benchmarks and as the list of **competing openings** for the same people.
   - Run it twice when useful: once for the exact role, once for the nearest comparable titles.
   - If the hiring company or a key competitor is missing from `boards.txt`, add it (`platform:slug`) and rerun.

3. **Triangulate comp** from 3+ sources. Posted ranges from step 2 come first. Then Levels.fyi, Glassdoor, Built In, and specialist firm salary guides relevant to the function.

4. **Build the Local Talent Ecosystem Map.** Find the actual employers, labs, agencies, and groups *in the target location* that hold this talent. Name them in a table with their focus and why they matter (direct fit vs adjacent). For thin pools, enumerate the named employer set. Use the general sources plus the matching pack in `references/location-packs.md`.

5. **Size the pool in tiers, calibrated to data.** Give:
   - **Direct fit** = people in the location now who can do the exact work, and the *available* slice of that.
   - **Adjacent fit** = people in related specialties who could cross over, and the movable slice.
   - **Alternate pool** = the role's non-obvious source (academic for research roles; search firms and agencies for business roles; career switchers where they apply).
   - State the binding constraint (usually the location) and how the pool changes if it is relaxed.
   - Label every estimate as inferred from the employer set, not a roster count. The named floor comes from Skill 3. Thin data means "seems like about X, directional," never "there are exactly X."

6. **Synthesize** into the output structure below. Cite every number.

7. **Save** to the search folder as `Market-Brief-<Role>-<Location>.md` with version and date. Standalone runs with no search folder: create one as described in the orchestrator's Step 0.

## General sources

Levels.fyi, Glassdoor, Built In (city edition), public job postings and the live job board check, company careers pages, news and funding coverage, SEC filings and state WARN notices for layoffs, and specialist salary guides for the function. Add the location pack for the search's metro.

## Output structure

### 1. Headline read
3 to 4 sentences. Tight or loose market, why, and what it means for the hiring strategy. Name any competing search found in step 2.

### 2. Market sizing
- Tiered, calibrated estimate (direct fit, available slice, adjacent fit, alternate pool). Never a single bare number.
- The binding constraint and how the pool changes if it is relaxed.
- Live demand: competing openings from the job board check, with the scan's scope stated (for example "33 boards scanned, not a census").

### 2.5 Local Talent Ecosystem Map
- Table: Employer or group | Type | Direct fit vs adjacent | Why it matters.
- For thin pools, the full named employer set.

### 3. Comp benchmarks
- Table of posted ranges from the job board check (company, role, range, date).
- Percentiles from aggregate sources where available.
- A one-line read on where the hiring company's range sits.

### 4. Common backgrounds
- Top prior titles, top prior employers, education or training profile, years of experience.

### 5. Supply and demand signal
- Verdict: tight, balanced, or loose, with reasoning.
- Supply triggers (layoffs, reorgs, vesting cliffs, graduation cycles).
- Demand triggers (funding, competing searches, market shifts).

### 6. Top 5 insights for the hiring manager
Each: a one-sentence headline, two supporting sentences, and one concrete action for this week.

### 7. Sources
URLs with publication or fetch dates.

## Quality bar

- Every number is cited. Posted pay ranges are labeled as pulled live with the date.
- Comp ranges are triangulated from 3 or more sources.
- A hiring manager can read it in 4 minutes and walk away with 3 specific actions.
- RJ-facing text follows her writing rules: no em or en dashes, plain declarative sentences.

## Examples (not defaults)

- GTM AI Engineer, New York, Series A to C AI startups: `outputs/Market-Brief-GTM-AI-Engineer-NY.md`.
- Machine Learning Scientist (generative audio/music), Boston, for a Series-D AI startup: `outputs/Market-Brief-ML-Scientist-Audio-Boston.md`. Thin-pool ecosystem map and tiered sizing.

## Future iterations

- Auto-count active postings per city from Built In.
- LinkedIn job count via Claude in Chrome.
- Grow `boards.txt` into a categorized list (AI, fintech, consumer, enterprise) so scans can target a sector.
