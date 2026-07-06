---
name: competitor-brief-synthesizer
description: Turn raw research findings into a structured markdown competitor brief following the project's brief template — what-changed summary, positioning, product moves, hiring signals, public commentary, open questions, flagged items. Enforces implication-not-just-fact, no padding, inline source citations, brand-neutral tone. Use this skill as Step 3 of the competitive-intelligence-agent workflow, after competitor-research has emitted findings.
---

# Competitor Brief Synthesizer

## Purpose

Step 3 of the Competitive Intelligence Brief workflow. Render the structured findings package into a publish-ready markdown brief.

## Inputs

- `findings` (required) — output of `competitor-research`
- `existing_knowledge` (required) — output of `competitor-knowledge-loader`
- `competitor_name`, `slug`, `cadence_window`, `run_count`
- Brief template at [templates/competitor-brief.md](templates/competitor-brief.md)

## Procedure

1. **Load the template.** Read `templates/competitor-brief.md`. Use its section structure exactly.

2. **Write the "What Changed Since Last Run" lead.**
   - Pick the 1–3 highest-signal `new`/`update`/`conflict` findings across all categories.
   - One bullet per finding, each carrying its implication (the "so what") and an inline `[source](url)`.
   - If `findings.no_change` is true, write: "No new signals this cycle. Knowledge file timestamp refreshed; no findings added."

3. **Draft each category section.** Two patterns apply:

   **a. Direct categories — Product Moves, Hiring Signals, Public Commentary.**
   - For each finding in that category, write 1–2 sentences: the fact + the implication.
   - Cite inline with `[source](url)` at the point of mention.
   - If a finding has `confidence: single-source` or `paywalled`, mark it inline: "(single-source — to verify)" or "(paywalled source)".
   - If the category has no findings, write the exact stock line from the template (e.g., "No product moves detected.").
   - **Never invent.** Never stretch one finding into three sentences.

   **b. Synthesized category — Positioning.** Positioning is NOT a research bucket. Derive it from cross-cutting patterns in the three direct categories:
   - Look across product, hiring, and commentary findings for signals about how the competitor positions itself (target audience, pricing posture, market segment, capability claims, narrative shifts).
   - Write 1–3 sentences synthesizing those signals, citing the underlying findings inline.
   - If no findings exist OR no positioning signal is detectable from the findings, write: "No positioning signals this cycle." Do not fabricate a positioning narrative from thin air.
   - On a first run with corroborated findings, this section establishes the initial positioning view — use only what the findings actually show.

4. **Open Questions.** Capture any single-source claims worth verifying and any ambiguities surfaced by the findings.

5. **Flagged Items.** List:
   - Every `novelty: conflict` finding with reference to the prior content it contradicts.
   - Paywalled sources that couldn't be verified.
   - If the competitor appears to have pivoted such that the schema no longer fits (e.g., they exited a product line entirely), add: "Schema-fit warning: {reason}. Consider revisiting the knowledge file schema for this competitor."
   - If nothing to flag, write: "None."

6. **Confidence Notes.** Count and report `corroborated`, `single-source`, `paywalled` totals.

7. **Header metadata.** Fill `Date`, `Cadence window`, `Run`, `Knowledge file` link.

## Output

A complete markdown brief, ready to save to `briefs/{slug}/{date}.md`. Return the full markdown string plus the target path.

## Hard rules

1. **Implication, not announcement.** Every finding gets a "so what" — competitive consequence, market signal, capability shift. Bare facts are rejected; revise before emitting.
2. **Cite at point of mention.** Sources go where they're referenced, not in a footer.
3. **Mark empty sections explicitly.** Use the template's stock lines. Do not pad.
4. **Brand-neutral tone.** No hype words ("game-changing", "revolutionary", "disrupts"). No editorial framing. Just what it is and what it implies.
5. **Cite only what the source supports.** If a source mentions Feature A, do not write that the competitor "now supports A, B, and C" because B and C feel adjacent.

## Failure modes

- **Findings are too thin to populate any category meaningfully**: produce a partial brief; mark empty sections honestly; the digest should note thin coverage.
- **A finding can't be cleanly categorized**: place it in the closest fit and note ambiguity in Open Questions.
- **Brief would duplicate the prior run's brief**: this should have been prevented upstream by `competitor-research` novelty tagging. If it still happens, flag for review and do not emit the duplicate.

## What this skill does NOT do

- Does not save the file to disk. (Caller saves to `briefs/{slug}/{date}.md`.)
- Does not update the knowledge file. (That's `competitor-knowledge-updater`.)
- Does not edit the template. Template changes are a Build/Improve decision, not a runtime decision.
