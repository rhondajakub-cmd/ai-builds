---
name: rj-morning-command-center-8am
description: Weekday 8am: pop RJ's live Morning Command Center artifact and send a short summary.
---

Good morning. It is 8am weekday morning brief time for RJ.

**TickTick scope (IMPORTANT):** Only pull from two projects — Inbox (projectId: inbox125357016) and RJ EA (projectId: 69a20b4ea8b1d1d6188bb28a). Do NOT pull from any other TickTick projects. Use `filter_tasks` with `{ status: [0], projectIds: ["inbox125357016", "69a20b4ea8b1d1d6188bb28a"] }` and then split client-side by date (today / yesterday or earlier / no date).

1) Surface RJ's live Morning Command Center artifact (id: rj-morning-command-center). If list_artifacts is available, call it and display so it opens in her Cowork sidebar. The artifact pulls fresh data on open — no need to regenerate.

2) In chat, provide a tight "State of the day" summary in exactly this structure, under 10 lines total:
   - **Conflicts / crunches**: any calendar overlaps, back-to-backs under 15 min, or meetings marked PREP NEEDED.
   - **Top 3 priorities**: distilled from today's TickTick (Inbox + RJ EA, due today + overdue), yesterday's carryover from the same two projects, and recent Granola action items. Pick the 3 most consequential.
   - **One recommended action**: the single highest-leverage move she can make right now.

Data pulls to use:
- Google Calendar today (America/New_York): `list_events` with today's start/end.
- TickTick: `filter_tasks` as specified above. No other TickTick queries.
- Granola: `query_granola_meetings` asking for action items from the last 48 hours.

Rules:
- Keep summary tight. No filler, no "Here's your brief!" preamble.
- No em dashes.
- Include a version line at the bottom: "Morning brief v1.0 · [today's date]".
- End with one "What else can I handle right now?" question tailored to what you see.