---
name: cpo-tracker
description: |
  Track new Chief People Officer / Head of People / Head of Talent / VP People placements at tech and VC-backed companies in NY, SF, or Remote. Scrapes RJ's logged-in LinkedIn (via Chrome MCP), filters for tech + target geography, and appends results to both a Desktop markdown log and a Notion database. Use when RJ says "run my CPO tracker", "/cpo-tracker", "scan LinkedIn for new heads of people", "who's new in CPO roles", "/cpo-tracker backfill", or any variation of asking for new CPO/HoP placement signals.
user-invocable: true
model: claude-opus-4-7
---

# CPO Tracker

Two modes:

- `/cpo-tracker` — weekly forward scan (past 7 days). Fast (~5 min). Safe for the Monday 8am scheduled run.
- `/cpo-tracker backfill` — one-time historical scan going back 6 months. Slow (~60–90 min). Run manually with RJ present in case of CAPTCHA.

## Hard time + scope caps (CRITICAL — prevents runaway runs)

Past runs have hung for hours. Enforce these caps strictly:

- **Forward mode total wall-clock budget: 15 minutes.** Track elapsed time at each source boundary. If the budget is exceeded, stop, write whatever is collected, and surface "Hit 15-min cap at [source]" in the summary.
- **Per-source budget (forward):** LinkedIn Posts 5 min total (1 min per query, 5 queries) · WebSearch 3 min · LinkedIn People 3 min · Notion writes 2 min · Output 2 min.
- **Max items per source (forward):** Posts 10 cards per query (scroll once, don't load more) · People 25 results (no scrolling past first batch) · WebSearch top 10 results per query.
- **No retries.** If a page read fails or returns junk, log it and move on. Do not retry the same URL.
- **No profile click-throughs in forward mode.** That's backfill-only — re-confirm before opening any individual profile page.
- **Backfill mode budget: 90 minutes.** Same hard stop behavior.

If you find yourself about to start a step that could exceed the remaining budget, skip it and note the skip in the summary instead.

Both modes write to:
1. `~/Desktop/cpo-tracker-log.md` (single growing file, dedup by profile URL)
2. Notion database (configured in `.notion-config.local.md`)

## Preflight

Before any scrape:

1. Load Chrome MCP tools via ToolSearch if not already available.
2. `tabs_context_mcp(createIfEmpty: true)` to ensure a tab is available.
3. Navigate to `https://www.linkedin.com/feed/` and screenshot. Confirm RJ is logged in (avatar visible top right). If not, abort with: "LinkedIn not logged in — open LinkedIn and sign in, then re-run."
4. Load Notion config from `~/.claude/skills/cpo-tracker/.notion-config.local.md`. If missing or has placeholder token, write to Desktop only and report this to the user.

## Filters applied

Hard filters (drop everything else):

- **Title regex (case-insensitive):** `(chief (people|talent|hr|human resources) officer|head of (people|talent|hr)|vp,? (of )?(people|talent|hr)|chro|cpo)`
- **Location:** must contain one of `New York`, `NYC`, `Brooklyn`, `Manhattan`, `San Francisco`, `SF Bay`, `Bay Area`, `Remote`, or `United States` (Remote)
- **Industry signal:** company must be in tech-adjacent — keyword check on company description / industry field for `software`, `tech`, `AI`, `SaaS`, `fintech`, `internet`, `startup`, `venture`, `Series`, `B2B`
- **Non-English / non-US timezone signal in post:** drop if post mentions `GST`, `IST`, `SGT`, `AEST`, `BST`, or non-Latin scripts (Devanagari, CJK)
- **Promotional content:** drop if post matches `(event|webinar|conference|summit|panel|speaker spotlight|register now|join us for)`
- **Must contain announcement language:** `(joined|joining|excited to (share|announce)|thrilled to (share|announce)|next chapter|new chapter|new role|pleased to announce.{0,80}joined|appointed)` — applies to Posts only, not People search

## ⚠️ LinkedIn scraping is currently unreliable

As of 2026-05-15, Chrome MCP auto-redacts personal names and profile URLs as `[BLOCKED: Sensitive key]` and `[BLOCKED: Cookie/query string data]` in returned page text and JS results. That makes Sources 1 (LinkedIn Posts) and 3 (LinkedIn People) effectively non-productive — you can see post bodies but not author identity, which is exactly what the tracker needs.

**Run order:** start with Source 2 (WebSearch) — it's now the primary signal. Only attempt Sources 1 and 3 if WebSearch yields fewer than 3 new placements AND there is remaining budget. When attempting them, hard-cap at 90 seconds total across both: one quick page-text dump per query, no scrolling beyond the initial viewport, no profile click-throughs ever. If page text comes back with redacted names, abort the LinkedIn portion and note it in the summary.

## Source 1: LinkedIn Posts search

**Important — LinkedIn soft-flag behavior:** A complex Boolean like `("thrilled" OR "excited" OR "joining") AND ("CPO" OR "Head of People" OR ...)` consistently returns **zero results** even when matching posts exist. LinkedIn appears to soft-flag overly-complex queries. **Always run simple single-title queries in sequence**, never one combined Boolean.

Run these queries in sequence (each is its own page load):

Forward mode (past week each):
```
https://www.linkedin.com/search/results/content/?keywords=%22Chief%20People%20Officer%22&datePosted=%22past-week%22&sortBy=%22date_posted%22
https://www.linkedin.com/search/results/content/?keywords=%22Head%20of%20People%22&datePosted=%22past-week%22&sortBy=%22date_posted%22
https://www.linkedin.com/search/results/content/?keywords=%22Head%20of%20Talent%22&datePosted=%22past-week%22&sortBy=%22date_posted%22
https://www.linkedin.com/search/results/content/?keywords=%22VP%20People%22&datePosted=%22past-week%22&sortBy=%22date_posted%22
https://www.linkedin.com/search/results/content/?keywords=%22CHRO%22&datePosted=%22past-week%22&sortBy=%22date_posted%22
```

Backfill mode: run each of the above with `datePosted=%22past-month%22` once. LinkedIn caps at past month — older posts come from Source 3 (WebSearch).

Extraction per post card (use `read_page` filter=interactive then walk DOM):
- Author name + profile URL
- Author headline (the tagline under the name)
- Post timestamp + post permalink URL (the timestamp anchor href)
- Post body text (first 500 chars)
- Company name + company URL (only if the post tags a company)

Apply filters. Keep matches.

## Source 2: WebSearch — press releases and indexed appointments (primary supplement)

Run these queries in parallel via WebSearch. They surface broad-LinkedIn signal that Posts search misses — press releases, indexed LinkedIn posts, tracker pages (Intellizence, The Key Executives, HR Today), and company "about" pages announcing new leadership.

Forward mode (past week — add "past week" or current month name to query):
- `"named Chief People Officer" announcement 2026 tech startup`
- `"appointed Chief People Officer" OR "joins as Chief People Officer" 2026`
- `"new Head of People" 2026 Series A B C startup`
- `"appointed Chief Human Resources Officer" 2026 tech`
- `"Head of Talent" appointment 2026 tech`

Backfill mode (last 6 months): same queries with date hints like `"Nov 2025"`, `"Dec 2025"`, `"Jan 2026"`, etc.

Extract per result: person, role, company, date (or estimated month), source URL. Tag source type as `Web` or `Press Release`.

WebSearch surfaced 5 of 7 placements in test runs (71%) — strongest single source for broad-LinkedIn coverage. Tradeoff: 2-3 week lag for some tracker pages.

## Source 3: LinkedIn People search (discovery pool, not placement signal)

URL template (with filters baked in — tech industries + NY/SF/Remote):
```
https://www.linkedin.com/search/results/people/?keywords=%22Chief%20People%20Officer%22%20OR%20%22Head%20of%20People%22%20OR%20%22Head%20of%20Talent%22%20OR%20%22VP%2C%20People%22%20OR%20CHRO&geoUrn=%5B%22103644278%22%2C%22102277331%22%2C%22102571732%22%5D&industry=%5B%224%22%2C%2296%22%2C%226%22%5D
```

(geoUrn codes: 103644278 = United States, 102277331 = SF Bay Area, 102571732 = NY Metro. Industry codes: 4 = Software Development, 96 = Internet Publishing, 6 = Technology, Information & Internet. Codes verified by testing in the actual UI; if any return zero, fall back to the unfiltered URL and apply filters in code.)

Scroll-load the result list (forward mode: first 25 results sufficient; backfill mode: scroll until 200 results or end-of-list).

For each result row, extract:
- Name + profile URL
- Title + company
- Location
- Mutual-connections indicator (optional)

**Backfill mode only — profile verification step:**
For each candidate, click into profile, read the Experience section, keep only if current role start date is within the last 6 months. Throttle: 4–5 second delay between profile navigations. Abort if any page shows CAPTCHA / "verify your identity" / "unusual activity" — write what's collected so far, surface clear error.

## Source 4: Firm placement page WebSearch (optional supplement)

For deeper firm-tag coverage, run these per-firm queries:
- `"placed" "Chief People Officer" Plenty Search OR "One North Talent" OR "True Search" 2026`
- `"led the search" "Head of People" 2026`

Tag matches with firm name when surfaced this way.

## Firm tag annotation

After extraction, for each placement, search the post body, profile experience, or surrounding context for the firm names in `firms.md`. If a firm name appears within 100 characters of "placed", "search", "recruited", "partnered with", tag the placement as `Placed via [Firm]`. Otherwise leave untagged. Do not infer.

## Output A: Google Doc (primary)

Title: `CPO Tracker Log`

Use `mcp__27efbef5-d8a2-4af1-ad04-7bb5b311851f__search_files` with `title contains 'CPO Tracker Log' and mimeType = 'application/vnd.google-apps.document'` to find the existing doc. If it exists, you need to append to it — but the Drive MCP exposes `create_file` only (not update). Workaround: read existing content via `read_file_content`, merge new placements (dedup by source URL), and use `create_file` to write a new version (title `CPO Tracker Log YYYY-MM-DD`), then ask RJ which to keep — OR build the doc from scratch each run using all placements stored in the Desktop backup file.

Recommended pattern: keep the Desktop `.md` file as the canonical store (always read + append), and re-create the Google Doc each run as a fresh export of the full log so RJ always has one clean doc to look at.

Create with:
- `contentMimeType: text/plain` (this converts plain text to a real Google Doc, not a `.md` file)
- `textContent`: the full log formatted as plain text with section headers and numbered entries (Markdown tables don't render in Google Docs — use numbered entries with key:value lines as in the latest run)

## Output B: Desktop markdown backup

**On every run:**
- Read existing file if present, parse the placements table to find URLs already logged (dedup key = profile URL primary, post URL secondary)
- Append new entries — do not rewrite existing ones
- Update header block at the top with last-run timestamp and totals

Structure:
```
# CPO Tracker Log

Last run: YYYY-MM-DD HH:MM — [forward | backfill]
Total placements tracked: N (oldest-date — newest-date)
Source breakdown: LinkedIn profile X · LinkedIn post Y · Web/press Z

## 🆕 New this run (date-range)

| Date | Person | Role | Company | Location | Industry | Source | Firm tag |
|---|---|---|---|---|---|---|---|
| ... | [Name](profile-url) | Role | [Company](company-url) | NYC | Fintech | [Post](post-url) | Placed via X |

## Active placements — full history

Sorted most recent first, grouped by month.

### Month YYYY
- **Person** — Role, [Company](url) · Location · Industry · Started Month YYYY · [Source](url) · [Profile](url) · Firm tag

## Filtered out this run (summary)
- N posts dropped: reasons
- N profiles dropped: reasons
- Run duration · CAPTCHA count · errors
```

## Output B: Notion database

Read `.notion-config.local.md` for:
- `NOTION_TOKEN` (integration secret)
- `DATABASE_ID` (the CPO Placements database ID)

If both present, POST each new placement to Notion via API:

```bash
curl -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "'$DATABASE_ID'"},
    "properties": {
      "Name": {"title": [{"text": {"content": "Person Name"}}]},
      "Role": {"rich_text": [{"text": {"content": "Chief People Officer"}}]},
      "Company": {"rich_text": [{"text": {"content": "Company Name"}}]},
      "Date": {"date": {"start": "2026-05-14"}},
      "Location": {"select": {"name": "NYC"}},
      "Industry": {"rich_text": [{"text": {"content": "Fintech"}}]},
      "Source URL": {"url": "https://linkedin.com/..."},
      "Profile URL": {"url": "https://linkedin.com/in/..."},
      "Firm Tag": {"rich_text": [{"text": {"content": "Placed via X"}}]},
      "Source Type": {"select": {"name": "LinkedIn Post"}}
    }
  }'
```

Dedup: before POSTing, GET-query the database for matching Profile URL. Skip if already present.

If the Notion call returns 401/403/404, log the error to the markdown file's "errors" section and continue. Do not abort the run.

## Failure / CAPTCHA handling

- If any LinkedIn page contains `captcha`, `verify your identity`, `unusual activity`, `please confirm you're a human`: stop scraping immediately, write whatever was already collected to outputs, report clearly: "LinkedIn requested verification at [URL]. Stopped at N results. Resolve in your browser and re-run."
- If a search returns zero results AND the page text doesn't contain expected LinkedIn UI text ("Posts", "People", "About"): treat as a parse failure, not a real zero. Surface as error.
- Never silently produce empty results.

## Scheduled run

The skill installs a scheduled task: weekly Mondays at 8:00am America/New_York, invoking `/cpo-tracker` (forward mode). The scheduled run requires LinkedIn to be logged in — if it's not, the run aborts cleanly and writes a note in the Desktop file.

To install/update the schedule, ask the user to confirm, then call `mcp__scheduled-tasks__create_scheduled_task` with cron `0 8 * * 1` (Monday 8am) and prompt `/cpo-tracker`.

## Final summary to the user

End each run with a one-paragraph summary in chat:
- Count of new placements found
- Count of filtered-out items + main reasons
- Notion sync status
- Path to Desktop log
- Any CAPTCHA / errors hit

Don't dump tables in chat — point RJ at the Desktop file and Notion. Brief.
