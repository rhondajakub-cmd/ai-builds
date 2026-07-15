---
name: active-search-intelligence-brief
description: >
  Weekly intelligence brief on a target list of companies RJ tracks.
  Auto-infers the pipeline from Granola meetings and Gmail threads, then scans
  for funding news, leadership changes, and product launches over the last 7 days
  per company. Drafts a Gmail email to RJ so it lands in her inbox Monday morning.
  Use when RJ says "run my search brief", "Monday search brief", "what's new with
  my interview companies", "pipeline intel", or when triggered by the scheduled
  task "Active Search Intelligence Brief" on Monday mornings.
user-invocable: true
version: v1.0 · 2026-04-23
---

# Active Search Intelligence Brief

Scan a target list of companies RJ tracks, surface material news from the past 7 days, and draft a Monday morning email brief. The goal: RJ walks into every Monday sharper on every target company, with funding context, leadership movement, and product launches already loaded.

## Critical Rules (from RJ's CLAUDE.md)

- **Accuracy.** Only present what was reported or announced. Use quotes where meaningful. Separate inferences with explicit labels: "I am inferring that..." or "Based on reporting, I suggest..." Never editorialize as fact.
- **Voice.** Peer-level, confident, matter-of-fact. No hype words, no breathless framing, no em dashes.
- **Cite everything.** Every claim gets a source link. If a claim cannot be sourced, drop it.

## Instructions

### Step 1: Build the active pipeline (auto-infer)

Pull from two sources in parallel and cross-reference.

**Granola source:**
- Call `list_meetings` for the last 30 days
- Filter to meetings where title contains "interview" OR a known recruiter / hiring manager is a participant
- Extract company names from meeting titles (e.g., "Cresta interview with Melissa Bair" → "Cresta")

**Gmail source:**
- Call `search_threads` with queries:
  - `newer_than:30d (interview OR recruiter OR "hiring manager" OR "next steps")`
  - `newer_than:30d from:(*@greenhouse.io OR *@ashbyhq.com OR *@lever.co)`
- Extract company signals from thread subjects, sender domains, and signatures

**Deduplicate and rank:**
- Merge the two lists. Dedupe by company name.
- Rank by recency of last activity (last Granola meeting date OR last email date, whichever is newer).
- Cap at **8 companies** for the brief. If more than 8, prioritize companies with activity in the last 14 days and flag overflow.
- For each company, capture: company name, latest round / stage, date of last touch, next scheduled interaction if known.

**Sanity check:** list the companies in the output as a header so RJ can confirm the auto-inference worked. If the list looks wrong on any given Monday, she can correct and re-run.

### Step 2: Research each company (past 7 days)

For each company on the list, run three targeted web searches. Scope to the last 7 days. Go deeper to 30 days only if the 7-day window returns nothing.

**Funding + financial:**
- Query: `"[Company]" funding OR raise OR series OR valuation OR acquisition 2026`
- Cross-check with Crunchbase or TechCrunch if available
- Look for: new rounds, valuation changes, M&A activity, revenue milestones, layoffs / RIFs

**Leadership changes:**
- Query: `"[Company]" "joins" OR "appointed" OR "new CEO" OR "new CRO" OR "new CHRO" OR "steps down" OR "departs"`
- Cross-check with LinkedIn company page if surfaced in results
- Prioritize: CEO, CRO, CPO, CHRO, CFO, Head of People / TA, board-level changes

**Product + launches:**
- Query: `"[Company]" launch OR announces OR unveils OR releases 2026`
- Cross-check with company blog / press room via WebFetch if needed
- Look for: major product announcements, customer wins, pricing shifts, partnership announcements

### Step 3: Filter for materiality

Not every signal makes the brief. Apply this filter:

**Include if:**
- Directly relevant to the role RJ is interviewing for (e.g., a new CHRO means her Head of TA role may change shape)
- Changes the company's trajectory (funding, layoffs, M&A)
- Gives RJ a talking point or sharper question for her next round
- Flags risk (leadership exit signaling instability, product miss, competitive loss)

**Exclude if:**
- Generic industry news not specific to the company
- Old news re-circulated
- Minor press / PR filler

If a company has zero material signals this week, note it explicitly: "Nothing material in the last 7 days." Do not pad.

### Step 4: Compose the brief

**Email structure:**

```
Subject: Search Intel Brief, [Date, e.g., April 27]

Hi RJ,

Weekly intel on your active pipeline. [N] companies covered. [M] flagged for attention.

## Flagged for attention
[0-3 items, highest priority. Each item: company, signal, why it matters in one line, link.]

## Upcoming this week
[Any interviews/rounds on your calendar for these companies in the next 7 days, with the most relevant signal to reference.]

## Full pipeline

### [Company 1] — [stage, last touch date]
- **Funding:** [one line + link] OR "Nothing material."
- **Leadership:** [one line + link] OR "Nothing material."
- **Product:** [one line + link] OR "Nothing material."
- **So what:** [one sentence, peer-level take on why this matters for RJ's process here. If nothing material, omit this line entirely.]

[Repeat per company]

---

Sources compiled from: Granola meetings (last 30d), Gmail threads (last 30d), web search (last 7d).

Missing anything? Reply with company names to add or remove.
```

**Voice checks before sending:**
- No em dashes anywhere
- No hype words ("incredible," "huge," "massive," "game-changing")
- "So what" lines are peer-level, not overeager
- Every claim has a link
- Inferences are labeled

### Step 5: Deliver

**Primary path:** create a Gmail draft addressed to `your-email@example.com`, subject per Step 4, body is the full brief in HTML-friendly formatting (preserve headers and bullets). Use `create_draft` with `to: your-email@example.com`.

**Ideal path (if sending is supported):** send the draft directly so it lands in the inbox Monday 8am. If send is not supported by the connector, the draft is in the Drafts folder and RJ can tap-send from her phone in 2 seconds.

**Backup path:** if Gmail is unavailable, create a Google Doc via `create_file` titled `Search Intel Brief — [Date]` in RJ's Drive, and print the doc link in the chat response.

### Step 6: Log

After delivery, append a one-line entry to a Google Doc called `Search Intel Brief Log`:
- Date run
- Number of companies covered
- Number of flagged items
- Any pipeline additions or removals vs last week

If the log doc does not exist yet, create it.

## Fallback: zero material signals across the board

If the 7-day window returns nothing material for any company, still send the brief. Use this abbreviated format:

```
Subject: Search Intel Brief, [Date] — Quiet Week

Hi RJ,

No material news across [N] active companies in the last 7 days. Pipeline steady.

[One-line summary per company with stage + next step, no signals.]

Reply with company names to add or remove.
```

A quiet week is valuable signal on its own. Do not manufacture news.

## Override: on-demand run

RJ may trigger this skill manually outside the Monday schedule, e.g., before a specific round. If she names a specific company, narrow scope to that single company and research the last 30 days instead of 7. Output can be chat-only (skip the email) if she asks for a quick read.
