# AI Builds — Rhonda (RJ) Jakub

Agents and workflows I've built for the real work of talent. I'm a Global People & Talent Leader (founding Talent teams @ Google + Facebook) who builds — these are the Claude skills and agents I use in my own work, most of them running on a schedule in production.

**Portfolio:** [rhondajakubportfolio.netlify.app](https://rhondajakubportfolio.netlify.app/) · **LinkedIn:** [linkedin.com/in/rhondajakub](https://www.linkedin.com/in/rhondajakub/)

---

## Talent Intelligence Agent

Five chained skills that map the talent market for a role — how many qualified people exist, what they cost, where they sit — then build a target-company list and a named candidate shortlist from a live search. Give it a role and a city; it hands back a sourcing brief a recruiter could pick up. [Case study →](https://rhondajakubportfolio.netlify.app/talent-intelligence-agent.html)

| Skill | What it does |
|---|---|
| [talent-map](talent-intelligence-agent/talent-map/SKILL.md) | Market sizing, supply/demand, comp benchmarks, common backgrounds |
| [target-company-builder](talent-intelligence-agent/target-company-builder/SKILL.md) | Ranked target companies with funding, headcount, and hiring signals |
| [candidate-sourcing-ranking](talent-intelligence-agent/candidate-sourcing-ranking/SKILL.md) | ICP + tiered Boolean strings; live LinkedIn validation to a named shortlist |
| [people-leader-role-watcher](talent-intelligence-agent/people-leader-role-watcher/SKILL.md) | Watches for senior People/Talent openings |
| [talent-intelligence-agent](talent-intelligence-agent/talent-intelligence-agent/SKILL.md) | Orchestrator — one command runs the chain end to end |

Architecture notes: [ARCHITECTURE.md](talent-intelligence-agent/ARCHITECTURE.md)

## Competitive Intelligence

A four-skill research pipeline with persistent memory: load prior knowledge → research recent moves (product, hiring, commentary) → synthesize a structured brief → write findings back so the next run knows what's already known. Conflicts get flagged, never silently overwritten.

| Skill | Role in the chain |
|---|---|
| [competitor-knowledge-loader](competitive-intelligence/competitor-knowledge-loader/SKILL.md) | Load prior state |
| [competitor-research](competitive-intelligence/competitor-research/SKILL.md) | Parallel web research with source discipline + confidence tiers |
| [competitor-brief-synthesizer](competitive-intelligence/competitor-brief-synthesizer/SKILL.md) | Implication-first brief, inline citations |
| [competitor-knowledge-updater](competitive-intelligence/competitor-knowledge-updater/SKILL.md) | Accrete knowledge, flag conflicts |

Agent: [competitive-intelligence-agent.md](competitive-intelligence/competitive-intelligence-agent.md)

## Talent-Market Intelligence

Scheduled agents that watch the senior People & Talent market — who's hiring, who's landing where, and what's changing across a target list of companies.

- [nyc-board-agent](market-intelligence/nyc-board-agent/SKILL.md) — weekly sweep of VC portfolio job boards (direct JSON APIs → SSR pages → search fallback), emailed as a digest ([agent file](market-intelligence/nyc-board-agent-agent.md))
- [vc-talent-agent](market-intelligence/vc-talent-agent/SKILL.md) — senior People/Talent hiring across top VC firms and portfolios
- [cpo-tracker](market-intelligence/cpo-tracker/SKILL.md) — tracks new CPO / Head of People placements, logs to Notion

## Productivity

- [daily-briefing](productivity/daily-briefing/SKILL.md) · [rj-morning-command-center-8am](productivity/rj-morning-command-center-8am/SKILL.md) · [weekly-planner](productivity/weekly-planner/SKILL.md) · [ss](productivity/ss/SKILL.md) (screenshot shorthand)

---

Built with [Claude](https://claude.com/claude-code). Skills follow the [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) format — a `SKILL.md` with frontmatter description plus instructions — and run in Claude Code, Claude Desktop, and Cowork.
