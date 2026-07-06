---
name: competitor-knowledge-loader
description: Read and parse the existing competitor knowledge file at knowledge/competitors/{kebab-name}.md and return structured state — sections, last_updated, first_run flag, aliases. Use this skill at the start of any competitive intelligence run to load prior context before researching. Triggers on "load competitor knowledge for X", "check existing knowledge on X", or as Step 1 of the competitive-intelligence-agent workflow.
---

# Competitor Knowledge Loader

## Purpose

Step 1 of the Competitive Intelligence Brief workflow. Load the persistent knowledge file for a competitor so downstream skills can build on prior context rather than start from scratch.

## Inputs

- `competitor_name` (required) — e.g., "Acme Corp"
- `cadence_window` (optional) — e.g., "last 30 days". If omitted, derive from `last_updated`; on first run, treat as "since project inception".

## Procedure

1. **Resolve the path.** Compute slug as kebab-cased competitor name (lowercase, spaces → hyphens, punctuation removed). Target file: `knowledge/competitors/{slug}.md`.

2. **Check existence.**
   - If `knowledge/competitors/` directory does not exist, create it. Set `first_run = true`. Skip parsing. Return early.
   - If the file does not exist, set `first_run = true`. Return early with empty knowledge.
   - If the file exists, read it.

3. **Parse the file.** Extract:
   - YAML frontmatter: `competitor`, `slug`, `last_updated`, `first_seen`, `run_count`
   - Section contents: Aliases, Positioning, Product Moves, Hiring Signals, Public Commentary, Open Questions, Flagged Conflicts, Run Log
   - The schema is documented in [knowledge/competitors/_schema.md](knowledge/competitors/_schema.md).

4. **Validate schema.** If required sections are missing or the frontmatter is malformed, **stop and notify the operator**. Do not proceed (the updater skill should not overwrite an inconsistent file).

5. **Check freshness.** Compute days-since-`last_updated`. If greater than the cadence window, set `stale = true`. Surface this flag in the digest later.

## Output (structured return)

```yaml
first_run: <bool>
slug: <kebab>
path: knowledge/competitors/<slug>.md
last_updated: <date or null>
run_count: <int or 0>
stale: <bool>
aliases:
  product_names: [...]
  executive_names: [...]
  alternate_brands: [...]
existing_findings:
  positioning: [...]
  product_moves: [...]
  hiring_signals: [...]
  public_commentary: [...]
open_questions: [...]
flagged_conflicts: [...]
schema_valid: <bool>
notes: <any parsing observations>
```

## Failure modes

- **Schema mismatch** (hand-edited inconsistency): notify the operator, return `schema_valid: false`, do not proceed to Step 2.
- **Folder doesn't exist on first ever run**: create it, return `first_run: true`.
- **Malformed YAML frontmatter**: surface the error explicitly; do not guess.

## What this skill does NOT do

- Does not write to the file. (That's `competitor-knowledge-updater`.)
- Does not research. (That's `competitor-research`.)
- Does not decide whether a finding is novel — only returns prior state.
