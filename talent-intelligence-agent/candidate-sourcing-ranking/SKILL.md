---
name: candidate-sourcing-ranking
description: Turn a role + market brief into an actionable candidate sourcing plan. Use when RJ wants to source candidates, build a target list, write LinkedIn boolean strings, define an ideal candidate profile (ICP), or rank a candidate export against a role. Triggers on phrases like "source candidates for", "build boolean strings for", "who should I target for", "find candidates for [role]", "rank these candidates", "build an ICP for". Two modes — Mode A (no paid tools): ICP + boolean strings to paste into LinkedIn. Mode B (Juicebox): rank a CSV export with match scores, strengths, gaps, and a "why now" trigger. Skill 3 of the Talent Intelligence Agent chain.
---

# Candidate Sourcing & Ranking

v1.1 · 2026-06-10

> v1.1 adds: precision-first boolean ordering + a noise filter (Process step 3), and an automated Chrome-driven LinkedIn run so Mode A executes as one command instead of manual paste-and-count.

## Purpose

Convert market intel into a sourcing plan a recruiter can act on today. Produces an Ideal Candidate Profile (ICP), copy-paste LinkedIn boolean strings, a ranked target-employer hit list, and — when a candidate export is available — a scored candidate ranking. Skill 3 of the Talent Intelligence Agent chain. Pairs directly with the Talent Map brief (Skill 1) and the target company list (Skill 2).

## Two modes

- **Mode A (no paid tools) — default.** Generates the ICP + boolean strings + target-employer list, then **runs the searches itself** via Claude-in-Chrome on RJ's logged-in LinkedIn (see "Mode A — automated LinkedIn run") to return a deduped, tiered named shortlist + textured floor. Can also stop at the booleans for RJ to run manually if Chrome isn't available.
- **Mode B (with Juicebox / PeopleGPT).** Ingests a Juicebox CSV export. Ranks each candidate against the role with a match score, strengths, gaps, and a "why now" trigger. Run Juicebox once with RJ to capture the export column format before relying on this mode.

## Inputs

Required:
- Role title + location
- Either: a Talent Map brief (preferred), or enough context to infer the ICP

Optional:
- Seniority target, comp band, must-have vs. nice-to-have skills
- Mode B only: path to the Juicebox CSV export
- Companies to exclude (already-applied, off-limits, current employer)

## Process — Mode A

1. **Read the market brief** (Skill 1 output) if one exists. Pull the common-backgrounds, ecosystem map, and supply/demand triggers — they feed the ICP and boolean directly.
2. **Write the ICP**: must-haves, strong signals, adjacent-pool entry points, disqualifiers, and the seniority/level read.
3. **Write boolean strings — precision-first.** Order queries by how *specific* the term is to the work, not by how obvious. Narrow technical phrases are the signal; broad category phrases are mostly noise.
   - **Lead with high-precision technical phrases** — the niche terms only real practitioners use (for generative audio: `"music information retrieval"`, `"neural audio"`, `"source separation"`, `"text-to-speech"`, `"audio codec"`). These return short, dense result sets.
   - **Demote broad category phrases to last resort** — e.g. `"music generation"`, `"generative AI"`. They return many pages of mostly-irrelevant matches (students, generic AI engineers). Run them only to catch stragglers, never as the primary query.
   - Then layer the tiers: **Tier 1 direct** (exact-profile phrases), **Tier 2 adjacent** (crossover pools from the ecosystem map), **Tier 3 academic** (PhD/publication signal).
   - Each string is one paste-ready line. Note the LinkedIn surface (basic vs. Recruiter) and any title/company/school facets. Reserve parenthesized booleans for the Recruiter paste only (basic search rejects them — see constraints below).
3b. **Apply the noise filter.** Keyword search self-selects junk. Auto-discard a result unless its headline carries a genuine audio/ML-research signal. **Drop** titles that are: "student" with no research/internship signal, "designer," "sales/recruiter/PM" (unless explicitly audio-research), or generic "AI Engineer / ML Engineer" with **no** audio/music/speech/DSP keyword. **Keep** anything with audio/music/speech/DSP + research/scientist/diffusion/model signal. The qualified pool is the **set of names that recur across ≥2 precise queries** — rank by recurrence, not by raw hit count.
4. **Build the target-employer hit list** from the ecosystem map: rank employers by talent density and approachability, with a sourcing note per employer.
5. **List "why now" triggers** to time outreach (layoffs, reorgs, vesting cliffs, paper-acceptance windows, graduation cycles).
6. **State the realistic headcount expectation** the booleans should return, so RJ can sanity-check coverage against the Skill 1 estimate.
7. Save to `/Claude for Builders/10x-TA-Leader/outputs/Sourcing-Plan-[Role]-[Location].md` with version + date.

## Process — Mode B

1. Load the Juicebox CSV. Confirm columns (name, title, company, location, profile URL, tenure, etc.).
2. Score each candidate 0–100 against the ICP: skills match, company-pedigree match, seniority fit, location fit.
3. For each, write: top 2 strengths, top 1–2 gaps, and a "why now" trigger if detectable (recent layoff, acquisition, IPO/vesting, tenure milestone, leadership change).
4. Sort by score. Flag the top tier for immediate outreach (hands off to Skill 4: Voice-Matched Outreach).
5. Save ranked output to `/Claude for Builders/10x-TA-Leader/outputs/Candidate-Ranking-[Role]-[Location].md`.

## Running booleans on LinkedIn (basic-account constraints)

Validated 2026-06-10 on RJ's logged-in basic account via Chrome. These are hard limits — design booleans around them:

- **No parenthesized grouping.** `( ... AND ... )` returns "No results found" on a basic account — grouping is Recruiter/Sales Navigator only. Use **exact phrases** (`"generative audio"`) or a simple two-term `AND` (`audio AND diffusion`). The full Tier-1 nested string is for paste into LinkedIn Recruiter, not basic search.
- **No total result count.** Basic people search shows results + pagination (10/page) but no "X results" number, and caps at ~100. Count by paginating; report a textured floor, not a census.
- **Keyword match is noisy.** Phrase/AND queries surface many non-fits (students, generic AI engineers). The real signal is the **small set of qualified people who recur across multiple precise queries** — track names, not raw counts.
- **Geo via the Locations filter UI**, then reuse the `geoUrn` from the resulting URL. Verify it returns results with a single working keyword first (a bad geoUrn silently zeroes everything — e.g., Greater Boston is `90000007`, not `90000383`).
- For a true qualified count, escalate to LinkedIn Recruiter or a Mode B tool (Juicebox) — basic search gives a named shortlist, not a number.

## Mode A — automated LinkedIn run (Chrome)

Runs the precision queries against RJ's logged-in LinkedIn via the Claude-in-Chrome tools, so Mode A executes end-to-end instead of RJ pasting and counting by hand. Deterministic procedure:

1. **Open a tab** (`tabs_context_mcp` → `tabs_create_mcp`). Confirm RJ is logged in by loading `linkedin.com/feed` or any `keywords=` search.
2. **Resolve the geoUrn once.** Navigate to a people search with one plain keyword (e.g. `keywords=audio`), open the **Locations** filter, type the metro, select it, Show results, then read the `geoUrn` out of the resulting URL. Cache it for the run (Greater Boston = `90000007`). Never trust a guessed geoUrn — a bad one silently returns zero.
3. **Run each precision query** by navigating to:
   `https://www.linkedin.com/search/results/people/?keywords=<URL-encoded phrase>&geoUrn=%5B%22<geo>%22%5D&origin=FACETED_SEARCH`
   Use exact phrases (quotes encoded as `%22`). Lead with the high-precision phrases from step 3 above; broad phrases last.
4. **Scrape with `get_page_text`** (not screenshots — faster, cleaner). Parse name + headline + location per result.
5. **Paginate** by appending `&page=2`, `&page=3`, … until the pager stops or precision drops to noise. Note total pages as a coverage signal.
6. **Apply the noise filter (step 3b)** to every scraped result. Maintain a running deduped map of kept names → {headline, which queries hit them}.
7. **Stop when queries stop adding new qualified names** (saturation) or the precise-phrase list is exhausted. If new names were still appearing on the last query, say so — the count is a floor.
8. **Tier the kept names** (strong direct-fit / adjacent / academic-pipeline) and write them into the Coverage section, with the per-query page counts and the saturation note.

Guardrails: read-only — never click into profiles, connect, follow, or message from this run. This step produces a **named shortlist + textured floor**, not a precise census (basic-account caps still apply).

## Output structure (Mode A)

### 1. Ideal Candidate Profile (ICP)
Must-haves · strong signals · adjacent-pool entry points · disqualifiers · seniority/level read.

### 2. Boolean strings (tiered, paste-ready)
Tier 1 direct · Tier 2 adjacent · Tier 3 academic. One line each, with the LinkedIn surface and facets noted.

### 3. Target-employer hit list
Ranked table: employer | fit | est. density | sourcing note.

### 4. "Why now" triggers
Timed events that make a passive candidate movable.

### 5. Coverage expectation
Rough headcount the booleans should surface; how it compares to the Skill 1 estimate; what's missed and how to close the gap.

## Quality bar

- Every boolean string is copy-paste ready — no placeholders left unfilled.
- ICP ties back to the market brief's common-backgrounds and ecosystem map.
- Target-employer list is specific and named, not generic ("AI companies").
- A recruiter who has never seen the role could run the plan unaided.

## Demo case (canonical test)

- Role: Machine Learning Scientist (generative audio/music), Boston (a Series-D AI startup)
- Mode: A
- Output: `/Claude for Builders/10x-TA-Leader/outputs/Sourcing-Plan-ML-Scientist-Audio-Boston.md`

## Future iterations

- ~~Auto-run booleans via Claude in Chrome~~ — done in v1.1 (see automated LinkedIn run).
- Citation-graph mining: pull co-authors of known target-company audio papers to catch stealth profiles keyword search misses.
- Cross-reference against people RJ has already contacted (dedupe).
- Auto-handoff top-tier matches to Skill 4 (Voice-Matched Outreach).
- Capture and lock the Juicebox export schema on first Mode B run.
