---
name: candidate-sourcing-ranking
description: Turn any role plus its market brief into an actionable candidate sourcing plan and a live named shortlist. Use when RJ wants to source candidates, build a target list, write LinkedIn boolean strings, define an ideal candidate profile (ICP), or rank a candidate export against a role. Triggers on phrases like "source candidates for", "build boolean strings for", "who should I target for", "find candidates for [role]", "find people for this rec", "rank these candidates", "build an ICP for". Two modes. Mode A (no paid tools): ICP, boolean strings, a per-role noise filter, and an automated LinkedIn run via Chrome that returns a tiered shortlist. Mode B (Juicebox): rank a CSV export with match scores, strengths, gaps, and a "why now" trigger. Skill 3 of the Talent Intelligence Agent chain.
---

# Candidate Sourcing & Ranking

v1.2 · 2026-09-29

> v1.2 makes Mode A work for any role. The noise filter is written per search from the ICP (nothing role-specific is built in). Generic tiers. Bundled LinkedIn scripts that store results in the browser so large runs are not lost to tool output truncation. Verified location code table. Per-search output folder.

## Purpose

Convert market intel into a sourcing plan a recruiter can act on today: an Ideal Candidate Profile, copy-paste LinkedIn boolean strings, a ranked target-employer hit list, and a live named shortlist (Mode A) or a scored ranking of an export (Mode B). Skill 3 of the Talent Intelligence Agent chain. Pairs with the Talent Map brief (Skill 1) and the target company list (Skill 2).

## Two modes

- **Mode A (no paid tools), default.** ICP, booleans, filter, target-employer list, then **runs the searches itself** via Claude in Chrome on RJ's logged-in LinkedIn and returns a deduped, tiered named shortlist with a textured floor. Can stop at the booleans for RJ to run manually if Chrome is not available.
- **Mode B (with Juicebox / PeopleGPT).** Ingests a Juicebox CSV export. Ranks each candidate against the role. Run Juicebox once with RJ to capture the export column format before relying on this mode.

## Inputs

Required:
- Role title and location
- Either a Talent Map brief (preferred) or the job description, enough to infer the ICP

Optional:
- Seniority target, comp band, must-haves vs nice-to-haves
- Target company list (Skill 2)
- Companies to exclude
- Mode B only: path to the Juicebox CSV export

## Process: Mode A

1. **Read the inputs.** Pull the market brief's common backgrounds, ecosystem map, supply triggers, and tiered sizing, and the job description's must-haves and named sub-specialties.

2. **Write the ICP**: must-haves, strong signals, adjacent pools, alternate pool, disqualifiers, and the level read. Disqualifiers must name the look-alikes for this role (titles that share keywords but are a different job).

3. **Write boolean strings, precision-first.** Order queries by how specific the term is to the work, not by how obvious it is.
   - **Lead with high-precision phrases**: the narrow titles or terms only real practitioners use. These return short, dense result sets.
   - **Demote broad category phrases to last resort.** They return many pages of mostly off-target people. Run them only to catch stragglers.
   - Layer the tiers: **Tier 1 direct**, **Tier 2 adjacent**, **Tier 3 alternate pool** (academic and publication signal for research roles; search firms and agencies for business roles; career switchers or bootcamps where they apply).
   - Write two versions: exact phrases for LinkedIn basic, and full parenthesized strings for LinkedIn Recruiter. Add a Past company facet line for the layoff and poaching pools from Skill 2.

   Examples of precision ordering:
   - Generative audio ML: lead with `"music information retrieval"`, `"neural audio"`, `"source separation"`; demote `"generative AI"`.
   - Enterprise AE: lead with `"strategic account executive"`, `"named accounts"`; demote `"account executive"`.

3b. **Write the noise filter for this search.** Keyword search matches anywhere in a profile, so most results are off-target. Write four lines from the ICP and record them in the plan's "Filter used" section:
   - **SIGNAL**: the specialty terms a qualified headline contains.
   - **ROLE**: the job family terms it must also contain.
   - **EXCLUDE**: the look-alikes from the disqualifiers.
   - **BROAD**: which queries are last-resort.

   A person is **kept** when the headline matches SIGNAL and ROLE and not EXCLUDE. People who recur across 2 or more precise queries without a headline signal go to a **"check profile"** list. Everyone else is dropped. Rank by recurrence, not raw hit count.

4. **Build the target-employer hit list** from Skill 2 (or the Step 1 ecosystem map): employer, fit, why now, sourcing note.

5. **List "why now" triggers** to time outreach: layoffs, reorgs, contract or fixed-term roles, vesting and bonus timing, graduation and conference cycles, competing searches.

6. **State the coverage expectation** before running, so the result can be checked against the Skill 1 estimate.

7. **Run the automated LinkedIn search** (below).

8. **Tier the kept names by hand.** Read each kept headline and place it in Tier 1, 2, or 3, or drop it. The filter narrows the list; judgment sets the tiers. Mark seniority reads ("likely above level, referral source"). Leave out anyone whose headline states a leave, sabbatical, or health situation, and never record the reason beyond "on a stated leave."

9. **Save** to the search folder as `Sourcing-Plan-<Role>-<Location>.md` with version and date.

## Mode A: automated LinkedIn run (Chrome)

Read-only. Never click into profiles, connect, follow, or message during this run.

1. **Open a tab** (`tabs_context_mcp`, then `tabs_create_mcp`). Confirm RJ is logged in by loading any people search.
2. **Location code.** Look it up in `references/geo-urns.md`. If it is not there, resolve it with the procedure in that file, confirm the first page shows the right location, and add it to the table.
3. **Load the helper.** Read `scripts/linkedin-setup.js` and run its contents once with `javascript_tool`. It stores the page extractor in the browser and clears old results.
4. **Run each query**, precision-first. For each page, in one `browser_batch`: `navigate` to
   `https://www.linkedin.com/search/results/people/?keywords=<URL-encoded phrase>&geoUrn=%5B%22<geoUrn>%22%5D&origin=FACETED_SEARCH&page=<n>`
   then `javascript_tool` with `await (new Function(localStorage.getItem('tia_fn')))()`. Batch 5 to 10 pages per call. Each call returns only a short count line; results accumulate in the browser.
5. **Paginate** until a page returns 0 or precision drops to noise. Basic search caps at about 100 results per query. Pages with fewer than 10 people usually mean unnamed out-of-network "LinkedIn Member" results, which the extractor skips.
6. **Report.** Read `scripts/linkedin-report.js`, replace the four filter lines with this search's filter from step 3b, run it with `javascript_tool`, then call `get_page_text` on the same tab. It returns the per-query table, kept names, broad-only kept names, and the check-profile list. (Do not return the report through `javascript_tool` itself; its output is truncated at about 1,000 characters.)
7. **Saturation.** Stop when precise queries stop adding new kept names. If the last query still added names, say the count is a floor.
8. **Clean up.** Run `localStorage.removeItem('tia_rows'); localStorage.removeItem('tia_fn')` and close the tab.

### LinkedIn basic account limits

- **No parenthesized grouping.** `( ... AND ... )` returns no results on a basic account. Use exact phrases or a simple two-term `AND`. Full nested strings are for LinkedIn Recruiter.
- **No total result count** and a cap of about 100 per query. Report a named shortlist and a floor, not a census.
- **A wrong geoUrn silently returns zero.** Use only verified codes.
- For a true qualified count, escalate to LinkedIn Recruiter or Mode B.

## Process: Mode B

1. Load the Juicebox CSV. Confirm columns (name, title, company, location, profile URL, tenure).
2. Score each candidate 0 to 100 against the ICP: skills, company pedigree, seniority, location.
3. For each: top 2 strengths, top 1 or 2 gaps, and a "why now" trigger if detectable.
4. Sort by score. Flag the top tier for outreach (Skill 4).
5. Save to the search folder as `Candidate-Ranking-<Role>-<Location>.md`.

## Output structure (Mode A)

1. **Ideal Candidate Profile.** Must-haves, strong signals, adjacent pools, disqualifiers, level read.
2. **Boolean strings.** LinkedIn basic phrases (as run) and LinkedIn Recruiter strings, by tier, plus Past company facet lines.
3. **Target-employer hit list.** Top employers with why now, linked to Skill 2.
4. **"Why now" triggers.**
5. **Coverage.** Per-query table (pages, profiles read, new kept names), the filter used, what the run found, and how the live floor compares to the Skill 1 estimate.
6. **Live named shortlist.** Tier 1, Tier 2, Tier 3 tables (name, headline, location, note), a check-profile list, and a "left off on purpose" list with counts and reasons.
7. **Next step.** Outreach status.

## Quality bar

- Every boolean string is copy-paste ready. No placeholders left.
- The filter used is written in the plan so RJ can check what was kept and dropped.
- The ICP ties back to the market brief and the job description.
- Target employers are named, not generic.
- A recruiter who has never seen the role could run the plan unaided.
- RJ-facing text follows her writing rules: no em or en dashes, plain declarative sentences.

## Examples (not defaults)

- Machine Learning Scientist (generative audio/music), Boston, for a Series-D AI startup. Mode A. `outputs/Sourcing-Plan-ML-Scientist-Audio-Boston.md`. Research role; Tier 3 is the academic pipeline.

## Future iterations

- Citation-graph mining for research roles: co-authors of known target-company papers.
- Cross-reference against people RJ has already contacted (dedupe).
- Auto-handoff Tier 1 to Skill 4 (Voice-Matched Outreach).
- Capture and lock the Juicebox export schema on first Mode B run.
