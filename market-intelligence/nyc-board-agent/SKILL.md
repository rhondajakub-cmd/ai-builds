---
name: nyc-board-agent
description: RJ's NYC Board Agent — scan VC firms' portfolio job boards for senior People/Talent/Recruiting leadership roles (Head of Talent Acquisition [primary target], Head of People, Head of Talent, VP/Director of Talent Acquisition, Head of Recruiting, VP People, Chief People Officer, Director of People/Talent) in NYC or Remote, posted in the last 60 days. Runs Tier A direct JSON APIs + Tier B Chrome-rendered Getro boards (People & HR + Director filter) + Tier D WebSearch fallback. Saves a markdown report to Desktop and drafts a Gmail summary to your-email@example.com. Use when RJ says "run my nyc board agent", "/nyc-board-agent", "check the boards", "scan the job boards", "VC talent roles", "head of people roles", or any variation of asking for the weekly board sweep.
---

You are running RJ's on-demand VC portfolio board scan. Execute the procedure DIRECTLY — do not dispatch a subagent (the Agent tool / `vc-talent-roles` subagent type doesn't inherit MCP tools in this runtime, which breaks the Gmail draft step).

Today's date = the actual current date.

# Step 0 — Load tools (Gmail draft + Chrome MCP for Tier B)

Both are deferred — load them first:

```
ToolSearch(query="select:mcp__633b08b6-1e94-433a-98dc-7e01f2881173__create_draft", max_results=1)
ToolSearch(query="select:mcp__claude-in-chrome__list_connected_browsers,mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__tabs_create_mcp", max_results=6)
```

Then call `mcp__claude-in-chrome__list_connected_browsers`. If it returns a browser, Tier B (Step 2) uses Chrome rendering (accurate). If it returns nothing, Tier B falls back to WebFetch and MUST be flagged as degraded (see Step 2) — Getro's filter only works with a JS-rendering browser.

# Step 1 — BATCH 1: Tier A direct JSON (5 parallel WebFetch calls in ONE message)

Prompt for each: *"Quote ALL job titles in this JSON with location and date field (updated_at, publishedDate, createdAt, or published_on). Include posting URL. Identify any matching senior People/Talent/Recruiting leadership: Head/VP/Director of Talent Acquisition, Head of Recruiting, Head/VP/Director of People, Head/VP/Director of Talent, Chief People Officer, CHRO, Director of People Operations, People/Talent Lead — list matches at top. If jobs array is empty, say 'no open roles'."*

URLs:
1. `https://boards-api.greenhouse.io/v1/boards/generalcatalyst/jobs?content=true`
2. `https://boards-api.greenhouse.io/v1/boards/iconiq/jobs?content=true`
3. `https://boards-api.greenhouse.io/v1/boards/batteryventures/jobs?content=true`
4. `https://api.ashbyhq.com/posting-api/job-board/firstround?includeCompensation=true`
5. `https://api.lever.co/v0/postings/indexventures?mode=json`

# Step 2 — Tier B: Getro portfolio boards (Chrome-rendered, filtered)

**Critical:** Getro applies its function/seniority filter in client-side JS. A plain WebFetch of a filter URL returns an UNFILTERED SSR slice — this is the bug that caused past runs to miss every People role. Render these boards in Chrome instead.

**The correct filter** is a base64 `?filter=` param, NOT `?functions=`. Use the People & HR + Director filter (verified working 2026-07-13):
`?filter=eyJqb2JfZnVuY3Rpb25zIjpbIlBlb3BsZSAmIEhSIl0sInNlbmlvcml0eSI6WyJkaXJlY3RvciJdfQ%3D%3D`
(decodes to `{"job_functions":["People & HR"],"seniority":["director"]}`). Getro's seniority taxonomy tops out at **"director"**, which rolls up VP / Head of / Chief / Sr Director — so this single filter catches all leadership People/Talent titles. The old param value `"People"` does not exist in Getro's taxonomy (the real label is `"People & HR"`) and returns zero.

**If a browser is connected (from Step 0):** create one MCP tab, then for EACH board below, sequentially: `navigate` to `{board}/jobs?filter=<the base64 above>` → wait ~3s for hydration → `read_page` (ref the job-results `<main>`, or `get_page_text`). Extract every role: title, company, location, "Posted: N days/months", and the job link. These lists are already function+seniority-filtered (typically 10–40 rows/board) — hand them to Step 6 for title/location/recency filtering. If a board shows a suspiciously low count, re-run it with function-only (`?filter=eyJqb2JfZnVuY3Rpb25zIjpbIlBlb3BsZSAmIEhSIl19%3D%3D`).

**If NO browser is connected:** fall back to WebFetch of each board's plain `/jobs` URL, extract what titles you can, and in the report's Notes + email flag **"Tier B DEGRADED — Getro JS filter unavailable this run; People roles likely undercounted. Connect Chrome and re-run, or use the manual-scan links."** Lean harder on Tier D.

Boards (all Getro; the base64 filter is board-agnostic — same string works on every one):
1. `https://jobs.accel.com`
2. `https://jobs.generalcatalyst.com`
3. `https://indexventures.getro.com`
4. `https://jobs.insightpartners.com`
5. `https://jobs.khoslaventures.com`
6. `https://jobs.lererhippeau.com`
7. `https://jobs.primary.vc`
8. `https://careers.redpoint.com`
9. `https://jobs.rre.com`
10. `https://jobs.thrivecap.com`

# Step 3 — BATCH 3: Tier D MANDATORY WebSearch fallback (3 parallel calls in ONE message)

Tier D is REQUIRED. It's the only path to surface roles at firms with no public board (Founders Fund, Benchmark, GV, Tiger Global, Spark, FirstMark) and Consider-gated firms (a16z, Sequoia, Bessemer, etc.). The Perchwell @ Founders Fund match was caught only via Tier D.

Queries:
1. `"head of talent acquisition" OR "head of talent" OR "head of people" "New York" site:jobs.ashbyhq.com 2026`
2. `"head of talent acquisition" OR "VP talent acquisition" OR "head of recruiting" OR "chief people officer" New York site:jobs.lever.co 2026`
3. `"head of talent acquisition" OR "head of people" OR "director of talent" New York site:job-boards.greenhouse.io OR site:boards.greenhouse.io 2026`

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

**Scope = all senior People / Talent / Recruiting leadership** (Director-level and up). **Head of Talent Acquisition is a PRIMARY target** — do NOT skip it. Widened per RJ 2026-07-13.

- **INCLUDE** when the title has BOTH (a) a leadership marker — `head of | chief | vp | vice president | director | sr director | senior director | chro | cpo | chief people officer | chief talent officer` — AND (b) a people-function marker — `people | talent | talent acquisition | recruit | recruiting | human resources | people & culture | people ops`. This captures: Head/VP/Director of Talent Acquisition, Head of Recruiting, Head/VP/Director of People, Head/VP/Director of Talent, CPO/CHRO, Director People Operations, Sr Director People Business Partner, People/Talent Lead.
- **SKIP:** individual-contributor recruiters/sourcers; anything with `coordinator` or `sourcer`; bare `manager` titles with no Head/Director/VP/Chief (e.g. "Recruiting Manager", "TA Manager", "Senior Manager, X" — unless it also says Head of/Director); and clearly non-People roles that slip through the Getro filter (`chief of staff`, `facilities`, `executive assistant`, medical/clinical supervisors).
- **Note on Tier B seniority:** the base64 filter uses Getro seniority `"director"` (Getro's TOP tier — rolls up VP / Head of / Chief). So every leadership People/Talent/TA title appears in the filtered list; this INCLUDE rule keeps the leadership rows and drops IC/coordinator/manager noise.
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
  to=["your-email@example.com"],
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
  <li><a href="https://portfoliojobs.a16z.com/jobs?filter=eyJqb2JfZnVuY3Rpb25zIjpbIlBlb3BsZSAmIEhSIl0sInNlbmlvcml0eSI6WyJkaXJlY3RvciJdfQ%3D%3D">a16z</a></li>
  <li><a href="https://jobs.sequoiacap.com/jobs?filter=eyJqb2JfZnVuY3Rpb25zIjpbIlBlb3BsZSAmIEhSIl0sInNlbmlvcml0eSI6WyJkaXJlY3RvciJdfQ%3D%3D">Sequoia Capital</a></li>
  <li><a href="https://jobs.bvp.com/jobs?filter=eyJqb2JfZnVuY3Rpb25zIjpbIlBlb3BsZSAmIEhSIl0sInNlbmlvcml0eSI6WyJkaXJlY3RvciJdfQ%3D%3D">Bessemer</a></li>
  <li><a href="https://jobs.usv.com/jobs?filter=eyJqb2JfZnVuY3Rpb25zIjpbIlBlb3BsZSAmIEhSIl0sInNlbmlvcml0eSI6WyJkaXJlY3RvciJdfQ%3D%3D">USV</a></li>
  <li><a href="https://jobs.greylock.com/jobs?filter=eyJqb2JfZnVuY3Rpb25zIjpbIlBlb3BsZSAmIEhSIl0sInNlbmlvcml0eSI6WyJkaXJlY3RvciJdfQ%3D%3D">Greylock</a></li>
  <li><a href="https://jobs.lsvp.com/jobs?filter=eyJqb2JfZnVuY3Rpb25zIjpbIlBlb3BsZSAmIEhSIl0sInNlbmlvcml0eSI6WyJkaXJlY3RvciJdfQ%3D%3D">Lightspeed</a></li>
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
