---
name: competitor-research
description: Research a competitor's recent moves across product launches, hiring signals, and public commentary. Runs three web searches in parallel, enforces source-URL discipline, tags confidence tiers, cross-references against prior knowledge to label novel vs. restatement, and flags conflicts. Use this skill as Step 2 of the competitive-intelligence-agent workflow, after competitor-knowledge-loader has returned prior context.
---

# Competitor Research

## Purpose

Step 2 of the Competitive Intelligence Brief workflow. Gather source-verified signals about the competitor's recent activity, scoped to the cadence window, and produce a structured findings package for the synthesizer.

## Inputs

- `competitor_name` (required)
- `cadence_window` (required) — e.g., "last 30 days"
- `existing_knowledge` (required) — the output of `competitor-knowledge-loader`
- `aliases` (optional) — pulled from `existing_knowledge.aliases` when available

## Procedure

### 1. Build the search queries

Construct three independent query sets, scoped to the cadence window:

- **Product moves:** `{competitor} product launch OR release OR announcement {cadence}`; supplement with known product names from aliases.
- **Hiring signals:** `{competitor} hires OR new VP OR new CTO OR layoffs OR leadership {cadence}`; supplement with known exec names.
- **Public commentary:** `{competitor} analyst OR podcast OR interview OR case study {cadence}`.

### 2. Run the three searches in parallel

Fire all three WebSearch calls in a single tool-use round. Do not serialize them.

### 3. Triage each candidate finding

For each result, apply these rules:

| Rule | Action |
|------|--------|
| No accessible source URL | **Drop the claim.** |
| Single source | Tag `confidence: single-source`. |
| Two or more independent sources | Tag `confidence: corroborated`. |
| Source is paywalled | Tag `confidence: paywalled`, include source reference, **do not invent content behind the paywall**. |
| Finding matches something already in `existing_knowledge` | Tag `novelty: restatement`. Do not include in output. |
| Finding adds new detail to an existing item | Tag `novelty: update`. Include with reference to the prior item. |
| Finding has no prior mention | Tag `novelty: new`. Include. |
| Finding directly contradicts existing knowledge | Tag `novelty: conflict`. **Include AND flag**. |

### 4. Cross-reference against existing knowledge

Walk the three search result sets together. For each candidate finding, check `existing_knowledge.positioning`, `.product_moves`, `.hiring_signals`, `.public_commentary` for matches before tagging novelty.

### 5. Detect new aliases

If a search result mentions a product name, executive name, or alternate brand not in `existing_knowledge.aliases`, surface it as a candidate alias for the updater to append.

## Output

```yaml
competitor: <name>
slug: <kebab>
cadence_window: <window>
search_status:
  product: ok | partial | failed
  hiring: ok | partial | failed
  commentary: ok | partial | failed
findings:
  product_moves:
    - text: "<one-sentence claim>"
      source_url: "<url>"
      confidence: corroborated | single-source | paywalled
      novelty: new | update | conflict
      implication: "<so-what, one sentence>"
      prior_reference: "<text from existing_knowledge, if novelty=update|conflict>"
  hiring_signals: [...]
  public_commentary: [...]
candidate_aliases:
  product_names: [...]
  executive_names: [...]
  alternate_brands: [...]
no_change: <bool>      # true if zero new/update/conflict findings across all categories
notes: <any caveats — paywalls, timeouts, rate limits>
```

## Hard rules

1. **No source URL → no finding.** Drop the claim. Do not paraphrase from memory.
2. **Single source = lower confidence**, regardless of how plausible the claim sounds.
3. **Paywalled content is never invented.** Note the paywall, link to it, move on.
4. **Conflicts are flagged, not resolved.** The synthesizer surfaces them; the updater appends them; reconciliation is a separate workflow.
5. **Empty result set is a valid result.** Set `no_change: true`. Do not pad.

## Failure modes

- **Search timeout or rate limit on one of the three categories**: mark that category as `partial` or `failed` in `search_status`; proceed with the others; the digest must surface this.
- **All three searches fail**: return `no_change: false` with `search_status` all failed and `notes` explaining. Do not proceed to synthesis with no data.

## What this skill does NOT do

- Does not write the brief. (That's `competitor-brief-synthesizer`.)
- Does not update the knowledge file. (That's `competitor-knowledge-updater`.)
- Does not decide whether to escalate conflicts. (Operator does, async, via the digest.)
