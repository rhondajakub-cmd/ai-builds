---
name: company-intelligence-brief
description: >
  Produces a fast, defensible intelligence brief on a single company. Pulls a
  fixed set of dimensions — snapshot (founded, HQ, offices, headcount, funding),
  what they do in plain terms, founders & leadership, leadership & org signals,
  investors & funding, profitability & clients, competitors, product, and how
  they hire — plus a rigorous AI-native assessment (is AI genuinely core to the
  product and company, or bolted on?). Ends with a clear signal read.
---

# Company Intelligence Brief

A fast, defensible read on a single company. One company at a time. The output
is a scannable brief with a clear signal, not a data dump.

## Operating rules

- **Accuracy over completeness.** Only present what is reported or on the record.
  If a data point cannot be found, say "Not found" — never guess a headcount, a
  funding figure, or a founder name.
- **Cite everything.** Every non-obvious claim gets an inline source link.
- **Label inferences.** Separate fact from read: "Reported:..." vs "I'm inferring...".
- **Voice.** Peer-level, matter-of-fact. No hype words, no breathless framing.

## Input

A company name (and website/URL if provided). If the name is ambiguous, confirm
which company before researching — match on domain, sector, or HQ.

## Research procedure

Run searches in parallel where possible. Prefer primary sources (company site,
careers page, founder LinkedIn, filings, reputable press) over aggregators.

**Handling conflicting data (common with headcount, revenue, valuation):**
Aggregators frequently disagree and lag reality. When numbers conflict, surface
the range, then state the figure from the best-sourced or most recent source and
label it. Never silently pick one; never average into a fake-precise number.

### 1. Snapshot
- Founded / age, and who was there at founding.
- HQ city + country.
- Known offices; note remote-first / hybrid / in-office model.
- Headcount + growth direction (surge, steady, layoffs), best-sourced.
- Funding line: latest round + date + valuation + lead investors.

### 2. What they do — in plain terms
One or two sentences a smart non-expert would understand. What the product is,
who pays, what problem it solves.

### 3. Founders & leadership
Founders and backgrounds; call out a shared pedigree if there is one. Note
marquee execs or notable technical leaders.

### 4. Leadership & org signals
- How the executive bench is built out, and where the gaps are.
- Note the state of key functions (e.g., is there a Head of People / senior
  functional leadership, or are roles unfilled at the company's scale?).
- Read the signal: a missing senior role at scale can indicate an under-built
  function or a fast-growth gap — name which it looks like and why.

### 5. Investors & funding
Total raised, latest round + date + lead investors, valuation, and trajectory
(up round / flat / down round — trajectory matters more than the absolute number).

### 6. Profitability & clients
- Profitable, breakeven, or burning? Distinguish "burning with strong traction"
  from "burning without it." Most private companies won't disclose — say so.
- Named customers, logos, customer count, case studies. Note if undisclosed.

### 7. Competitors
3–5 direct competitors, one line on differentiation. Name both sets if the
business model is hybrid (e.g., platform + services).

### 8. Product — noteworthy
Distinctive strengths (technical edge, data moat, delivery model, pricing,
traction) and notable weaknesses (reviews, incidents, churn, scalability questions).

### 9. How they hire — noteworthy
Interview process, hiring philosophy, unusual practices, and public signal on the
process (separate from overall employer rating).

### 10. AI-native assessment
Is AI genuinely core to who they are, or is it marketing? Gather evidence, then
classify. Do NOT take the company's own "AI-powered" copy at face value.

**Evidence:** product (core value prop vs. bolt-on; proprietary/fine-tuned vs.
wrapper), founding DNA (technical/ML founders? AI from the start or added late?),
hiring signal (ML/research roles, or "AI" only in marketing?), engineering signal
(technical blog, papers, model releases, infra).

**Classification:**
- **AI-Native** — built on AI; wouldn't exist without it; ML founding DNA.
- **AI-Enabled** — real established product that added meaningful, working AI.
- **AI-Veneer** — "AI" in the copy, thin evidence (wrapper, roadmap promise, buzzword).
- **Not-AI** — doesn't claim to be, and isn't.

**Two distinctions to always draw:** (1) authenticity vs. business model — an
AI-native firm can still be services-led vs. a product company; say which.
(2) DNA vs. dependency — AI-native leadership pedigree can coexist with a product
that's really a data/services platform with AI on top; say which.

Frame the call with evidence and a counter-signal: "Classifying them as [X]
because [evidence]. Counter-signal: [what cuts the other way]."

## Output format

```
# Company Intelligence Brief — [Company]
[one-line plain-English description] · [website]

## Snapshot
## What they do
## Founders & leadership
## Leadership & org signals
## Money & clients
## Competitors
## Product — noteworthy
## How they hire — noteworthy
## AI-native read
  - Classification + evidence + authenticity-vs-business-model + counter-signal

## Signal — [Watch closely / Monitor / Low priority]
[2–3 sentences: the company's trajectory, whether the AI story is real, and the
single biggest open question about the company.]

---
Sources: [inline throughout; key ones listed]
Not found: [dimensions that couldn't be sourced]
```

## Signal logic
- **Watch closely** — real product/traction, credible funding trajectory, a
  genuine AI story, and momentum worth tracking.
- **Monitor** — promising but a material unknown remains (financial health, the
  AI claim, or execution). Name the one thing to resolve.
- **Low priority** — weak signals: AI-veneer, instability (layoffs, down round,
  leadership churn), or no distinctive edge.

## Guardrails
- One company per run.
- Never state a headcount, funding figure, or founder name you couldn't source.
- If the company is early / stealth with little public, say so plainly and set
  the signal to "Monitor" with the gaps named — don't pad.
