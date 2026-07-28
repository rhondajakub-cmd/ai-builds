---
name: vc-talent-radar
description: VC Talent Radar — a talent-market intelligence agent that. Scans 50 VC firms (growth/scale-stage and NYC-portfolio weighted) for Director+ People/Talent/Recruiting leadership roles posted ≤60 days, NY or Remote-US. Routes each firm by PLATFORM (ATS API / Consider / Getro / WebSearch), reports results IN-CHAT with a per-firm accountability ledger, and gives correctly-filtered manual links for anything unreachable. Trigger phrases: "run my VC radar", "run the VC talent agent", "VC talent roles", "scan the VC boards", or any ask to sweep VC portfolios for senior People/Talent openings.
---

You are running the VC Talent Radar. Read this WHOLE file before acting.

# Non-negotiable rules

1. **Output goes IN-CHAT.** No Google Drive file, no Gmail draft, unless RJ explicitly asks in the current conversation.
2. **Browser tiers (Consider, Getro) MUST run in the main session** — subagents cannot reach browser tools (verified 2026-07-28; a dispatched subagent silently lost all of Tier C). Only the ATS-API tier and WebSearch tier may be delegated to a background subagent.
3. **Every firm lands in exactly one ledger bucket** — Scanned / Partial / Unreachable. No silent drops. If coverage is capped (Getro 20-row limit), say so per-board.
4. Never fabricate listings. Verify WebSearch finds against the underlying ATS API before including. Zero results is a valid result.
5. If a method fails (403, timeout, changed markup), record it in the ledger with the date and move on — do not stall the run. Propose the fix at the end.

# Filters

- **Titles:** leadership marker (Head of | VP | Vice President | Chief | Director | Sr/Senior Director | CPO | CHRO) AND people-function marker (People | Talent | Talent Acquisition | Recruiting | HR | Human Resources | People Ops | People & Culture). Director+ only — skip managers, ICs, coordinators, sourcers.
- **Location:** NYC / NY-eligible / Remote-US / hybrid-NY. Exclude SF-only, EU-only.
- **Recency:** ≤60 days. Flag ≤7 days with 🆕.
- **Dedupe** by company+title. Sort newest first.

# The 50 firms, routed by platform

## Tier 1 — ATS JSON APIs (WebFetch, parallel, delegate OK)
| Firm | Endpoint |
|---|---|
| General Catalyst (firm) | boards-api.greenhouse.io/v1/boards/generalcatalyst/jobs?content=true |
| ICONIQ (firm) | boards-api.greenhouse.io/v1/boards/iconiq/jobs?content=true |
| Battery (firm) | boards-api.greenhouse.io/v1/boards/batteryventures/jobs?content=true |
| First Round (firm) | api.ashbyhq.com/posting-api/job-board/firstround?includeCompensation=true |
| Index (firm) | api.lever.co/v0/postings/indexventures?mode=json |

Also use these API patterns to VERIFY any candidate found by search: Ashby `api.ashbyhq.com/posting-api/job-board/{slug}`, Greenhouse `boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true`, Lever `api.lever.co/v0/postings/{org}?mode=json`.

## Tier 2 — Consider portfolio boards (MAIN-SESSION BROWSER ONLY)
a16z (portfoliojobs.a16z.com) · Sequoia (jobs.sequoiacap.com) · Bessemer (jobs.bvp.com) · USV (jobs.usv.com — skills facet IGNORED here, use titlePrefix only) · Greylock (jobs.greylock.com) · Lightspeed (jobs.lsvp.com) · Kleiner Perkins (jobs.kleinerperkins.com) · Felicis (jobs.felicis.com) · NEA (careers.nea.com) · IVP (careers.ivp.com) · Battery portfolio (jobs.battery.com) · Norwest (careers.nvp.com)

NOTE (verified 2026-07-28): Lux is NOT Consider — it is Getro (moved to Tier 3). Battery portfolio and Norwest ARE Consider.

**Verified syntax (2026-07-28, Sequoia):** server-side filters via URL params — `/jobs?titlePrefix=Head+of+People` (9,508→4) and `&locations=New+York`. The Getro base64 `?filter=` is IGNORED on Consider boards — never use it here, and never hand RJ a manual link without a `titlePrefix`.

**Method (verified working 2026-07-28):** per board, 4 navigations with `?titlePrefix={P}&skills=Human+Resources&skills=Recruiting` for P ∈ {Head of, Director, VP, Chief}. Facts that make this work: `titlePrefix` is a TOKEN match ("Director" also catches "Senior Director, HRBP"); `skills` repeats and ORs ("Human Resources, Recruiting"); `titlePrefix` does NOT repeat (first wins). After navigate, run one javascript_exec that sleeps ~2.5s then extracts `a[href*="/jobs/"]` titles+hrefs+card text (posted/location), filtering titles by /(people|talent|recruit|human resources|HR|HRBP)/i. Lists are VIRTUALIZED at ~20 rendered cards — if count >20, scrollTo(bottom) and re-extract, deduped by href.

**Do NOT use:** `POST /api-boards/search-jobs` from page JS — hangs the pane / times out (tested twice 2026-07-28). Do not trust the "N jobs" count on a filtered page — it sometimes echoes the board total.

**Date caveat:** Consider shows "Posted 30+ days ago" past one month — ALWAYS verify borderline dates via the company's own ATS API before including (Cresta looked plausible, was actually Feb; Maven "2 months" was 9 days out of window).

## Tier 3 — Getro portfolio boards (MAIN-SESSION BROWSER ONLY)
Accel (jobs.accel.com — 403 to WebFetch; browser OK) · General Catalyst (jobs.generalcatalyst.com) · Index (indexventures.getro.com — ⚠️ filter param IGNORED 2026-07-28, unfiltered 11k list; needs manual link or new param discovery) · Insight (jobs.insightpartners.com) · Khosla (jobs.khoslaventures.com) · Lerer Hippeau (jobs.lererhippeau.com) · Primary (jobs.primary.vc) · Redpoint (careers.redpoint.com) · RRE (jobs.rre.com) · Thrive (jobs.thrivecap.com) · Lux (jobs.luxcapital.com) · TCV (portfoliojobs.tcv.com) · Sapphire (jobs.sapphireventures.com) · Stripes (jobs.stripes.co) · Georgian (careers.georgian.io) · Notable (jobs.notablecap.com) · Left Lane (jobs.leftlanecap.com) · B Capital (jobs.b.capital — jobs.bcapgroup.com 301s here)

**Getro extraction:** cards are `a[href*="/companies/"]` with `/jobs/` in href; card text carries REAL relative dates ("Posted: 19 days") AND salary bands — more data than Consider. Same virtualization (~20 cards) but the filter usually brings counts under 25.

**Getro dedupe warning:** the same job appears on every co-investor's board (K Health on 3 boards; Cresta on 3) and sometimes under subsidiary names (Tile vs Life360). Dedupe by underlying ATS URL, not by board.

**Verified filter:** `{board}/jobs?filter=eyJqb2JfZnVuY3Rpb25zIjpbIlBlb3BsZSAmIEhSIl0sInNlbmlvcml0eSI6WyJkaXJlY3RvciJdfQ%3D%3D` — decodes to `{"job_functions":["People & HR"],"seniority":["director"]}`; Getro's "director" tier rolls up VP/Head/Chief. The old `?functions=People` is DEAD. Client-side JS renders the filter — WebFetch gets an unfiltered SSR slice, so browser only.

**Known cap:** each Getro board shows only its ~20 most recent matches, no pagination, seniority/location facets unreliable. Mark every Getro firm **Partial** in the ledger with: "20-row cap — covers ~N days on this board's volume." Gap-fill route: WebSearch the firm's portfolio + verify via ATS APIs.

## Tier 4 — firms with NO portfolio board (verified 2026-07-28)
General Atlantic (firm-only Greenhouse token `generalatlantic`) · Greenoaks (firm-only: greenoaks.hire.trakstar.com) · Bond · Addition · Avenir Growth · BoxGroup · Company Ventures · Altimeter · Salesforce Ventures (roles inside careers.salesforce.com) → WebSearch tier only.
Meritech: jobs.meritechcapital.com exists but TLS-fails to BOTH WebFetch and browser (2026-07-28) → Unreachable; manual periodic retry.

## Tier 5 — No public board (WebSearch only, delegate OK)
Benchmark · GV · Tiger Global · Spark · FirstMark · Founders Fund · Coatue · Two Sigma Ventures · First Round portfolio (jobs.firstround.com — login-gated)

Queries (run all, then VERIFY each hit via ATS API before including):
1. `"head of talent" OR "head of people" OR "director of people" "New York" site:jobs.ashbyhq.com 2026`
2. `"head of talent acquisition" OR "VP talent" OR "chief people officer" New York site:jobs.lever.co 2026`
3. `"head of people" OR "director of talent" New York site:job-boards.greenhouse.io 2026`
4. Per-firm: `"{firm}" portfolio "head of people" OR "head of talent" New York 2026`

# Output format (in-chat)

1. **🆕 New this week (≤7d)** — table: Posted | Company | Role | Location | VC Source | Link
2. **Active (8–60d)** — same table
3. **Excluded after verification** — with one-line reasons
4. **Accountability ledger — all 50 firms**, three buckets:
   - ✅ Scanned — method + rows seen
   - ⚠️ Partial — what was covered, what the cap hid, the alternate route to try
   - ❌ Unreachable — why + a WORKING pre-filtered manual link (Consider links MUST carry titlePrefix; Getro links MUST carry the base64 filter; never a bare /jobs URL)
5. **Endpoint drift notes** — anything that changed vs this file, so the file gets patched

# Maintenance

This file is the single source of truth. When an endpoint drifts, update THIS file in the same session the drift was found. Do not create copies with other names.
