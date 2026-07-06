---
name: people-leader-role-watcher
description: Find and track Head of People, Head of Talent, VP People, VP Talent, Director-level People/Talent, Chief People Officer, and Founding People/Talent/Recruiter roles in an NYC Startup Job Board Airtable that RJ provides. Use when RJ shares a new Airtable URL from the NYC Startup Jobs Newsletter and wants the People & Talent leadership roles surfaced. Triggers on phrases like "run the role watcher on this airtable", "pull People leader roles from this list", "check this Airtable for TA leader roles", "scan this for Head of People openings". Outputs a clean table + diff vs. prior run.
---

# People Leader Role Watcher

v1.1 · 2026-05-07

## Purpose

Surface every Head of People / Head of Talent / VP / Director / Chief / Founding People & Talent leadership role in an NYC Startup Job Board Airtable. Built for RJ's job hunt, but transferable to any People leader.

## Trigger

**On-demand only.** This skill runs when RJ shares a new Airtable URL from the NYC Startup Jobs Newsletter (typically weekly). The newsletter at https://nycstartups.beehiiv.com/ publishes new curated lists every 1 to 2 weeks. RJ forwards the URL, then this skill executes.

## Inputs

Required:
- Airtable URL (provided by RJ when she runs this)

Optional:
- Stage filter (default: all)
- Industry filter (default: all)

## Title patterns to match (canonical list)

**Senior leadership:**
- Head of People
- Head of Talent
- Head of People & Talent / Head of People and Talent
- Head of Talent Acquisition / Head of TA
- VP People / VP, People / VP of People / VP People Operations
- VP Talent / VP, Talent / VP of Talent / VP of Talent Acquisition / VP TA
- Chief People Officer / CPO (for People role)
- Chief Talent Officer
- SVP People / SVP Talent

**Director-level:**
- Director, People / Director of People / Director of PeopleOps
- Director, Talent / Director of Talent / Director, TA
- Senior Director, People / Senior Director Talent

**Founding roles:**
- Founding Recruiter
- Founding Head of Talent / Founding Head of People
- Founding People Lead / Founding Talent Lead
- Founding Talent Partner
- Founding HR Lead

## Process

1. Navigate to the provided Airtable URL via Claude in Chrome.
2. Click "Filter rows" and add a Title contains filter.
3. Run filter for each substring sequentially:
   - "of People"
   - "of Talent"
   - "VP, People"
   - "VP, Talent"
   - "Chief People"
   - "Chief Talent"
   - "Founding" (then filter results for People, Talent, Recruiter, HR matches)
   - "Recruiter" (then filter for senior level: Head, Lead, Founding)
4. For each matched row, click Expand to capture: Title, Company, Industry, Stage, Last Funding, Headcount, Location, Job Link, Department.
5. Compile into the table format below.
6. Save to `/Claude for Builders/10x-TA-Leader/outputs/People-Leader-Roles-YYYY-MM-DD.md`.
7. If a previous People-Leader-Roles file exists in the outputs folder, compare and add a diff section: new roles, gone roles, companies with multiple matches.

## Output structure

### Headline (one paragraph)
Total matches. New since last run. NYC count. AI-flagged count.

### Master table

| # | Title | Company | Industry | Stage | Last Funding | Headcount | Location | AI? | Job Link |
|---|---|---|---|---|---|---|---|---|---|

### Sort order
1. NYC first, then Remote US, then Remote.
2. Within each location, sort by Last Funding amount descending.

### Diff section (when prior run exists)
- New since last run (table format, same columns)
- Disappeared since last run (Title + Company)
- Companies with multiple matching roles (signal of People function buildout)

### Fit notes
Brief 1-2 sentence prioritization note for the top 3 to 5 matches. Flag stage fit, location fit, AI signal, and any "why now" trigger (recent funding, leadership change).

## Quality bar

- Every match has full company context (Stage, Funding, Industry, Headcount).
- AI startups flagged in dedicated column.
- File is dated and versioned.
- Diff vs. prior week is included if prior file exists.

## First demo run

2026-05-07. See `/Claude for Builders/10x-TA-Leader/outputs/People-Leader-Roles-2026-05-07.md`.

## Future iterations

- Layer in Tech:NYC member careers pages.
- Layer in LinkedIn job alerts.
- Auto-cross-reference with companies RJ has already applied to (skip duplicates).
- Add personal fit score (RJ-defined criteria: stage preference, industry fit, location, mission alignment).
- Auto-trigger thank-you/intro outreach drafts for high-fit matches.
