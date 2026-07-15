---
name: capacity-model
description: >
  RJ's recruiter capacity model. Takes a req list (CSV, ATS/job-board export, or pasted list) plus
  optional company context and optional historical recruiting data, and returns a defensible answer to
  "how many recruiters do we need to hit these hiring goals?" — with every number's provenance labeled.
  Use when RJ says "run my capacity model", "how many recruiters", "capacity plan", "size the recruiting
  team", "can this TA team hit this hiring plan", or provides a req list / careers-page export and asks
  about recruiter staffing.
---

# Recruiter Capacity Model

Reqs in → five-factor difficulty scores → weighted load → recruiter count, math shown.

## The No-Guessing Rule (governs everything)

No number in any output comes from anyone's gut. Every figure resolves through this hierarchy, and every output labels each number's provenance:

1. **[company data]** — the user's historical data (hires/recruiter, TTF, OAR, pause rates) when provided. Always overrides benchmarks where it exists.
2. **[benchmark]** — published figures from `~/Claude for Builders/capacity-model/benchmarks.md` (read it at run time; every figure there is cited with source + year).
3. **[derived]** — arithmetic on published figures, with the derivation shown.
4. **[gap]** — neither exists: name the gap and present a sensitivity range ("if X=10% → N; if X=20% → N+1"). Never silently fill a hole.

If asked for a number the hierarchy can't produce, say so — that answer is part of the product.

## Step 1 — Ingest & normalize (sources are additive)

Accept any mix of sources, and allow reqs to be **added to an existing run** at any time:
- Public job-board pull (Ashby: `api.ashbyhq.com/posting-api/job-board/{org}`; Greenhouse: `boards-api.greenhouse.io/v1/boards/{org}/jobs`)
- CSV / ATS export
- Pasted list from internal sources — including **planned-but-unposted headcount** (a hiring plan is more than the live board)

Tag every req with its `source` (board / ats-export / internal-plan / manual). When reqs are added to an existing run: score only the new reqs (reuse cluster scores where they fit an existing cluster), preserve any user overrides on existing reqs, recompute totals, and append a revision note to the run doc. Normalize each req: title, function, location, workplace type (remote/hybrid/onsite), posted comp if any, open date.

- **Infer level from title** (Junior/Mid/Senior/Staff+/Manager/Director/VP+). Flag ambiguous inferences in the output.
- **Job-board caveat:** postings ≠ approved reqs. Flag postings open >6 months as likely evergreen. State the Greenhouse ghost-posting benchmark (18–22% of postings never actively pursued, Q4 2024) as an input caveat for any board-scraped portfolio.
- **Intake questions** (ask what's known; flag the rest): fill expectations (else the 45–90-day default applies) · current team size · **sourcing stack & technology** (ATS, LinkedIn Recruiter seats, sourcing/CRM tooling, AI sourcing, scheduling automation) · **sourcing & coordination support model** (dedicated sourcers? coordinators? ratios?).

## Step 1b — Sourcing support & stack: the LEVERAGE layer

[user rule — RJ 2026-07-09]: **never recommend sourcing/coordination headcounts in the output.** Support model and sourcing stack (including AI tooling) enter as a **bounded multiplier on base throughput** (effective throughput = base × leverage), the mirror of how difficulty weights reqs. Anchored bands (evidence: `~/Claude for Builders/capacity-model/leverage-research.md`):

| Leverage tier | Multiplier | Basis |
|---|---|---|
| Under-equipped (no coordination support, minimal tooling) | **~0.85x** | [derived] inverse of measured scheduling burden (25–38% of recruiter time) going unreclaimed |
| Benchmark-typical | **1.0** | Ashby/Gem base rates are measured on modern-ATS orgs with typical support — that IS the benchmark org |
| Best-in-class (full coordination + genAI adoption + AI top-of-funnel) | **1.1–1.3x** | [derived] composite of published anchors (coordination +10–30% time-reclaim, genAI +10–20% LinkedIn FoR 2025, AI screening ~+10–15% job-level), capped — compounding uncertain bands is not allowed |

Rules: leverage is always shown as a **range on the headline, never a point**. When [company data] throughput exists, leverage is already embedded in it — the multiplier prices *changes* only ("if they add AI sourcing"). On benchmarks-only runs, set the tier from the intake questions or a stated [assumption], and say which.

## Step 2 — Score difficulty: 4 market factors + 2 company modifiers [redesigned per RJ 2026-07-10]

**Core factors — about the MARKET for this role** (1–5 each, sum 4–20):

| Factor | 1 (easy) → 5 (brutal) |
|---|---|
| Market scarcity | abundant pool (SDR, support) → low-hundreds globally (ML research, niche security) |
| Seniority | junior IC → Staff/Principal/Director (VP+ triggers exec-class override) |
| Location & remote | remote-open → hybrid major hub → onsite required → onsite thin market |
| Comp competitiveness | above band → at band → **unknown/not published = 3 with flag** → below band (known declines = 5) |

**Company modifiers — about THIS company, signed, can push either way:**

| Modifier | Range | Meaning |
|---|---|---|
| Employer brand | **−2 … 0 … +2** | −2 magnet brand *for this talent pool* · 0 **no effect** · +2 unknown or negative reputation. Score per talent pool, not per company — a dev-tools darling can be −2 for engineers and 0 for enterprise sales buyers. Anchor within published ranges (outreach reply ~21% avg; OAR spread 60–95%) |
| Hiring bar | **−1 … 0 … +2** | −1 below-benchmark selectivity (hires fast) · 0 benchmark-average · +2 famously selective (top-percentile-only screening = more sourcing, more loops, more declined finalists per hire) |

**Hiring-bar provenance (in hierarchy order):** funnel data — interviews-per-offer, pass-through vs Ashby norms [company data] → stated philosophy or public reputation [assumption, labeled] → 0 [gap]. **Double-count guard:** when [company data] *throughput* drives the math, the company's bar and brand are already embedded in it — set both modifiers to 0 except where a specific req deviates from that company's own norm. Modifiers are fully active on benchmarks-only runs.

**Total = core + brand + bar** (range 1–24) → tier and load weight:

| Tier | Total | Load weight | Anchor (why this weight is defensible) |
|---|---|---|---|
| Standard | ≤7 | 0.7 | high-volume profiles sustain 3–4x corporate req loads (SHRM) |
| Moderate | 8–11 | 1.0 | baseline = the "average req" the throughput benchmarks describe |
| Hard | 12–15 | 1.4 | tech-vs-business published deltas: 1.5x interviews/hire, ~2x interviewer-hours, OAR 73% vs 84%, +15d TTF (Ashby 2026) |
| Very Hard | 16+ | 1.8–2.0 | sourced-dependent scarce pools: ~8% outreach-interested yield (Gem), senior +37% TTF (Ashby) |
| Exec (VP+/C) | override | **no weight — dedicated slot** | published search durations: Director ~2.5–3.5mo, VP ~3.5–4mo, C-suite 4+mo |

(Thresholds recalibrated from the old 5-factor scale so a neutral-modifier org lands in the same tiers as before.)

**Exec-class rule [user rule — RJ, 2026-07-09]: VP and above is exec, no exceptions** — including RVP/Regional Vice President titles. Directors stay in-book. Exec reqs never enter the load math: **a handful of exec searches (~4 concurrent) go to ONE dedicated leadership recruiter, who also carries a few director-level reqs. Do not put agency cost figures in the output.**

Score in clusters of similar reqs (same family/level/location), not one-by-one theater. Show at least one cluster's five-factor scoring in full so the method is inspectable.

**Scores are reviewable and editable — always.** Alongside the run doc, emit `runs/{company}-{date}-scores.csv`: one row per req with its cluster, all five factor scores, sum, tier, weight, flags — plus empty `override_*` columns for each factor and the tier. The user can edit the CSV directly or say adjustments in chat ("CUR-027 scarcity should be 4", "move federal cluster to Very Hard"). On any override: recompute sums/tiers/weights for affected reqs, rerun the capacity math, and append a **Revision** section to the run doc showing what changed and how it moved the headline. User overrides are provenance-tagged **[user override]** and survive re-pulls and added reqs.

## Step 3 — Classify recruiter books

Split reqs by the talent pool they recruit from, not the department label: **technical book** (software/ML/data/design/field-and-solutions engineering, technical systems roles) vs **business book** (sales, marketing, CS, people, G&A). Exec-class reqs form a third bucket (slots, not load). Note misfiled reqs (e.g., a recruiting coordinator posted under Sales).

## Step 4 — Capacity math (SLA basis is the headline; two more lenses behind it)

**Lens A — fill-expectation SLA (the headline).** Companies don't fill boards as batch projects — each req carries an expectation of how fast it fills. Default fill expectations per tier [user default — RJ 2026-07-09: standard roles fill in **45–90 days, i.e., within the quarter**; deliberately a band, not a point estimate]:

| Tier | Fill expectation | Anchor |
|---|---|---|
| Standard / Moderate | **within the quarter** (45–90 days) | band brackets the published medians: SHRM 2025 US median 44d non-exec; Ashby 2026 time-to-first-fill ~8 wks business / ~10 wks technical — the quarter-unit math is insensitive to where in the band the truth sits |
| Hard | **1.5 quarters** (~90–135 days) | [derived] Ashby 2026: technical +15 days, senior +37% |
| Very Hard | **2 quarters** | [derived] compounding scarce + senior |
| Exec | published search durations | Director ~2.5–3.5mo, VP ~3.5–4mo, C-suite 4+mo [benchmark] |

Ask whether the company has its own fill-time expectations (SLA policy or historical TTF [company data]); these defaults are overridable like any score.

Per-tier math, per book: **recruiters_T = reqs_T ÷ ((base throughput ÷ tier weight) × tier horizon in quarters)**. Sum tiers → book need; sum books + exec slots → total. Base throughput: [company data] if provided, else [benchmark] Ashby 2026 (3.8/qtr technical, 5.0 business). Exec: 1 senior recruiter runs ~2–3 concurrent searches, or agency at ~$100K+/search [benchmark].

**The inversion (always include when current team size is known):** the same math run backwards gives the **open-req budget** — how many weighted units per quarter the current team can keep inside SLA (team × base throughput). This tells a TA leader how many reqs they can afford to have open at once, which is often the more actionable number than "hire more recruiters."

**Lens B — batch fill-by-date (scenario table):** the old framing, kept as scenarios — reqs ÷ (adjusted throughput × horizon) for 2-qtr and 3-qtr horizons. Useful when leadership genuinely thinks in "clear the board by X" terms.

**Lens C — sustainable-carry (cross-check):** weighted units ÷ Gem 13.4 and ÷ SHRM ~20 → carry band. When SLA-basis > carry band, say why: carrying reqs isn't closing them inside an SLA. Divergences are explained, never averaged.

**Lens B — sustainable-carry (load):** the cross-check.
- Weighted concurrent units ÷ Gem 13.4 avg open reqs/recruiter, and ÷ SHRM ~20 survey figure → a carry band.
- When Lens A > Lens B, say why: carrying reqs isn't closing them by a date. This divergence is a feature — explain it, don't average it.

## Step 5 — Volatility & sensitivity

Volatility (ghost postings, evergreen reqs, mid-quarter pauses) is **accounted for inside the "Challenges & adjustments" section — never as headline scenarios or discount rows in the recommendation** [user rule — RJ 2026-07-09]. Use the company's pause rate [company data] when available, else the published proxies (Greenhouse 18–22% ghost postings; Revelio <50% filled at 6mo), state the adjusted durable-core number once in that section, and frame the remedy as req-by-req intake triage ("is this seat real, funded, dated?"), not a blanket discount.

## Step 6 — Output format (layered: skim first, dig second)

The output is three layers, so a reader can review results at altitude and then drill down:

- **Layer 1 — THE RECOMMENDATION** (top of run doc, must stand alone). Opens with a compact **"Where these assumptions come from"** block [user rule — RJ 2026-07-09] naming the four sources before any numbers: (1) published benchmarks used (Ashby/Gem/SHRM + years, full citations in benchmarks.md), (2) company data and what it covers (or "none — benchmarks-only run"), (3) operating standards set by the TA leader (fill windows, VP+ exec rule, support model), (4) everything else is shown arithmetic or a named gap. Then one table, one answer — **no scenario tables, no discount rows, no alternate lenses here**:

  | Recruiter type | Open reqs | Very Hard | Hard | Moderate | Standard | Recruiters needed |
  |---|---|---|---|---|---|---|
  | Technical | … | n | n | n | n | **N** |
  | Business | … | n | n | n | n | **N** |
  | Leadership (VP+) | … | n exec searches | | | | **1** |
  | + Support (sourcing & coordination) | — | | | | | coordinators + sourcer coverage per Step 1b |
  | **Total** | … | | | | | **N** |

  Difficulty tier counts get their own explicit columns (never squashed into "15/29/0" shorthand). Add Have/Gap columns when current team size is known. Directly under the table: a bold **recommendation sentence** (staff N: X technical, Y business, 1 leadership), including the open-req-budget alternative when N isn't fundable ("a smaller number isn't the alternative — a smaller board is"). Then a **difficulty legend**: each tier's score range, plain-language meaning, and which of this company's reqs sit in it. Then the 2–3 judgment calls most worth challenging. A reader who stops here has the staffing plan. Alternate lenses (batch-fill, carry) live in Layer 2 as cross-checks only.
- **Layer 2 — The reasoning** (rest of run doc): math, difficulty map, cross-check, exclusions, assumptions.
- **Layer 3 — The data** (`-scores.csv`): every req, every factor score, editable overrides.

Mandatory sections in the run doc:

1. **Headline** — recruiter count (range across scenarios), one paragraph, plain language, followed immediately by the scenario table and a "worth challenging" list of the biggest judgment calls (these are the review entry points).
2. **The math** — Lens A per book, shown as arithmetic with provenance tags on every number.
3. **Difficulty map** — cluster table: cluster, req count, tier, weight, one-line rationale; plus one fully-worked five-factor example.
4. **Cross-check** — Lens B band and what the divergence from Lens A means.
5. **Scenario table** — horizon × volatility.
6. **What this model excludes** — verbatim list, every run: hiring-manager responsiveness and interview-loop weight, recruiter ramp time, req arrival during the period (the plan models today's snapshot). Each exclusion gets one line on the direction it would move the answer. (Hiring bar is no longer excluded — it's a scored company modifier per Step 2; note its provenance in the assumptions.)
7. **Assumptions & flags** — fill horizon, level inferences flagged, evergreen postings, comp-unknown flags, book classification judgment calls.

Never output a recruiter count without sections 6 and 7. The model's credibility *is* the labeled uncertainty.

## Placeholders (mandatory in every run doc)

The model is **benchmarks-first with named plug-in slots** [user rule — RJ 2026-07-09]. Every run doc shows two placeholders explicitly, filled or empty:

1. **Historical data** — hires/recruiter/qtr, time-to-fill, offer-accept, req-pause rate. When provided, replaces the benchmark base rates row-by-row (tagged [company data]); when absent, the slot reads "none provided — benchmark rates in effect" so the reader sees exactly what a client's ATS export would change.
2. **Sourcing & tooling profile** — coordination support, dedicated sourcers, stack/AI adoption. Sets the leverage tier (Step 1b); when unknown, state the assumption used and its tier.

## Run artifacts

Save each run to `~/Claude for Builders/capacity-model/runs/{company}-{date}.md`. Test fixtures: `real-portfolio/cursor-reqs.csv` (benchmarks-only path), `synthetic-portfolio/` (Meridian — exercises the historical-merge path; its `historical-data.md` numbers must override benchmarks and be tagged [company data] in output).
