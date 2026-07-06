---
name: nyc-board-agent
description: RJ's NYC Board Agent — scan VC firms' portfolio job boards for Head of People / Head of Talent / VP People / Chief People Officer / Director of Talent roles in NYC or Remote, posted in the last 60 days. Runs Tier A direct JSON APIs + Tier B Getro SSR pages + Tier D WebSearch fallback. Saves a markdown report to Desktop and drafts a Gmail summary to rhondajakub@gmail.com. Use when RJ says "run my nyc board agent", "/nyc-board-agent", "check the boards", "scan the job boards", "VC talent roles", "head of people roles", or any variation of asking for the weekly board sweep.
---

You are running RJ's on-demand VC portfolio board scan. Execute the procedure DIRECTLY — do not dispatch a subagent (the Agent tool / `vc-talent-roles` subagent type doesn't inherit MCP tools in this runtime, which breaks the Gmail draft step).

Today's date = the actual current date.

# Step 0 — Load the Gmail draft tool

The `mcp__633b08b6-1e94-433a-98dc-7e01f2881173__create_draft` tool is deferred — load its schema first:

```
ToolSearch(query="select:mcp__633b08b6-1e94-433a-98dc-7e01f2881173__create_draft", max_results=1)
```

# Step 1 — BATCH 1: Tier A direct JSON (5 parallel WebFetch calls in ONE message)

Prompt for each: *"Quote ALL job titles in this JSON with location and date field (updated_at, publishedDate, createdAt, or published_on). Include posting URL. Identify any matching: Head of People, Head of Talent, Head of People & Talent, VP of People, VP of Talent, Chief People Officer, Director of People, Director of Talent — list matches at top. If jobs array is empty, say 'no open roles'."*

URLs:
1. `https://boards-api.greenhouse.io/v1/boards/generalcatalyst/jobs?content=true`
2. `https://boards-api.greenhouse.io/v1/boards/iconiq/jobs?content=true`
3. `https://boards-api.greenhouse.io/v1/boards/batteryventures/jobs?content=true`
4. `https://api.ashbyhq.com/posting-api/job-board/firstround?includeCompensation=true`
5. `https://api.lever.co/v0/postings/indexventures?mode=json`

# Step 2 — BATCH 2: Tier B Getro portfolio (10 parallel WebFetch calls in ONE message)

Prompt for each: *"Search this page for any role whose title contains: 'Head of People', 'Head of Talent', 'VP People', 'VP Talent', 'Chief People Officer', 'Director of People', 'Director of Talent'. For each match: role title, company, location, posting date, link. If no matches, say 'no matching roles'. Then list ALL OTHER visible job titles."*

URLs:
1. `https://jobs.accel.com/jobs?functions=People`
2. `https://jobs.generalcatalyst.com/jobs?functions=People`
3. `https://indexventures.getro.com/jobs?functions=People`
4. `https://jobs.insightpartners.com/jobs?functions=People`
5. `https://jobs.khoslaventures.com/jobs?functions=People`
6. `https://jobs.lererhippeau.com/jobs?functions=People`
7. `https://jobs.primary.vc/jobs?functions=People`
8. `https://careers.redpoint.com/jobs?functions=People`
9. `https://jobs.rre.com/jobs?functions=People`
10. `https://jobs.thrivecap.com/jobs?functions=People`

# Step 3 — BATCH 3: Tier D MANDATORY WebSearch fallback (3 parallel calls in ONE message)

Tier D is REQUIRED. It's the only path to surface roles at firms with no public board (Founders Fund, Benchmark, GV, Tiger Global, Spark, FirstMark) and Consider-gated firms (a16z, Sequoia, Bessemer, etc.). The Perchwell @ Founders Fund match was caught only via Tier D.

Queries:
1. `"head of people" OR "head of talent" "New York" site:jobs.ashbyhq.com 2026`
2. `"head of people" OR "VP of people" OR "chief people officer" New York site:jobs.lever.co 2026 -recruiter`
3. `"head of people" OR "head of talent" New York site:job-boards.greenhouse.io OR site:boards.greenhouse.io 2026`

# Step 4 — Verify Tier D candidates via direct API

For each promising Tier D result, fetch the underlying API to confirm it's still live (search caches go stale). Use the slug from the URL:
- Ashby: `https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true`
- Greenhouse: `https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true`
- Lever: `https://api.lever.co/v0/postings/{org}?mode=json`

Only include roles confirmed currently posted. Log any that were in the search results but are gone now in an "Excluded after verification" section.

# Step 5 — Identify VC backers

For each verified Tier D match, run a quick WebSearch: `{company} investors series funding 2026`. Check whether the company is in the 32-firm portfolio map below. If yes → mark as 32-firm match. If no → list as "adjacent — not in 32-firm map".

**The 32 firms:** Sequoia, a16z, Accel, Benchmark, Greylock, Kleiner Perkins, Lightspeed, Bessemer, General Catalyst, Index, Founders Fund, NEA, Tiger Global, Insight Partners, Coatue, Battery, IVP, Khosla, Redpoint, Spark, Thrive, GV, Felicis, First Round, USV, FirstMark, Lerer Hippeau, RRE, Lux, Primary Venture Partners, Two Sigma Ventures, ICONIQ.

# Step 6 — Filter and aggregate

- **Title regex (case-insensitive):** `(head of (people|talent)|vp (of )?(people|talent)|chief (people|talent) officer|director of (people|talent)|people lead|talent lead)`
- **Skip:** recruiter roles, talent acquisition coordinators, people business partners, HR generalists, "head of talent acquisition"
- **Location:** NY/NYC/Remote (US)/Hybrid-with-NY only
- **Recency:** last 60 days. Flag last 7 days with 🆕
- **Dedupe:** by title+company
- **Sort:** newest first

# Step 7 — Save markdown report

Path: `~/Desktop/nyc-board-agent-{YYYY-MM-DD}.md`

Sections:
1. Headline + counts
2. `## 🆕 New this week (≤7 days)` + table
3. `## Active (8–60 days) — 32-firm portfolio` + table
4. `## Adjacent (NYC, not in 32-firm map)` + table
5. `## Excluded after verification` (with reasons)
6. `## Auto-scan coverage detail` (which boards loaded, counts of jobs visible, etc.)
7. `## Firms not auto-scanned (Consider-gated)` — list Tier 1 (top 7) + Tier 2 (others)
8. `## Firms with no public portfolio board` — Benchmark, GV, Tiger Global, Spark, FirstMark (Founders Fund caught via Tier D)
9. `## Notes` — any endpoint errors, caveats

Table columns: Posted | Company | Role | Location | VC Source | Link

# Step 8 — Create Gmail draft via MCP

Call:
```
mcp__633b08b6-1e94-433a-98dc-7e01f2881173__create_draft(
  to=["rhondajakub@gmail.com"],
  subject="NYC Board Agent — {N} active ({top-match-headline}) — {YYYY-MM-DD}",
  htmlBody="<see below>"
)
```

The subject's `{top-match-headline}` is the highest-priority match in plain English, e.g. `Perchwell @ Founders Fund`. If 0 matches, say `0 new this week`.

HTML body sections in this exact order:

1. Headline `<p>` with count + one-line summary of top match
2. `<h3>🆕 New this week (≤7 days)</h3>` + HTML `<table>` (or "None.")
3. `<h3>Active (8–60 days) — 32-firm portfolio</h3>` + HTML `<table>` with columns: Posted, Company, Role, Location, VC, Link
4. `<h3>Adjacent (NYC, but not in your 32-firm map)</h3>` + HTML `<table>` (only if any)
5. **Sticky block — paste verbatim every run:**
```
<h3>🔎 Manual 5-min scan (Tier 1 Consider boards — agent can't reach these)</h3>
<p>Cmd-click each to open in a new tab:</p>
<ul>
  <li><a href="https://portfoliojobs.a16z.com/jobs?functions=People">a16z</a></li>
  <li><a href="https://jobs.sequoiacap.com/jobs?functions=People">Sequoia Capital</a></li>
  <li><a href="https://jobs.bvp.com/jobs?functions=People">Bessemer</a></li>
  <li><a href="https://jobs.usv.com/jobs?functions=People">USV</a></li>
  <li><a href="https://jobs.greylock.com/jobs?functions=People">Greylock</a></li>
  <li><a href="https://jobs.lsvp.com/jobs?functions=People">Lightspeed</a></li>
  <li><a href="https://jobs.firstround.com">First Round (login required)</a></li>
</ul>
<p>Or right-click your "NYC Board — Tier 1" Chrome bookmark folder → "Open all (7)".</p>
```
6. `<p>Full report: <code>~/Desktop/nyc-board-agent-{YYYY-MM-DD}.md</code></p>`
7. `<p style="color:#666; font-size:12px;">Auto-scanned: 15 firms (5 Tier A + 10 Tier B) · Tier D WebSearch fallback ran · Manual scan needed: 13 Consider boards (top 7 above) · No public board: 5 firms — Founders Fund caught via Tier D</p>`

# Step 9 — Report back to RJ

After everything is done, give RJ a short confirmation message:
- Markdown file path
- Gmail draft ID (from create_draft's return value)
- Bucket counts: {X} 32-firm matches, {Y} adjacent, {Z} new this week
- Any endpoint errors

# Critical rules

- Run BATCH 1, BATCH 2, BATCH 3 each as a SINGLE message with multiple parallel tool calls. Don't sequence.
- DO NOT dispatch a subagent. Execute every step directly.
- DO NOT write a `.eml` file — only the MCP `create_draft` puts a real draft in Gmail.
- Tier D is mandatory — skipping it loses real roles (Founders Fund, a16z portfolio, etc.).
- Verify every Tier D candidate via direct API before including (search results go stale).
- If a role is excluded after verification, mention it in the "Excluded" section so RJ knows it was checked.
- Don't fabricate. Zero matches is a valid honest result.
