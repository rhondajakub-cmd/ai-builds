---
name: talent-map
description: Generate a structured talent market intelligence brief for a role + location. Use when RJ wants to understand the talent market before opening a search, briefing a hiring manager, or evaluating a target company. Triggers on phrases like "talent map for [role]", "map the talent for", "market read for [role]", "talent intel on", "what's the market for [role]", "supply demand for [role]", "build a market brief". Outputs a market brief with sizing, comp benchmarks, common backgrounds, supply/demand signal, and 5 actionable insights for the hiring manager. Skill 1 of the Talent Intelligence Agent chain.
---

# Talent Map

v1.1 · 2026-06-10

## Purpose

Produce a structured talent market intelligence brief for a role + location. Defensible in front of a hiring manager. Foundation for the rest of the sourcing strategy.

When the role is specialized or the talent pool is thin (frontier AI, generative audio, niche research), the brief must answer the hiring manager's real question: **"How many qualified people are actually here, and where do they sit?"** That requires a Local Talent Ecosystem Map and a tiered, calibrated pool estimate — not a single global number. See Process steps 4–5 and Output sections 2 + 2.5.

## Inputs

Required:
- Role title (e.g., "GTM AI Engineer")
- Location (e.g., "New York")

Optional:
- Comp band (target base, target total comp)
- Seniority (IC, Manager, Director, VP)
- Company stage focus (Seed, Series A-C, Growth, Public)

## Process

1. Run 3 parallel web searches:
   - "[Role] [Location] salary [year]"
   - "[Role] [Location] hiring demand [year]"
   - "[Role] role definition responsibilities" (only if role is non-standard)

2. Triangulate comp from 3+ sources. Approved sources include Levels.fyi, Glassdoor, Built In NYC, Betts Recruiting, Apollo, Clay, ZipRecruiter, Skaled, Clientell.

3. **Build the Local Talent Ecosystem Map.** Search for the actual employers, labs, and academic groups *in the target location* that hold this talent. Name them in a table with their audio/AI focus and why they matter (direct-fit vs. adjacent). For specialized roles, enumerate the named employer set — the pool is small enough to list.

4. **Size the pool in tiers, calibrated to data.** Do not give a single global number. Give:
   - **Direct fit** = people in the location *right now* who can do the exact work, and the *available* slice of that (most are happily employed or not looking).
   - **Adjacent fit** = people in related sub-fields (e.g., speech/ASR for a generative-audio role) who could cross over, and the movable/research-grade slice.
   - State the binding constraint explicitly. If the role allows relocation, note how much the pool grows when "in [location]" is relaxed.
   - Label every estimate as inferred from the employer set, not a roster count. Flag that a precise count requires a LinkedIn Recruiter pull (which Skill 3 produces). Follow RJ's calibration rule: thin data → "seems like ~X, directional" not "there are exactly X."

5. Synthesize into the output structure below. Cite every number.

6. Save to `/Claude for Builders/10x-TA-Leader/outputs/Market-Brief-[Role]-[Location].md` with version and date.

## Output structure

### 1. Headline read
3 to 4 sentences. Tight or loose market, why, what it means for hiring strategy.

### 2. Market sizing
- Approximate qualified candidate count in the location, given as a **tiered, calibrated estimate** (direct fit / available slice / adjacent fit / movable slice) — never a single bare number.
- The binding constraint (e.g., "in this metro") and how the pool changes if it's relaxed (relocation).
- Active job postings (national + location share).
- YoY demand change.

### 2.5 Local Talent Ecosystem Map
- Table of the actual employers, labs, and academic groups *in the target location* that hold this talent.
- Columns: Employer / lab | Focus | Direct-fit vs. adjacent | Why it matters (named people if known).
- For thin pools, enumerate the full named employer set — the goal is a hiring manager who can see exactly where the ~N people sit.

### 3. Comp benchmarks
- Base salary by percentile (25/50/75/90).
- Total comp with equity for the company stage.
- Variance vs. national median.
- 3+ cited sources.

### 4. Common backgrounds
- Top 5 prior titles candidates typically come from.
- Top 5 prior companies (high-density talent pools).
- Education profile (CS, bootcamp, self-taught split).
- Years of experience distribution.

### 5. Supply/demand signal
- Verdict: tight, balanced, loose. With reasoning.
- Supply trigger events (recent layoffs, IPOs, vesting cliffs).
- Demand trigger events (funding waves, AI boom, regulatory changes).

### 6. Top 5 insights for the hiring manager
Each insight contains:
- One sentence headline (the takeaway).
- Two sentences supporting it.
- One concrete action the hiring team should take this week.

### 7. Sources
URLs with publication date where available.

## Quality bar

- Every number is cited.
- Comp ranges are triangulated from 3 or more sources.
- Hiring manager can read it in 4 minutes and walk away with 3 specific actions.
- Brief is defensible in a live interview run-through.

## Demo case (canonical test)

- Role: GTM AI Engineer
- Location: New York
- Stage: Series A-C AI startup
- Demo output: `/Claude for Builders/10x-TA-Leader/outputs/Market-Brief-GTM-AI-Engineer-NY.md`

### Thin-pool example (v1.1 ecosystem map + tiered sizing)

- Role: Machine Learning Scientist (generative audio/music)
- Location: Boston
- Target company: a Series-D AI startup (Cambridge, MA)
- Output: `/Claude for Builders/10x-TA-Leader/outputs/Market-Brief-ML-Scientist-Audio-Boston.md`
- Demonstrates the Local Talent Ecosystem Map + tiered, calibrated pool sizing for a scarce specialized role.

## Future iterations

- Add automatic Built In NYC scrape for active postings count.
- Add Tech:NYC member overlap (which member companies are hiring this role?).
- Add LinkedIn job count via Claude in Chrome navigation.
- Add NYC Startup Job Board (Airtable) row count for the role across the 1,574 active jobs.
