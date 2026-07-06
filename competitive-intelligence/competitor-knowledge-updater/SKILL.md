---
name: competitor-knowledge-updater
description: Write findings back to the persistent competitor knowledge file at knowledge/competitors/{slug}.md. Bootstraps the file on first run; on subsequent runs appends date-stamped findings with source links, flags conflicts (never silently overwriting), accretes new aliases, and updates last_updated and run_count. Use this skill as Step 4 of the competitive-intelligence-agent workflow, after the brief has been synthesized.
---

# Competitor Knowledge Updater

## Purpose

Step 4 of the Competitive Intelligence Brief workflow. Write findings back to `knowledge/competitors/{slug}.md`. This is the compounding mechanism that turns a one-off workflow into a self-improving knowledge base.

## Inputs

- `findings` (required) — output of `competitor-research`
- `existing_knowledge` (required) — output of `competitor-knowledge-loader`
- `brief_path` (required) — where the synthesizer saved this run's brief
- `first_run` (required, bool)
- `slug`, `competitor_name`
- Schema convention at [knowledge/competitors/_schema.md](knowledge/competitors/_schema.md)

## Procedure

### First-run path (`first_run == true`)

1. Create `knowledge/competitors/{slug}.md` using the file template from `_schema.md`.
2. Set frontmatter:
   - `competitor: {Competitor Name}`
   - `slug: {slug}`
   - `last_updated: {today}`
   - `first_seen: {today}`
   - `run_count: 1`
3. Seed sections conservatively from `findings`:
   - **Only** include `confidence: corroborated` findings in section bodies on the first run.
   - `single-source` findings go in **Open Questions** with a "verify this" tag.
   - `paywalled` findings are noted but the content is not transcribed beyond the source title.
4. Populate **Aliases** from `findings.candidate_aliases`.
5. Add an initial **Run Log** entry: `{today}: brief at {brief_path}. N findings seeded.`

### Update path (`first_run == false`)

1. Read the current file (it was already validated by `competitor-knowledge-loader`).
2. **No-change short-circuit:** if `findings.no_change == true` (all categories empty after novelty filtering), skip the append loops below and go straight to the frontmatter + Run Log update at the bottom of this procedure. The knowledge file still gets a timestamp bump and a "no change" Run Log entry.
3. For each finding in `findings` with `novelty: new`:
   - Append to the matching section with format: `- {today}: {finding text} — [source]({url}) — confidence: {tier}`.
3. For each `novelty: update` finding:
   - Append a new bullet noting the update and referencing the prior item: `- {today}: UPDATE — {finding text} — [source]({url}) — refines prior item from {prior_date}`.
4. For each `novelty: conflict` finding:
   - Append the new finding to its category section as a normal bullet.
   - **AND** append a flag entry under **Flagged Conflicts**:
     ```
     - {today}: new finding contradicts prior content.
       New: "{finding text}" ([source]({url})).
       Prior: "{prior_reference}" (run {prior_date}).
       NEEDS RECONCILIATION.
     ```
   - **Never overwrite the prior content.**
5. For each `candidate_alias` not already in **Aliases**, append it under the appropriate subsection.
6. Update frontmatter: `last_updated: {today}`, `run_count: run_count + 1`.
7. Append to **Run Log**: `{today}: brief at {brief_path}. {N} new findings, {M} conflicts flagged.`

### Findings explosion guard

After writing, count active items in each category section:
- If a category exceeds **30** active items, age out the oldest `single-source` items by moving them to a `## Archive` section (create if needed).
- `corroborated` items are never aged out.
- Note in the Run Log if archiving happened.

## Output

```yaml
write_status: ok | error
path: knowledge/competitors/<slug>.md
findings_appended:
  new: <count>
  updates: <count>
  conflicts: <count>
aliases_added: <count>
archived: <count>
notes: <any caveats>
```

## Hard rules

1. **Never overwrite confirmed prior content.** Append always.
2. **Conflicts go to two places**: the category section (as a new finding) AND **Flagged Conflicts**.
3. **First-run is conservative.** Only corroborated findings seed sections; everything else goes to Open Questions or notes.
4. **Atomicity.** Read the file fresh, compute the full new content in memory, then write once. Do not perform multiple partial writes.
5. **Frontmatter is always updated**, even on a no-change run (timestamp + run_count bump).

## Failure modes

- **Concurrent write collision** (two scheduled runs hitting the same file): detect by re-reading just before write; if `last_updated` changed since the loader read it, abort with a clear error and surface in the digest. (A future Build iteration may add a file lock.)
- **Malformed markdown emission**: validate the rendered content against the schema template before writing. If invalid, abort and surface the error.
- **Disk full / permission denied**: surface the error; do not partially write.

## What this skill does NOT do

- Does not research. (That's `competitor-research`.)
- Does not synthesize the brief. (That's `competitor-brief-synthesizer`.)
- Does not reconcile flagged conflicts. (Reconciliation is a separate workflow, deferred to the Improve phase.)
